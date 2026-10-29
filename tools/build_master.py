#!/usr/bin/env python3
"""Build canonical two-document set for Klątwa Siedmiu Światów.
Uses existing verified original drawing assets and new authoritative setup text.
All source graphics live under assets/zrodla; only the two PDFs at repository root are printable.
"""
import os, math, re
from pathlib import Path
import fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, SimpleDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE = Path(os.getenv('HALLOWEEN_ASSET_DIR', str(PROJECT_ROOT)))
OUT = Path(os.getenv('HALLOWEEN_OUT_DIR', str(PROJECT_ROOT)))
OUT.mkdir(parents=True, exist_ok=True)
ASSETS={
'monsters':'assets/zrodla/karty_potworow.png',
'world2':'assets/zrodla/lustrzane_wiadomosci.pdf',
'enigma':'assets/zrodla/enigma_instrukcja_obrazkowa.pdf',
'discs':'tarcze_7_2_4_test.pdf',
'symbols4':'assets/zrodla/symbole_zegara.pdf',
'books5':'assets/zrodla/symbole_ksiazek.pdf',
'final7':'assets/zrodla/list_morthara_i_zaklecie.pdf'
}

def locate(key):
 if key not in ASSETS: raise KeyError(f'Unknown source asset: {key}')
 candidate=BASE/ASSETS[key]
 if candidate.is_file():return candidate
 raise FileNotFoundError(f'Brak wymaganego źródła {key}: {candidate}. Sprawdź folder assets/zrodla.')

