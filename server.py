#!/usr/bin/env python3
"""Klątwa Siedmiu Światów — etap 1, lokalny serwer LAN."""
import json, os, time, threading
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT=Path(__file__).resolve().parent
SAVE=ROOT/"stan_wprowadzenia.json"
LOCK=threading.RLock()
PASSWORD=os.environ.get("SWIATY_HASLO","morthar-2026")
PAGES=[
("TAJEMNICA ÓSMEGO POKOJU","Myślałyście, że znacie ten dom. Wiecie, gdzie skrzypi podłoga i gdzie nocą pojawiają się dziwne cienie. Ale jest coś, o czym nikt wam nie powiedział. Dawno temu w tym domu istniał ósmy pokój. Nie miał okien. Nie było go na żadnym planie. Nazywano go Komnatą Cienia."),
("MORTHAR, STRAŻNIK CZASU","W Komnacie Cienia mieszkał Morthar — potężny Strażnik Czasu. Pewnej halloweenowej nocy zapragnął zatrzymać czas na zawsze. Zaklęcie wymknęło się spod kontroli. Zegar rozpadł się na siedem fragmentów, a dom został uwięziony pomiędzy Siedmioma Światami. Komnata zniknęła. Ale Morthar nigdy nie odszedł."),
("PRZEBUDZENIE SIEDMIU ŚWIATÓW","Dziś, w halloweenową noc, granica między światami ponownie pęka. W salonie budzą się bestie. W sypialni lustra zaczynają szeptać. W kuchni odzywa się aparatura zaginionego naukowca. A w starej garderobie pojawiają się drzwi, których wcześniej nie było. Morthar powrócił."),
("WIADOMOŚĆ OD MORTHARA","WITAJCIE, MAŁE STRAŻNICZKI. A więc to wy zamierzacie mnie powstrzymać? Daję wam 120 minut. Siedem Światów. Siedem pieczęci. Jedna szansa. W każdym świecie pozostawiłem zagadki, których nie rozwiąże żadna z was samotnie. Jeśli zabraknie wam czasu... ZOSTANIECIE TU ZE MNĄ. Tik. Tak. Tik. Tak."),
("SIEDEM PRAW — CZĘŚĆ PIERWSZA","I. Nie wolno przechodzić do kolejnego pomieszczenia, dopóki aplikacja go nie odblokuje.\n\nII. Każda z was otrzyma inne wskazówki. Rozmawiajcie i współpracujcie.\n\nIII. Obie musicie potwierdzić rozwiązanie na swoich tabletach."),
("SIEDEM PRAW — CZĘŚĆ DRUGA","IV. Od startu pierwszego świata macie 120 minut. Próby Czasu mogą dać wam dodatkowe minuty.\n\nV. Używajcie czołówek. Nie niszczcie rzeczy ani nie otwierajcie miejsc poza grą.\n\nVI. Zachowujcie wszystkie fragmenty Pieczęci.\n\nVII. Eksperymenty wykonujcie tylko za zgodą Mistrza Gry. Nie dotykajcie obracających się urządzeń ani przewodów. Gdy dorosły przerywa grę, natychmiast przestańcie.")
]
RACES=["Elfka Księżyca","Wampirzyca","Wróżka Cieni","Czarownica"]
AVATARS=["🌙","🦇","🧚","🔮","🐈‍⬛","🕯️","🦉","✨"]
BEASTS={"Wampir":"7","Wilkołak":"2","Mumia":"9","Wiedźma":"4","Duch":"1","Kościotrup":"6"}
SEARCH_ORDER=["Kościotrup","Duch","Wiedźma","Mumia","Wampir","Wilkołak"]
def fresh(): return {"players":{"1":None,"2":None},"page":0,"oaths":{"1":False,"2":False},"started_at":None,"world1":{"found":[],"numbers":{},"answers":{"1":False,"2":False},"envelope":{"1":False,"2":False}}}
try: STATE=json.loads(SAVE.read_text(encoding="utf-8"))
except (FileNotFoundError,ValueError): STATE=fresh()
def save(): SAVE.write_text(json.dumps(STATE,ensure_ascii=False,indent=2),encoding="utf-8")
if "world1" not in STATE: STATE["world1"]=fresh()["world1"]
def snapshot(role):
    players=STATE["players"]; page=STATE["page"]; started=STATE["started_at"]
    phase="create" if not players[role] else "waiting" if not all(players.values()) else "story" if page<len(PAGES) else "playing" if started else "oath"
    reader=str(page%2+1) if page<len(PAGES) else None
    w=STATE["world1"]
    stage="search" if len(w["found"])<6 or len(w["numbers"])<6 else "solve" if not all(w["answers"].values()) else "envelope" if not all(w["envelope"].values()) else "finished"
    return {"world1":{"stage":stage,"found":w["found"],"numbers":w["numbers"] if role=="2" else {},"answers":w["answers"],"envelope":w["envelope"],"search_order":SEARCH_ORDER if role=="1" else []},"role":role,"profile":players[role],"players":players,"phase":phase,"page_index":page,"page_count":len(PAGES),"reader":reader,"page":{"title":PAGES[page][0],"text":PAGES[page][1]} if phase=="story" and role==reader else None,"oaths":STATE["oaths"],"remaining":max(0,7200-int(time.time()-started)) if started else 7200}
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def reply(self,obj,status=200,html=False):
        raw=obj if isinstance(obj,bytes) else (json.dumps(obj,ensure_ascii=False).encode("utf-8"))
        self.send_response(status); self.send_header("Content-Type","text/html; charset=utf-8" if html else "application/json; charset=utf-8"); self.send_header("Cache-Control","no-store"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=="/": return self.reply((ROOT/"index.html").read_bytes(),html=True)
        if u.path=="/api/state":
            role=parse_qs(u.query).get("role",[""])[0]
            if role not in ("1","2"): return self.reply({"error":"Nieprawidłowy gracz"},400)
            with LOCK: return self.reply(snapshot(role))
        return self.reply({"error":"Nie znaleziono"},404)
    def do_POST(self):
        try:
            n=int(self.headers.get("Content-Length","0"))
            if not 1<=n<=4096: raise ValueError()
            data=json.loads(self.rfile.read(n))
            if not isinstance(data,dict): raise ValueError()
        except (ValueError,TypeError): return self.reply({"error":"Nieprawidłowe dane"},400)
        role=str(data.get("role","")); path=urlparse(self.path).path
        with LOCK:
            if path=="/api/admin/reset":
                if data.get("password")!=PASSWORD: return self.reply({"error":"Nieprawidłowe hasło"},403)
                STATE.clear(); STATE.update(fresh()); save(); return self.reply({"ok":True})
            if role not in ("1","2"): return self.reply({"error":"Nieprawidłowy gracz"},400)
            w=STATE["world1"]
            if path=="/api/world1/find":
                if not STATE["started_at"] or role!="1": return self.reply({"error":"Ta czynność należy do Strażniczki I"},403)
                beast=str(data.get("beast",""))
                if beast not in BEASTS: return self.reply({"error":"Nieznana bestia"},400)
                if beast not in w["found"]: w["found"].append(beast)
                save(); return self.reply({"ok":True})
            if path=="/api/world1/number":
                if not STATE["started_at"] or role!="2": return self.reply({"error":"Ta czynność należy do Strażniczki II"},403)
                beast=str(data.get("beast","")); number=str(data.get("number","")).strip()
                if beast not in w["found"]: return self.reply({"error":"Najpierw znajdźcie tę bestię"},409)
                if number!=BEASTS.get(beast): return self.reply({"error":"Cyfra nie pasuje do bestii. Sprawdźcie odwrotną stronę karty."},409)
                w["numbers"][beast]=number; save(); return self.reply({"ok":True})
            if path=="/api/world1/answer":
                if not STATE["started_at"] or len(w["found"])!=6 or len(w["numbers"])!=6: return self.reply({"error":"Najpierw zbierzcie sześć bestii i cyfr"},409)
                if str(data.get("code","")).strip()!="7219": return self.reply({"error":"Pieczęć nie ustępuje. Sprawdźcie bestie i ich kolejność."},409)
                w["answers"][role]=True; save(); return self.reply({"ok":True})
            if path=="/api/world1/envelope":
                if not all(w["answers"].values()): return self.reply({"error":"Obie Strażniczki muszą złamać pieczęć"},409)
                w["envelope"][role]=True; save(); return self.reply({"ok":True})
            if path=="/api/create":
                if STATE["players"][role] or STATE["page"] or STATE["started_at"]: return self.reply({"error":"Postać już zapisana"},409)
                name=str(data.get("name","")).strip()
                if not 2<=len(name)<=20 or data.get("race") not in RACES or data.get("avatar") not in AVATARS: return self.reply({"error":"Wpisz imię, wybierz rasę i awatar"},400)
                STATE["players"][role]={"name":name,"race":data["race"],"avatar":data["avatar"]}; save(); return self.reply({"ok":True})
            if not all(STATE["players"].values()): return self.reply({"error":"Czekamy na drugą postać"},409)
            if path=="/api/next":
                if STATE["page"]>=len(PAGES): return self.reply({"error":"Historia już zakończona"},409)
                if role!=str(STATE["page"]%2+1): return self.reply({"error":"Teraz czyta druga Strażniczka"},403)
                STATE["page"]+=1; save(); return self.reply({"ok":True})
            if path=="/api/oath":
                if STATE["page"]<len(PAGES) or STATE["started_at"]: return self.reply({"error":"Nie można jeszcze złożyć przysięgi"},409)
                STATE["oaths"][role]=True
                if all(STATE["oaths"].values()): STATE["started_at"]=time.time()
                save(); return self.reply({"ok":True})
        return self.reply({"error":"Nieznana operacja"},404)
if __name__=="__main__":
    port=int(os.environ.get("SWIATY_PORT","8000"))
    print(f"Gra działa na porcie {port}. Otwórz http://ADRES_IP_LAPTOPA:{port}",flush=True)
    ThreadingHTTPServer(("0.0.0.0",port),Handler).serve_forever()