fonts=[('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','DV'),('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','DV-B'),('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf','DVS'),('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf','DVS-B')]
for f,n in fonts:pdfmetrics.registerFont(TTFont(n,f))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-B',italic='DV',boldItalic='DV-B')
INK=colors.HexColor('#202237'); PUR=colors.HexColor('#573864'); GOLD=colors.HexColor('#bd955e'); PALE=colors.HexColor('#f5f1f8'); GREY=colors.HexColor('#5a5566')
MARGIN=43
ST={
 'title':ParagraphStyle('Title',fontName='DVS-B',fontSize=22,leading=29,textColor=PUR,spaceAfter=12),
 'subtitle':ParagraphStyle('Subtitle',fontName='DV',fontSize=11,leading=17,textColor=GREY,spaceAfter=14),
 'h1':ParagraphStyle('H1',fontName='DV-B',fontSize=15.2,leading=22,textColor=PUR,spaceBefore=18,spaceAfter=10,keepWithNext=True),
 'h2':ParagraphStyle('H2',fontName='DV-B',fontSize=10.6,leading=16,textColor=PUR,spaceBefore=11,spaceAfter=6,keepWithNext=True),
 'p':ParagraphStyle('Body',fontName='DV',fontSize=9.15,leading=14.6,spaceAfter=7,textColor=INK),
 'small':ParagraphStyle('Small',fontName='DV',fontSize=8,leading=12,textColor=INK,spaceAfter=5),
 'tiny':ParagraphStyle('Tiny',fontName='DV',fontSize=7,leading=10,textColor=INK,spaceAfter=3),
 'splash':ParagraphStyle('Splash',fontName='DVS-B',fontSize=23,leading=33,alignment=TA_CENTER,textColor=PUR,spaceAfter=15),
 'center':ParagraphStyle('Center',fontName='DV-B',fontSize=12,leading=20,alignment=TA_CENTER,textColor=PUR,spaceAfter=12),
 'quote':ParagraphStyle('Quote',fontName='DVS',fontSize=10.3,leading=18,textColor=PUR,backColor=PALE,borderPadding=14,spaceAfter=11),
}
def P(t,style='p'):return Paragraph(t,ST[style])
def tbl(rows,colWidths=None,header=True):
 t=Table([[P(str(c),'small') for c in row] for row in rows],colWidths=colWidths,repeatRows=1 if header else 0,hAlign='LEFT')
 cmd=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),.42,colors.HexColor('#d3cbd6')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]
 if header:cmd.extend([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#ede4ee')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#faf8fc')])]);
 t.setStyle(TableStyle(cmd));return t

def page_frame(c,doc,tag='ORGANIZATOR'):
 w,h=A4
 c.saveState();c.setStrokeColor(GOLD);c.setLineWidth(.7);c.line(MARGIN,h-34,w-MARGIN,h-34)
 c.setFont('DV-B',7);c.setFillColor(PUR);c.drawString(MARGIN,h-24,'KLĄTWA SIEDMIU ŚWIATÓW')
 c.setFont('DV',7);c.drawRightString(w-MARGIN,h-24,tag)
 c.setFillColor(GREY);c.drawRightString(w-MARGIN,23,f'Strona {doc.page}')
 c.restoreState()

class ResistDiagram(Flowable):
 def __init__(self):super().__init__();self.width=482;self.height=95
 def draw(self):
  c=self.canv;c.saveState();c.setStrokeColor(colors.HexColor('#515166'));c.setLineWidth(3);c.line(35,49,450,49)
  c.setFillColor(colors.HexColor('#dbc399'));c.setStrokeColor(colors.HexColor('#7f623e'));c.roundRect(104,28,265,44,16,stroke=1,fill=1)
  for x,cl in [(156,'#96501d'),(214,'#111111'),(271,'#d83930'),(335,'#d1ae39')]:c.setFillColor(colors.HexColor(cl));c.rect(x,29,13,42,fill=1,stroke=0)
  c.setFillColor(PUR);c.setFont('DV-B',9)
  for x,label in [(162,'1'),(220,'2'),(277,'3'),(341,'4')]:c.drawCentredString(x,12,label)
  c.setFont('DV',9);c.drawCentredString(244,80,'Czwarty pasek (tolerancja) pomijamy!');c.restoreState()

# AUTHORITATIVE GUIDE
G=[]
def h(t):G.append(P(t,'h1'))
def hh(t):G.append(P(t,'h2'))
def p(t):G.append(P(t))
def quote(t):G.append(P(t,'quote'))
def gap(n=7):G.append(Spacer(1,n))
def breakp():G.append(PageBreak())
G += [Spacer(1,72),P('KLĄTWA<br/>SIEDMIU ŚWIATÓW','splash'),P('JEDNA INSTRUKCJA DLA MISTRZA GRY','center'),Spacer(1,25),P('Siedem światów · dwoje dzieci · dwa tablety · 60 puzzli · jedna skrzynia','center'),Spacer(1,30),P('WERSJA ZAKTUALIZOWANA — 29 PAŹDZIERNIKA 2026','center')]
quote('TEN DOKUMENT ZAWIERA WSZYSTKIE ROZWIĄZANIA. Nie pokazuj go Zosi ani Emilce. Wszystkie karty, pieczęcie, rysunki i instrukcje do wycinania znajdują się w osobnym pliku „Materialy_do_druku.pdf”.')
p('Ważne: źródłem prawdy są aktualne etapy aplikacji i ostatnie ustalenia. Starsze, rozproszone PDF-y mają nieaktualne fragmenty. W tej wersji zebrano przygotowanie wszystkich siedmiu światów w jednym miejscu.')
breakp()
h('00 · Przygotowania ogólne i uruchomienie')
hh('Sprzęt i rzeczy do zebrania')
p('Laptop z Ubuntu i Pythonem 3, domowe Wi-Fi, dwa tablety (Strażniczka I = Zosia, Strażniczka II = Emilka), ładowarki, czołówki, nożyczki, taśma papierowa, sześć kopert na pieczęcie, sześć MAŁYCH kopert na rezystory, długopis z tuszem UV i latarką UV, lustro, sześć książek z co najmniej 50 stronami, mikroskop z oświetleniem, jeden silnik DC 3–6 V z osłoną, zasilacz 5 V, opcjonalny wyłącznik, cztery wymienne tarcze 10 cm, taśma klejąca, stroboskop, Arduino UNO z Enigmą, czterocyfrowa kłódka oraz skrzynia.')
p('Materiały: wydrukowane karty i pieczęcie; <b>gotowe, prawdziwe puzzle składające się z dokładnie 60 elementów</b> (jeden komplet, nie kilka zestawów); dwie sztywne, płaskie tektury lub deski do odwracania układanki; długopis UV i latarka UV; skrzynia z czterocyfrową kłódką; słodycze i dyplomy.')
hh('Zasilanie i bezpieczeństwo')
p('Elektronikę montuje dorosły i kontroluje przy odłączonym zasilaniu. Nie używaj napięcia sieciowego na odsłoniętych przewodach. W eksperymencie ze stroboskopem nie kieruj błysków w oczy; przy nadwrażliwości na światło stosuj wariant bez stroboskopu. Ruchome tarcze osłoń. Mikroskop, UV i małe rezystory używaj pod nadzorem; nie świeć UV w oczy i nie pozwalaj wkładać drobnych elementów do ust. Nie chowaj kopert przy gniazdkach ani ostrych narzędziach.')
hh('Zanim przyjdą Strażniczki')
p('1. Na laptopie zatrzymaj działający serwer (Ctrl+C), wykonaj <b>git pull</b>, następnie <b>python3 server.py</b>.\n<br/>2. Ustal adres IP laptopa poleceniem <b>hostname -I</b>; na tabletach otwórz <b>http://ADRES_IP:8000</b>. Każda wybiera inny numer Strażniczki.\n<br/>3. Przeprowadź próbę obu tabletów; sprawdź, czy postęp jest zsynchronizowany.\n<br/>4. Jeśli była rozgrywka testowa, uruchom <b>python3 reset.py</b> przy działającym serwerze. Uwaga: reset usuwa WSZYSTKIE dane poprzedniej gry — nie używaj go w środku przygody.\n<br/>5. Przygotuj zegar 120 minut; aplikacja odmierza czas od wspólnej przysięgi i zatrzymuje wynik po wpisaniu magicznego słowa na obu tabletach. Co 10 minut Morthar może wyświetlać klimatyczną wiadomość, którą dzieci zamykają jednym przyciskiem.')
hh('Prawdziwe puzzle: 60 elementów, nie papierowe wycinanki')
p('Przygotuj <b>jeden gotowy zestaw dokładnie 60 prawdziwych puzzli</b>. Ułóż cały obrazek na sztywnej, płaskiej podkładce. Sprawdź na jednym elemencie, czy tusz UV dobrze przylega do rewersu i jest czytelny po wyschnięciu. Drugą tekturą przykryj obraz, ściśnij je i ostrożnie obróć całość, żeby ułożone elementy nie rozsypały się. Na odsłoniętym odwrocie napisz dużymi literami zagadkę o Kasprowym Wierchu (treść w Świecie VII). Nie zapisuj na puzzlach gotowego kodu 1987.')
p('Nie rozłączając układanki, obejrzyj napis pod latarką UV: powinien być czytelny <b>dopiero po połączeniu wielu elementów</b>. Pozostaw tusz do całkowitego wyschnięcia, a następnie delikatnie rozdziel puzzle. Wymieszaj 60 kawałków i podziel na <b>6 równych paczek po 10</b>. Do kopert I–VI włóż po jednej paczce i pieczęć danego świata. Na finał pozostaw obie tektury: dziewczynki ułożą obrazek, odwrócą go wspólnie i odczytają zagadkę UV.')
breakp()
h('01 · SALON — Krypta Sześciu Bestii')
hh('Przygotuj i rozłóż')
p('Wydrukuj arkusz z sześcioma bestiami i wytnij karty: Wampir 7, Wilkołak 2, Mumia 9, Wiedźma 4, Duch 1, Kościotrup 6. Każda ma mieć swoją cyfrę na TEJ SAMEJ stronie co rysunek. Schowaj karty osobno w sześciu bezpiecznych miejscach salonu; ich kolejność odnajdywania NIE może zdradzać kodu.')
p('Kopertę <b>I</b> z pieczęcią <b>KRUK-583</b> i dziesięcioma puzzlami schowaj w ciemnej szczelinie kanapy, od boku lub od spodu (tam, gdzie dziecko może bezpiecznie sięgnąć). Aplikacja sugeruje ciemne zakamarki kanapy, a nie wygodne siedzisko. Nie chowaj przy ostrych elementach stelaża.')
hh('Przebieg i odpowiedź — tylko dla dorosłego')
p('Zosia odnajduje karty i zaznacza je na tablecie; Emilka przypisuje cyfry. Dwie bestie do odrzucenia: <b>Wiedźma i Kościotrup</b>. Kolejność czterech prawdziwych: <b>Wampir → Wilkołak → Duch → Mumia</b>. Wspólny kod: <b>7219</b>. Następnie obie odnajdują kopertę, odczytują i wpisują <b>KRUK-583</b>.')
hh('Przed grą sprawdź')
p('□ Sześć kart jest wydrukowanych i rozłożonych. □ Numery na kartach zgadzają się. □ Koperta I z pieczęcią i 10 puzzlami jest ukryta. □ Nie pokazujesz dzieciom niniejszych odpowiedzi.')
breakp()
h('02 · SYPIALNIA — Galeria Lustrzanych Szeptów')
hh('Przygotuj i rozłóż')
p('Przygotuj prawdziwe lustro i trzy wydrukowane, lustrzane kartki. Kartę I (NOC) włóż <b>do szuflady komody</b>; kartę II (MA) schowaj <b>pod łóżkiem</b>; kartę III (OCZY) <b>za roletą okienną opuszczaną łańcuszkiem</b>. Nie pisz zwykłych słów po drugiej stronie kartek. Upewnij się, że z dziećmi da się bezpiecznie dosięgnąć trzeciej kryjówki.')
p('Kopertę <b>II</b> z pieczęcią <b>LUSTRO-426</b> i 10 puzzlami włóż <b>do bidonu przy trenażerze rowerowym</b>. Bidon ma być czysty i suchy; nie dodawaj wody.')
hh('Przebieg i odpowiedź')
p('Zosia dostaje trzy zagadki o ukryciu kartek. Emilka sugeruje użycie lustra. Z odnalezionych napisów tworzą hasło <b>NOC MA OCZY</b>. Potem rozwiązują zagadkę podróżnika, który pedałuje, lecz nie przemieszcza się — trenażer rowerowy. Obie wpisują kod pieczęci <b>LUSTRO-426</b>.')
p('□ Lustro jest w zasięgu dzieci. □ Napisy rzeczywiście czytają się poprawnie w odbiciu. □ Bidon i koperta są suche. □ W kopercie II jest 10 puzzli.')
breakp()
h('03 · KUCHNIA — Laboratorium Doktora Morse’a')
hh('Rzeczy na stanowisku')
p('Arduino UNO z wgranym plikiem <b>Enigma_Doktora_Morsea.ino</b>; matryca LED MAX7219 8×32; klawiatura 4×4 o przyciskach S1–S16; płytka stykowa i przewody; LED niebieska i zielona; <b>dwa rezystory 330 Ω</b> (nie mylić z rezystorami Świata VI); odpowiedni zasilacz USB 5 V albo bateria 9 V z wtykiem DC tylko po wcześniejszej próbie. Przygotuj 7 oznaczonych stanowisk / etykiet do montażu, dziecięcą instrukcję obrazkową, tabelę obsługi klawiatury i ołówek. Wszystkie łączenia weryfikuje dorosły.')
hh('Najważniejsze przewody Arduino UNO')
G.append(tbl([['MAX7219 (strona IN)','Arduino UNO'],['VCC','5V'],['GND','GND'],['DIN','D11'],['CS','D10'],['CLK','D13']], [230,275]))
gap(8)
G.append(tbl([['Klawiatura','Arduino UNO','Klawiatura','Arduino UNO'],['C4','D2','R1','D6'],['C3','D3','R2','D7'],['C2','D4','R3','D8'],['C1','D5','R4','D9']], [135,110,135,125]))
gap(7)
p('Dioda niebieska: A0 → rezystor 330 Ω → anoda LED, katoda → GND. Dioda zielona: A1 → osobny rezystor 330 Ω → anoda, katoda → GND. Nie łącz 9 V bezpośrednio z pinem 5V. Po sprawdzeniu połączeń użyj sprawdzonego sposobu zasilania; baterie typu 9 V mogą szybko tracić wydajność, dlatego przed imprezą sprawdź cały cykl transmisji.')
hh('Misja i tajne rozwiązanie')
p('Niebieska LED świeci 5 sekund na początku; zielona nada zagadkę alfabetem Morse’a. Jej odpowiedź to <b>WIATR</b>. Klucz starego telefonu: W=9, I=4, A=2, T=8, R=7, czyli kod klawiatury <b>94287</b>, potwierdź S12. Na wyświetlaczu pokaże się <b>BURZA</b>. Obie wpisują BURZA na tabletach.')
p('Koperta <b>III</b> z pieczęcią <b>ISKRA-731</b> i 10 puzzlami spoczywa <b>przy doniczce rośliny na parapecie</b>, w suchym zabezpieczonym woreczku lub przy zewnętrznej ściance. Nie zakopuj głęboko i nie uszkadzaj korzeni.')
p('□ Wgraj skecz, wykonaj test wszystkich klawiszy. □ Sprawdź osobno niebieską i zieloną diodę. □ Przetestuj całą wiadomość Morse’a i kod 94287. □ Koperta III zawiera 10 puzzli i pieczęć.')
breakp()
h('04 · GABINET — Mechanizm Zatrzymanego Czasu')
hh('Ustaw urządzenie wcześniej')
p('Przygotuj <b>jeden osłonięty silnik 3–6 V zasilany bezpośrednio z 5 V</b> i cztery wymienne tarcze o średnicy 10 cm. Wytnij symbole z arkusza i <b>przyklej po jednym na odwrocie właściwej tarczy</b>: <b>KSIĘŻYC = 7</b>, <b>KRUK = 2</b>, <b>KLUCZ = 9</b>, <b>KLEPSYDRA = 4</b>. Drukuj w skali 100%. Tarcze muszą być wyważone i pewnie zamocowane taśmą. Przed każdą wymianą wyłącz zasilanie i poczekaj na całkowite zatrzymanie.')
p('Silnik został sprawdzony z bezpośrednim zasilaniem <b>5 V</b>. W Świecie IV <b>nie używamy NodeMCU ani L298N</b>. Proste połączenie: <b>+5 V zasilacza → [opcjonalny wyłącznik] → + silnika; – silnika → GND zasilacza</b>. Użyj zasilacza 5 V o wydajności prądowej wystarczającej również podczas rozruchu oraz wyłącznika o odpowiednich parametrach. Przewody zabezpiecz przed zwarciem. Bez wyłącznika dorosły odłącza zasilanie przed każdą wymianą.')
hh('Zagadki i wynik')
p('Strażniczka I wybiera tarczę, <b>sprawdza symbol na odwrocie</b>, a dorosły mocuje ją taśmą na nieruchomym silniku i zamyka osłonę. Po uruchomieniu odczytują cyfrę stroboskopem, zapisują parę symbol–cyfra, wyłączają silnik i <b>czekają na pełne zatrzymanie przed wymianą tarczy</b>. Powtarzają to dla czterech tarcz. Strażniczka II układa symbole według wskazówek w aplikacji: <b>KSIĘŻYC → KRUK → KLUCZ → KLEPSYDRA</b>; kod <b>7294</b>. Kolejność wymiany tarcz nie ma znaczenia.')
p('Kopertę <b>IV</b> z pieczęcią <b>CZAS-604</b> i 10 puzzlami schowaj <b>w szufladzie biurka w gabinecie</b>. Jeżeli zabawa stroboskopem jest niewskazana, dorosły powinien przygotować bezpieczny zastępczy sposób ujawnienia tych samych cyfr. Nie kieruj błysków w oczy.')
p('□ Jeden silnik pracuje bezpośrednio z 5 V (bez MCU), z osłoną. □ Opcjonalny wyłącznik sprawdzony. □ Cztery tarcze i symbole na odwrotach gotowe. □ Taśma mocująca, wyłączanie i pełne zatrzymanie przed wymianą sprawdzone. □ Stroboskop przetestowany. □ Koperta IV z 10 puzzlami w szufladzie.')
breakp()
h('05 · POKÓJ EMILKI — Biblioteka Zapomnianych Imion')
p('Przygotuj sześć książek liczących co najmniej 50 stron. Każdą oznacz papierowym symbolem z drugiego PDF-u. Na stronie prawdziwej napisz UV właściwą literę (lub „NA”); na fałszywej — mylący znak. Nie odsłaniaj imienia Morweny przed rozwiązaniem.')
G.append(tbl([['Symbol','Gdzie ukryć książkę','Strona UV','Fałszywa strona UV'],['KSIĘŻYC','Regał między książkami','24 → M','11 → X'],['KRUK','Szuflada biurka','36 → O','13 → P'],['KLUCZ','Za monitorem komputera','18 → R','31 → T'],['PAJĄK','Pod kaloryferem','42 → W','16 → A'],['WĄŻ','Pojemnik z klockami LEGO','27 → E','39 → K'],['ŚWIECA','POD PODUSZKĄ łóżka','15 → NA','28 → S']], [88,191,106,120]));gap(8)
hh('Odłóż UV na właściwy moment')
p('Długopis z lampką UV schowaj <b>w piórniku znajdującym się w szufladzie biurka</b>, oddzielnie od księgi KRUK. Najlepiej tak, by podczas wyjmowania książki nie było go od razu widać. Aplikacja ujawni trzyetapową wskazówkę dopiero po odnalezieniu ksiąg i ustaleniu stron.')
hh('Kontrola sześciu zagadek stron')
p('KSIĘŻYC: XII + XII = 24. KRUK: Morse ...-- / -.... = 36. KLUCZ: C+F+I = 3+6+9 = 18. PAJĄK: 5×8 − 2 + 4 = 42. WĄŻ: odwróć cyfry 72 → 27. ŚWIECA: pięć lamp 16,8,4,2,1 i kod 01111 daje 8+4+2+1 = 15.')
p('Kolejność książek: KSIĘŻYC, KRUK, KLUCZ, PAJĄK, WĄŻ, ŚWIECA. UV da odpowiednio <b>M + O + R + W + E + NA = MORWENA</b>. Dopiero po wpisaniu imienia obie dziewczynki szukają koperty <b>V</b> schowanej <b>wewnątrz policyjnej wyspy z klocków LEGO na regale</b>. W kopercie: pieczęć <b>MROK-852</b> i 10 puzzli.')
p('□ Świeca na pewno POD PODUSZKĄ, nie na regale. □ 12 napisów UV na właściwych stronach. □ Długopis UV pozostaje oddzielony od księgi KRUK. □ Policja LEGO zawiera tylko kopertę, nie książki.')
breakp()
h('06 · POKÓJ ZOSI — Laboratorium Profesora Volta')
p('Przygotuj sześć małych kopert, po jednym rezystorze <b>czteropaskowym</b> w każdej. Na zewnątrz każdej koperty napisz atramentem UV TYLKO jedną przypisaną literę. Nie dopisuj wartości oporności. Rozsyp/ukryj koperty w pokoju Zosi bez zagadek kryjówek. Opcjonalne błyskawice UV mogą naprowadzać na ukryte koperty. Długopis UV pochodzi ze Świata V.')
G.append(tbl([['Oporność','Pierwsze trzy paski','Litera UV'],['10 Ω','brązowy / czarny / czarny','P'],['22 kΩ','czerwony / czerwony / pomarańczowy','R'],['100 kΩ','brązowy / czarny / żółty','Ą'],['220 kΩ','czerwony / czerwony / żółty','D'],['470 kΩ','żółty / fioletowy / żółty','E'],['550 kΩ','zielony / zielony / żółty','M']], [113,285,107]));gap(6)
p('<b>Uwaga dla dorosłego:</b> 550 kΩ nie jest najczęstszą wartością w typowych zestawach. Przed grą obejrzyj jego paski: zielony – zielony – żółty dla czteropaskowego oznaczenia 550 kΩ. Jeśli jest inny, sprawdź miernikiem lub zamień element, ale wtedy zaktualizuj tę mapę. Czwarty pasek to tolerancja i nie uczestniczy w obliczeniach.')
p('Pod mikroskopem dzieci odczytują pierwsze trzy paski; obliczają oporność i sortują od najmniejszej do największej. Hasło: <b>PRĄDEM</b>. Przygotuj jasną kartkę i ewentualną masę mocującą, żeby rezystor nie uciekał spod mikroskopu. Dzieci nie podłączają ich do zasilania.')
p('Kopertę <b>VI</b> z pieczęcią <b>ISKRA-906</b> i 10 puzzlami ukryj <b>WE WNĘTRZU ŁÓŻKA ZOSI</b>. To osobna koperta — NIE jedna z sześciu kopert rezystorowych. Po wpisaniu hasła aplikacja ujawni miejsce.')
p('□ 6 rezystorów, 6 kopert, 6 prawidłowych liter UV. □ Mikroskop wyostrzony. □ Wyczytelne paski. □ Pieczęć VI z 10 puzzlami we wnętrzu łóżka.')
breakp()
h('07 · GARDEROBA — Komnata Cienia i finał')
hh('Przygotowanie skrzyni')
p('W garderobie / wybranej finałowej komnacie postaw skrzynię z <b>czterocyfrową kłódką ustawioną na 1987</b>. Zawartość skrzyni: <b>wydrukowany list Morthara</b>, <b>kartka z magicznym słowem WOLNOŚĆ</b>, coś słodkiego dla każdej dziewczynki oraz opcjonalnie siódma pieczęć i dyplomy. Nie ujawniaj słowa ani cyfr przed otwarciem skrzyni.')
hh('Jak przygotować rewers 60 puzzli')
quote('Tekst do napisania długopisem UV na odwrocie W CAŁOŚCI UŁOŻONYCH, PRAWDZIWYCH puzzli: „MORTHAR UKRYŁ SIĘ NA KASPROWYM WIERCHU. WYSOKOŚĆ TEGO SZCZYTU W METRACH NAD POZIOMEM MORZA TO CZTERY CYFRY OTWIERAJĄCE SKRZYNIĘ”.')
p('Zapisuj treść przez <b>granice stykających się puzzli</b>, a nie osobno na każdym kawałku. Nie przyklejaj puzzli na stałe i nie zasłaniaj ich łączeń. Jeśli odwrotna strona jest ciemna lub śliska, przetestuj najpierw jeden element i dobierz widoczny pod UV pisak; nie naklejaj papieru, który utrudni dopasowanie części. Napis ma wyschnąć przed rozdzieleniem 60 elementów na sześć kopert. W czasie finału dziewczynki same złożą obraz, odwrócą go między dwiema tekturami i oświetlą tył UV.')
hh('Ostatnie pięć kroków')
p('1. Po 6. pieczęci aplikacja wysyła do Komnaty Cienia.\n<br/>2. Dziewczynki układają 60 puzzli, odwracają i czytają zagadkę UV.\n<br/>3. Ustalają wysokość Kasprowego Wierchu: <b>1987 m n.p.m.</b> — kod kłódki <b>1987</b>. Nie wpisuje się go do aplikacji.\n<br/>4. Otwierają skrzynię, znajdują list Morthara, słodycze i kartkę ze słowem <b>WOLNOŚĆ</b>. Wypowiadają je i wpisują na obu tabletach.\n<br/>5. Gdy obie wpiszą poprawne słowo, zegar zatrzymuje się, pojawia się animowane zwycięstwo i dokładny czas ukończenia. Wręcz dyplomy.')
p('□ Kłódka otwiera się kodem 1987. □ List, kartka WOLNOŚĆ i słodycze znajdują się wewnątrz. □ Zestaw naprawdę ma 60 elementów. □ Napis UV jest czytelny i suchy. □ Dwie sztywne tektury pozwalają odwrócić ułożone puzzle bez rozsypania.')
breakp()
h('LISTA OSTATECZNA · przed wpuszczeniem dzieci')
G.append(tbl([['Sprawdź','Stan'],['Dwa tablety + Wi-Fi + zsynchronizowany serwer','□'],['Przygotowane stanowiska, sprzęt i zasilanie','□'],['Sześć kart bestii w salonie','□'],['Trzy lustrzane kartki w sypialni','□'],['Działająca Enigma Morse’a w kuchni','□'],['Jeden silnik 5 V + cztery tarcze, taśma i osłona','□'],['Sześć ksiąg UV + długopis w piórniku','□'],['Sześć kopert rezystorów + mikroskop','□'],['Sześć kopert I–VI zawiera pieczęć i 10 puzzli','□'],['Skrzynia z kłódką 1987, listem, WOLNOŚĆ i nagrodami','□'],['Wszystkie 60 puzzli mają jedną wspólną wiadomość UV','□'],['Stare testowe dane gry zresetowano PRZED startem','□']], [435,70]));gap(10)
quote('OSTATNIA PRÓBA: uruchom obu Strażniczek w trybie testowym i sprawdź fizycznie wszystkie kryjówki, kody, rewers UV, jakość mikroskopu i działanie zamka. Nie resetuj ani nie zmieniaj materiałów, gdy dzieci już grają.')
p('Uwaga: w Świecie IV silnik jest zasilany bezpośrednio z 5 V i nie wymaga mikrokontrolera. Arduino UNO pozostaje potrzebne wyłącznie w Świecie III. Ustalony komplet 60 puzzli i finał WOLNOŚĆ zastępują dawne warianty zakończenia. Sam dokument nie potwierdza, czy fizyczne układy są już poprawnie zmontowane — wymagana jest próba sprzętowa.')

def build_guide(dst):
 doc=SimpleDocTemplate(str(dst),pagesize=A4,rightMargin=MARGIN,leftMargin=MARGIN,topMargin=47,bottomMargin=44,title='Klątwa Siedmiu Światów - instrukcja organizatora',author='Instrukcja gry domowej')
 doc.build(G,onFirstPage=lambda c,d:page_frame(c,d),onLaterPages=lambda c,d:page_frame(c,d))
 return dst

# CUSTOM HANDOUT/PRINT PAGES, independently printable
class PrintSeal(Flowable):
 def __init__(self,roman,title,code):super().__init__();self.width=480;self.height=345;self.roman=roman;self.title=title;self.code=code
 def draw(self):
  c=self.canv;c.saveState();c.setStrokeColor(GOLD);c.setLineWidth(2);c.roundRect(14,12,452,317,20)
  c.setStrokeColor(PUR);c.setLineWidth(1);c.roundRect(25,23,430,295,15)
  c.setFillColor(PUR);c.setFont('DVS-B',40);c.drawCentredString(240,245,self.roman)
  c.setFont('DV-B',18);c.drawCentredString(240,198,'PIECZĘĆ ZWYCIĘSTWA')
  c.setFont('DV-B',11);c.drawCentredString(240,160,self.title)
  c.setFont('DVS-B',22);c.drawCentredString(240,104,self.code)
  c.setFont('DV',9);c.drawCentredString(240,58,'ZACHOWAJ DO KOŃCA GRY');c.restoreState()


# Świat IV: tarcze 7, 4 i 2B są kopiowane bez skalowania z nowego
# źródła w katalogu głównym. Dziewiątka jest odtworzona z wektorowych
# współrzędnych sprawdzonej tarczy 6-sektorowej (bez starego wzoru 12×9).
def build_world4_discs():
 source=fitz.open(locate('discs'))
 if len(source)<2:raise ValueError('Nowy plik tarcz musi mieć co najmniej 2 strony')
 output=fitz.open()
 cx=184.252; upper=243.7795; lower=583.937
 radius=50*mm
 def label(page,x,y,text,size=9,bold=False):
  fontname='dvbold' if bold else 'dvregular'
  fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
  page.insert_font(fontname=fontname,fontfile=fontfile)
  page.insert_text((x,y),text,fontname=fontname,fontsize=size,color=(.16,.15,.22))
 for page_number in range(2):
  page=output.new_page(width=A4[0],height=A4[1])
  label(page,44,40,'ŚWIAT IV — WYMIENNE TARCZE ZEGARMISTRZA',14,True)
  label(page,44,61,'Jedna tarcza na raz • wytnij po obwodzie • wydruk 100%',9)
  for row in range(2):
   if page_number==1 and row==1:continue
   source_row=row if page_number==0 else 1
   source_y=(upper,lower)[source_row]
   target_y=(upper,lower)[row]
   clip=fitz.Rect(cx-radius-2,source_y-radius-2,cx+radius+2,source_y+radius+2)
   target=fitz.Rect(cx-radius-2,target_y-radius-2,cx+radius+2,target_y+radius+2)
   page.show_pdf_page(target,source,page_number,clip=clip)
  # Wyraźna linia cięcia o średnicy 10 cm dla każdej tarczy.
  for center_y in (upper,lower):
   page.draw_circle((cx,center_y),radius-1.1,color=(0,0,0),width=2.2)
  if page_number==1:
   # Cyfra 9: dokładne końce sześciu kresek działającej tarczy,
   # przeliczone z pierwszego na dolny środek strony.
   page.draw_circle((cx,lower),radius,color=(0,0,0),width=.27)
   page.draw_circle((cx,lower),1.4*mm,color=(0,0,0),width=.45)
   nine_segments=[
    ((197.2913,126.1418),(171.2126,126.1418)),
    ((276.4081,173.2253),(262.4153,181.3042)),
    ((273.0201,277.6821),(259.0274,269.6034)),
    ((171.2126,318.8976),(197.2913,318.8976)),
    ((77.0722,288.3120),(91.0650,280.2333)),
    ((107.3059,184.2982),(94.2665,206.8830)),
   ]
   shift=lower-upper
   for a,b in nine_segments:
    page.draw_line((a[0],a[1]+shift),(b[0],b[1]+shift),color=(0,0,0),width=6.5197,lineCap=1)
  labels=(
   [('7','KSIĘŻYC','2 fragmenty co 180°'),('4','KLEPSYDRA','3 fragmenty co 120°')]
   if page_number==0 else
   [('2 (wariant B)','KRUK','5 fragmentów co 72°'),('9','KLUCZ','6 fragmentów co 60°')]
  )
  for row,(digit,symbol,detail) in enumerate(labels):
   y=(upper,lower)[row]
   label(page,344,y-24,'CYFRA '+digit,12,True)
   label(page,344,y,'SYMBOL: '+symbol,9)
   label(page,344,y+20,detail,8)
   label(page,344,y+44,'Symbol naklej na odwrocie.',7.5)
  page.draw_line((44,791),(44+50*mm,791),color=(0,0,0),width=1)
  label(page,44,806,'50 mm — kontrola skali',8)
  label(page,44,824,'Tarczę wymienia dorosły przy wyłączonym silniku.',7)
 path=OUT/'_world4_discs.pdf'
 output.save(str(path),garbage=4,deflate=True)
 output.close();source.close()
 return path

def build_world4_symbols():
 source=fitz.open(locate('symbols4'))
 output=fitz.open()
 output.insert_pdf(source,from_page=0,to_page=0)
 source.close()
 page=output[0]
 page.add_redact_annot(fitz.Rect(45,655,560,792),fill=(1,1,1))
 page.apply_redactions(images=0,graphics=0,text=0)
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
 page.insert_font(fontname='dv',fontfile=font)
 page.insert_font(fontname='dvbold',fontfile=bold)
 page.insert_text((54,681),'JAK PRZYGOTOWAĆ TARCZE?',fontname='dvbold',fontsize=11,color=(.25,.18,.32))
 for y,line in [
  (705,'1. Wytnij cztery symbole i przyklej każdy na ODWROCIE właściwej tarczy.'),
  (724,'2. Wytnij same symbole z nazwami; nie naklejaj całych dużych ramek.'),
  (743,'3. Przed zamontowaniem sprawdź symbol; po odczycie zapisz symbol i cyfrę.'),
  (762,'4. Wymieniaj tarcze wyłącznie po wyłączeniu i zatrzymaniu silnika.'),
  (784,'Symbole nie określają kolejności kodu — rozstrzyga zagadka na tablecie.')
 ]:page.insert_text((54,y),line,fontname='dv',fontsize=8.2,color=(.22,.18,.27))
 path=OUT/'_world4_symbols.pdf'
 output.save(str(path),garbage=4,deflate=True)
 output.close()
 return path

# Jedna lista nazw na tabliczki drzwi i etykiety kopert.
WORLD_TITLES = [
 ('I', 'KRYPTA SZEŚCIU BESTII'),
 ('II', 'GALERIA LUSTRZANYCH SZEPTÓW'),
 ('III', 'LABORATORIUM DOKTORA MORSE’A'),
 ('IV', 'MECHANIZM ZATRZYMANEGO CZASU'),
 ('V', 'BIBLIOTEKA ZAPOMNIANYCH IMION'),
 ('VI', 'LABORATORIUM PROFESORA VOLTA'),
 ('VII', 'KOMNATA CIENIA'),
]

def cutout_table(rows, heights):
 t=Table(rows,colWidths=[250,250],rowHeights=heights,hAlign='CENTER')
 t.setStyle(TableStyle([
  ('GRID',(0,0),(-1,-1),3.2,PUR),
  ('BOX',(0,0),(-1,-1),3.2,PUR),
  ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fcf8fd')),
  ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ('LEFTPADDING',(0,0),(-1,-1),12),
  ('RIGHTPADDING',(0,0),(-1,-1),12),
 ]))
 return t

def build_handouts(dst):
 def textpage(filename,parts,tag='DO WYDRUKU'):
  arr=[]
  for typ,t in parts:
   if typ=='title':arr.append(P(t,'title'))
   elif typ=='subtitle':arr.append(P(t,'subtitle'))
   elif typ=='h1':arr.append(P(t,'h1'))
   elif typ=='h2':arr.append(P(t,'h2'))
   elif typ=='quote':arr.append(P(t,'quote'))
   elif typ=='p':arr.append(P(t,'p'))
   elif typ=='seal7':arr.append(PrintSeal('VII','KOMNATA CIENIA','CZAS UWOLNIONY'))
   elif typ=='seal_custom':arr.append(PrintSeal(*t))
   elif typ=='diagram':arr.append(ResistDiagram())
   elif typ=='table':arr.append(t)
   elif typ=='spacer':arr.append(Spacer(1,int(t)))
   elif typ=='pagebreak':arr.append(PageBreak())
  dest=OUT/('_'+filename+'.pdf')
  SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=MARGIN,leftMargin=MARGIN,topMargin=47,bottomMargin=44).build(arr,onFirstPage=lambda c,d:page_frame(c,d,tag),onLaterPages=lambda c,d:page_frame(c,d,tag))
  return dest

 # Etykiety kopert: nazwy światów, bez nazw pomieszczeń.
 envelope_style=ParagraphStyle('EnvelopeLabel',fontName='DV-B',fontSize=12.5,
     leading=20,alignment=TA_CENTER,textColor=PUR)
 door_style=ParagraphStyle('DoorLabel',fontName='DVS-B',fontSize=15,
     leading=24,alignment=TA_CENTER,textColor=PUR)
 def envelope_cell(roman,title):
  return Paragraph('KOPERTA '+roman+'<br/><br/>'+title,envelope_style)
 def door_cell(roman,title):
  return Paragraph('<font size="28">ŚWIAT '+roman+'</font><br/><br/>'+title,door_style)
 envelope_rows=[[envelope_cell(*WORLD_TITLES[i]),envelope_cell(*WORLD_TITLES[i+1])]
                for i in (0,2,4)]
 labels=textpage('labels',[
   ('title','ETYKIETY KOPERT — NAZWY ŚWIATÓW'),
   ('subtitle','Wytnij sześć etykiet i naklej na koperty z pieczęciami i puzzlami.'),
   ('table',cutout_table(envelope_rows,[130]*3)),
   ('spacer','12'),
   ('p','Do każdej koperty włóż pieczęć i dokładnie 10 prawdziwych puzzli. Sześć małych kopert z rezystorami oznaczaj wyłącznie tuszem UV.'),
 ])
 # Siedem dużych tabliczek na drzwi: 4 na pierwszej stronie, 3 na drugiej.
 door_cards=[door_cell(*item) for item in WORLD_TITLES]
 room_labels=textpage('room_labels',[
   ('title','TABLICZKI NA DRZWI — SIEDEM ŚWIATÓW'),
   ('subtitle','Wytnij i przyklej na wejściach do właściwych pomieszczeń.'),
   ('table',cutout_table([[door_cards[0],door_cards[1]],[door_cards[2],door_cards[3]]],[270,270])),
   ('pagebreak',''),
   ('title','TABLICZKI NA DRZWI — SIEDEM ŚWIATÓW'),
   ('subtitle','Drugi arkusz: światy V–VII.'),
   ('table',cutout_table([[door_cards[4],door_cards[5]],[door_cards[6],'']],[270,270])),
 ])
 # Children get the keypad legend on tablets. Print only physical component labels.
 station_names=[
    '1 · ARDUINO UNO\\nMÓZG MASZYNY',
    '2 · WYŚWIETLACZ LED 8 × 32',
    '3 · KLAWIATURA S1–S16',
    '4 · NIEBIESKA DIODA LED\\n+ REZYSTOR 330 Ω',
    '5 · ZIELONA DIODA LED\\n+ REZYSTOR 330 Ω',
    '6 · PŁYTKA STYKOWA\\nI PRZEWODY',
    '7 · ZASILANIE\\nPODŁĄCZA DOROSŁY'
 ]
 station_cells=[]
 for i in range(0,8,2):
     station_cells.append([P(station_names[j].replace('\\n','<br/>'),'center') if j<len(station_names) else '' for j in (i,i+1)])
 station_table=Table(station_cells,colWidths=[250,250],rowHeights=[108]*4,hAlign='LEFT')
 station_table.setStyle(TableStyle([
     ('GRID',(0,0),(-1,-1),1.5,GOLD),
     ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fcf8f3')),
     ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
     ('LEFTPADDING',(0,0),(-1,-1),12),
     ('RIGHTPADDING',(0,0),(-1,-1),12),
 ]))
 stations=textpage('enigma_stations',[
     ('title','ENIGMA DOKTORA MORSE’A'),
     ('subtitle','Siedem etykiet do wycięcia i rozłożenia obok części urządzenia.'),
     ('table',station_table),
 ])
 seven=textpage('seal7',[
 ('title','OSTATNIA PIECZĘĆ'),('subtitle','Jeśli chcesz, włóż ją do skrzyni obok listu Morthara, kartki z zaklęciem i słodyczy.'),('seal7','')])


 def seal_sheet(number,roman,title,code):
  return textpage('seal_'+str(number),[('title','PIECZĘĆ '+roman+' — '+title),('subtitle','Wytnij ozdobną kartę. Włóż do koperty świata '+str(number)+' razem z DOKŁADNIE 10 puzzlami.'),('seal_custom',(roman,title,code))])

 # Open all inputs: key assets, write handwritten cards as supplementary pages
 seals={
  1:seal_sheet(1,'I','KRYPTA SZEŚCIU BESTII','KRUK-583'),
  2:seal_sheet(2,'II','GALERIA LUSTRZANYCH SZEPTÓW','LUSTRO-426'),
  3:seal_sheet(3,'III','LABORATORIUM DOKTORA MORSE’A','ISKRA-731'),
  4:seal_sheet(4,'IV','MECHANIZM ZATRZYMANEGO CZASU','CZAS-604'),
  5:seal_sheet(5,'V','BIBLIOTEKA ZAPOMNIANYCH IMION','MROK-852'),
  6:seal_sheet(6,'VI','LABORATORIUM PROFESORA VOLTA','ISKRA-906')
 }
 # Two corrected, ceremonial diplomas for the heroes.
 class Diploma(Flowable):
  def __init__(self,name):super().__init__();self.width=490;self.height=400;self.name=name
  def draw(self):
   c=self.canv;c.saveState();c.setStrokeColor(GOLD);c.setLineWidth(3);c.roundRect(9,12,470,375,17)
   c.setStrokeColor(PUR);c.setLineWidth(1.3);c.roundRect(22,25,444,351,12)
   c.setFillColor(PUR);c.setFont('DVS-B',23);c.drawCentredString(244,311,'DYPLOM ZWYCIĘSTWA')
   c.setFont('DV',13);c.drawCentredString(244,260,'DLA '+self.name)
   c.setFont('DVS-B',16);c.drawCentredString(244,213,'STRAŻNICZKI SIEDMIU ŚWIATÓW')
   for y,t in [(174,'Za odwagę, wytrwałość i współpracę,'),(151,'odnalezienie 60 fragmentów tajemnicy,'),(128,'odkrycie kryjówki Morthara na Kasprowym Wierchu'),(105,'oraz przywrócenie wolności Siedmiu Światom.')]:
    c.setFont('DV',10);c.drawCentredString(244,y,t)
   c.setFont('DVS-B',10);c.drawCentredString(244,65,'MORWENA • PROFESOR VOLT • MISTRZ GRY')
   c.restoreState()
 def diploma_sheet(name,filename):
  story=[P('OSTATNIA NAGRODA','title'),P('Dyplom po pokonaniu Morthara','subtitle'),Spacer(1,35),Diploma(name)]
  dest=OUT/('_'+filename+'.pdf')
  SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=MARGIN,leftMargin=MARGIN,topMargin=47,bottomMargin=44).build(story,onFirstPage=lambda c,d:page_frame(c,d,'DYPLOM'))
  return dest
 diploma_zosia=diploma_sheet('ZOSI','dyplom_zosia')
 diploma_emilka=diploma_sheet('EMILKI','dyplom_emilki')
 world4_discs=build_world4_discs()
 world4_symbols=build_world4_symbols()
 sections=[]
 def add(title,filename,pages=None,kind='pdf'):
  sections.append((title,filename,pages,kind))
 add('Etykiety kopert z nazwami światów',labels)
 add('Tabliczki na drzwi siedmiu światów',room_labels)
 add('I • Karty bestii',locate('monsters'),None,'image')
 add('I • Pieczęć',seals[1])
 add('II • Trzy lustrzane wiadomości',locate('world2'),[1])
 add('II • Pieczęć',seals[2])
 add('III • Instrukcja obrazkowa Enigmy',locate('enigma'),None)
 add('III • Etykiety stanowisk',stations)
 add('III • Pieczęć',seals[3])
 add('IV • Cztery wymienne tarcze (7, 4, 2B, 9)',world4_discs)
 add('IV • Symbole do przyklejenia na odwrotach',world4_symbols)
 add('IV • Pieczęć',seals[4])
 add('V • Sześć symboli ksiąg',locate('books5'),[2])
 add('V • Pieczęć',seals[5])
 add('VI • Pieczęć',seals[6])
 add('VII • List Morthara',locate('final7'),[1])
 add('VII • Magiczne słowo',locate('final7'),[3])
 add('VII • Siódma pieczęć',seven)
 add('VII • Dyplom dla Zosi',diploma_zosia)
 add('VII • Dyplom dla Emilki',diploma_emilka)

 result=fitz.open()
 bookmarks=[]
 for title,path,indices,kind in sections:
  first=len(result)+1
  if kind=='image':
   doc2=fitz.open();page=doc2.new_page(width=A4[1],height=A4[0]);page.insert_image(fitz.Rect(22,22,A4[1]-22,A4[0]-22),filename=str(path),keep_proportion=True)
  else:
   doc2=fitz.open(path)
  pages=indices if indices is not None else list(range(len(doc2)))
  for no in pages:result.insert_pdf(doc2,from_page=no,to_page=no)
  bookmarks.append([1,title,first]);doc2.close()
 # Normalize pagination after merging legacy source PDFs.
 for no,pg in enumerate(result,1):
  pg.add_redact_annot(fitz.Rect(440,814,587,842),fill=(1,1,1))
  pg.apply_redactions(images=0,graphics=0,text=0)
  pg.insert_text((481,831),f'Strona {no} / {len(result)}',fontsize=8,color=(0.37,0.34,0.43))
 result.set_toc(bookmarks)
 result.set_metadata({'title':'Klątwa Siedmiu Światów — wyłącznie rekwizyty do druku','author':'Kreatywny escape room — dokumentacja finałowa','keywords':'Siedem światów, puzzle, karty, pieczęcie, Zosia, Emilka'})
 result.save(str(dst),garbage=4,deflate=True)
 result.close()
 generated_names=['_labels.pdf','_room_labels.pdf','_enigma_stations.pdf','_seal7.pdf','_world4_discs.pdf','_world4_symbols.pdf',
                  '_dyplom_zosia.pdf','_dyplom_emilka.pdf'] + [
                    f'_seal_{number}.pdf' for number in range(1,7)]
 for name in generated_names:
  try: (OUT/name).unlink(missing_ok=True)
  except OSError: pass
 return sections

if __name__=='__main__':
 a=OUT/'Instrukcja_organizatora.pdf'; b=OUT/'Materialy_do_druku.pdf'
 build_guide(a);sections=build_handouts(b)
 print(a,a.stat().st_size,'bytes',len(fitz.open(a)),'pages')
 print(b,b.stat().st_size,'bytes',len(fitz.open(b)),'pages (physical materials only)')
 for title,src,pg,kind in sections: print(title,('all' if pg is None else pg))