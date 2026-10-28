#!/usr/bin/env python3
"""Build canonical two-document set for Klątwa Siedmiu Światów.
Uses existing verified original drawing assets and new authoritative setup text.
A PDF source can be resolved either from local /mnt/data or organized GitHub subdirectories.
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

BASE = Path(os.getenv('HALLOWEEN_ASSET_DIR','/mnt/data'))
OUT = Path(os.getenv('HALLOWEEN_OUT_DIR','/mnt/data'))
OUT.mkdir(parents=True, exist_ok=True)
ASSETS={
'monsters':'01_Salon_Krypta_Szesciu_Bestii/KARTY_POTWOROW_CZARNO_BIALE.png',
'seal1':'01_Salon_Krypta_Szesciu_Bestii/Pieczec_I_KRUK-583_czarno_biala_poprawiona.pdf',
'world2':'02_Sypialnia_Galeria_Lustrzanych_Szeptow/Swiat_II_Galeria_Lustrzanych_Szeptow_DO_DRUKU.pdf',
'enigma':'03_Kuchnia_Laboratorium_Doktora_Morsea/Enigma_Doktora_Morsea_PELNA_INSTRUKCJA_OBRAZKOWA.pdf',
'seal3':'03_Kuchnia_Laboratorium_Doktora_Morsea/Pieczec_III_Enigma_Doktora_Morsea.pdf',
'discs':'04_Biuro_Mechanizm_Zatrzymanego_Czasu/Swiat_IV_Cztery_Tarcze_12_Cyfr.pdf',
'symbols4':'04_Biuro_Mechanizm_Zatrzymanego_Czasu/Swiat_IV_Symbole_i_Dziennik_Zegarmistrza.pdf',
'seal4':'04_Biuro_Mechanizm_Zatrzymanego_Czasu/Pieczec_IV_Mechanizm_Zatrzymanego_Czasu.pdf',
'books5':'05_Pokoj_Emilki_Biblioteka_Niewidzialnego_Atramentu/Swiat_V_Kompletny_Pakiet_Do_Druku.pdf',
'world6':'06_Pokoj_Zosi_Laboratorium_Ohma/Swiat_VI_Laboratorium_Volta_PELNY_KLIMATYCZNY_PAKIET.pdf',
'final7':'07_Garderoba_Komnata_Cienia/Swiat_VII_FINAL_60_PUZZLI_KASPROWY.pdf',
}
LOCAL={
'monsters':'KARTY_POTWOROW_CZARNO_BIALE.png',
'seal1':'Pieczec_I_KRUK-583_czarno_biala_poprawiona.pdf',
'world2':'Swiat_II_Galeria_Lustrzanych_Szeptow_DO_DRUKU.pdf',
'enigma':'Enigma_Doktora_Morsea_PELNA_INSTRUKCJA_OBRAZKOWA.pdf',
'seal3':'Pieczec_III_Enigma_Doktora_Morsea.pdf',
'discs':'Swiat_IV_Cztery_Tarcze_12_Cyfr.pdf',
'symbols4':'Swiat_IV_Symbole_i_Dziennik_Zegarmistrza.pdf',
'seal4':'Pieczec_IV_Mechanizm_Zatrzymanego_Czasu.pdf',
'books5':'Swiat_V_Kompletny_Pakiet_Do_Druku.pdf',
'world6':'Swiat_VI_Laboratorium_Volta_PELNY_KLIMATYCZNY_PAKIET.pdf',
'final7':'Swiat_VII_FINAL_60_PUZZLI_KASPROWY.pdf',
}

def locate(key):
 for candidate in (BASE/ASSETS[key], BASE/LOCAL[key]):
  if candidate.is_file():return candidate
 raise FileNotFoundError(f'Missing source asset {key}: '+str(BASE/ASSETS[key]))

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
G += [Spacer(1,72),P('KLĄTWA<br/>SIEDMIU ŚWIATÓW','splash'),P('JEDNA INSTRUKCJA DLA MISTRZA GRY','center'),Spacer(1,25),P('Siedem światów · dwoje dzieci · dwa tablety · 60 puzzli · jedna skrzynia','center'),Spacer(1,30),P('WERSJA OBOWIĄZUJĄCA — 28 PAŹDZIERNIKA 2026','center')]
quote('TEN DOKUMENT ZAWIERA WSZYSTKIE ROZWIĄZANIA. Nie pokazuj go Zosi ani Emilce. Wszystkie karty, pieczęcie, rysunki i instrukcje do wycinania znajdują się w osobnym pliku „02_MATERIALY_DO_DRUKU.pdf”.')
p('Ważne: źródłem prawdy są aktualne etapy aplikacji i ostatnie ustalenia. Starsze, rozproszone PDF-y mają nieaktualne fragmenty. W tej wersji zebrano przygotowanie wszystkich siedmiu światów w jednym miejscu.')
breakp()
h('00 · Przygotowania ogólne i uruchomienie')
hh('Sprzęt i rzeczy do zebrania')
p('Laptop z Ubuntu i Pythonem 3, domowe Wi-Fi, dwa tablety (Strażniczka I = Zosia, Strażniczka II = Emilka), ładowarki, czołówki, nożyczki, taśma papierowa, sześć kopert na pieczęcie, sześć MAŁYCH kopert na rezystory, długopis z tuszem UV i latarką UV, lustro, sześć książek z co najmniej 50 stronami, mikroskop z oświetleniem, komplet czterech silniczków z papierowymi tarczami i osłonami, stroboskop, Arduino UNO z Enigmą, czterocyfrowa kłódka oraz skrzynia.')
p('Materiały papiernicze: dwie kopie PDF-ów do sprawdzenia; papier zwykły na karty i pieczęcie; karton 160–250 g/m² na stronę 60 puzzli; przygotowany długopis UV; czarne pudełko/szafka lub skrzynia na finał; słodycze dla obu dziewczynek; dwa dyplomy.')
hh('Zasilanie i bezpieczeństwo')
p('Elektronikę montuje dorosły i kontroluje przy odłączonym zasilaniu. Nie używaj napięcia sieciowego na odsłoniętych przewodach. W eksperymencie ze stroboskopem nie kieruj błysków w oczy; przy nadwrażliwości na światło stosuj wariant bez stroboskopu. Ruchome tarcze osłoń. Mikroskop, UV i małe rezystory używaj pod nadzorem; nie świeć UV w oczy i nie pozwalaj wkładać drobnych elementów do ust. Nie chowaj kopert przy gniazdkach ani ostrych narzędziach.')
hh('Zanim przyjdą Strażniczki')
p('1. Na laptopie zatrzymaj działający serwer (Ctrl+C), wykonaj <b>git pull</b>, następnie <b>python3 server.py</b>.\n<br/>2. Ustal adres IP laptopa poleceniem <b>hostname -I</b>; na tabletach otwórz <b>http://ADRES_IP:8000</b>. Każda wybiera inny numer Strażniczki.\n<br/>3. Przeprowadź próbę obu tabletów; sprawdź, czy postęp jest zsynchronizowany.\n<br/>4. Jeśli była rozgrywka testowa, uruchom <b>python3 reset.py</b> przy działającym serwerze. Uwaga: reset usuwa WSZYSTKIE dane poprzedniej gry — nie używaj go w środku przygody.\n<br/>5. Przygotuj zegar 120 minut; aplikacja odmierza czas od wspólnej przysięgi i zatrzymuje wynik po wpisaniu magicznego słowa na obu tabletach. Co 10 minut Morthar może wyświetlać klimatyczną wiadomość, którą dzieci zamykają jednym przyciskiem.')
hh('Zasada puzzli: 60 kawałków, nie sześć')
p('Wydrukuj JEDNĄ planszę finałową z siatką 6 × 10. <b>Na całym arkuszu, od tyłu, napisz długopisem UV wiadomość o Kasprowym Wierchu</b> (tekst poniżej w Świecie VII). Wysusz. Dopiero potem potnij planszę po wszystkich liniach na 60 prostokątów. Podziel na sześć paczek po DZIESIĘĆ elementów i włóż po jednej paczce do kopert I–VI. Nie należy wkładać jednego puzzla do każdego świata. Nie drukuj sześciu pełnych plansz!')
p('Drobne kawałki pogrupuj w szóstki po 10 losowo, nie według ułożenia obrazka. Każda koperta pieczęci I–VI zawiera swój wydrukowany znak oraz dokładnie 10 fragmentów puzzli. W finale dziewczynki łączą 60 elementów, odwracają gotowy obraz (najbezpieczniej między dwoma kartonami), podświetlają rewers UV i odczytują wskazówkę.')
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
p('Przygotuj cztery fizyczne tarcze z powtarzaną cyfrą, cztery małe silniki DC 3–6 V i bezpieczne osłony. Oznacz stanowiska nieruchomymi symbolami, obok tarcz, nie bezpośrednio na nich: <b>KSIĘŻYC = 7</b>, <b>KRUK = 2</b>, <b>KLUCZ = 9</b>, <b>KLEPSYDRA = 4</b>. Tarcze drukuj w skali 100% i upewnij się, że są wyważone. Nie pozwalaj ich dotykać podczas pracy.')
p('Jeżeli używasz z repozytorium układu NodeMCU V3 + 2×L298N, sprawdź zgodność połączeń ze skeczem <b>Mechanizm_Zatrzymanego_Czasu_NodeMCU.ino</b>. Silniki L298N mają spadki napięcia — próba na 5 V może nie ruszyć. NodeMCU zasilaj osobnym USB, przy wspólnej masie GND, nie łącz dodatnich wyjść niezależnych ładowarek. Nie poprawiaj połączeń pod napięciem. Dokładny schemat został wcześniej opisany w starszych materiałach, lecz obecny pakiet opiera się na gotowym, przetestowanym mechanizmie.')
hh('Zagadki i wynik')
p('Strażniczka I odczytuje cyfry przez zewnętrzny stroboskop, przy pomocy dorosłego. Strażniczka II otrzymuje w aplikacji logiczne wskazówki o kolejności symboli. Prawidłowy porządek: <b>KSIĘŻYC → KRUK → KLUCZ → KLEPSYDRA</b>; kod <b>7294</b>. Nie wystarczy ustawić tarcz w kolejności na biurku — kolejność wynika z zagadki.')
p('Kopertę <b>IV</b> z pieczęcią <b>CZAS-604</b> i 10 puzzlami schowaj <b>w szufladzie biurka w gabinecie</b>. Jeżeli zabawa stroboskopem jest niewskazana, dorosły powinien przygotować bezpieczny zastępczy sposób ujawnienia tych samych cyfr. Nie kieruj błysków w oczy.')
p('□ Cztery tarcze się obracają i są osłonięte. □ Symbole stoją przy właściwych cyfrach. □ Stroboskop sprawdzony w warunkach pokoju. □ Koperta IV z 10 puzzlami jest w szufladzie.')
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
quote('Tekst do zapisania UV na odwrocie jednej, jeszcze NIEROZCIĘTEJ planszy: „MORTHAR UKRYŁ SIĘ NA KASPROWYM WIERCHU. WYSOKOŚĆ TEGO SZCZYTU W METRACH NAD POZIOMEM MORZA TO CZTERY CYFRY OTWIERAJĄCE SKRZYNIĘ”.')
p('Zapisz treść dużymi literami, tak aby przebiegała przez wiele przyszłych granic cięcia. Upewnij się, że odczytanie pojedynczego kawałka niczego nie zdradza. Poczekaj aż UV wyschnie; potnij planszę na dokładnie 60 elementów. Rozdziel po 10 do kopert I–VI. Obie dziewczynki muszą najpierw złożyć 60 elementów, a dopiero potem odwrócić całość i oświetlić UV.')
hh('Ostatnie pięć kroków')
p('1. Po 6. pieczęci aplikacja wysyła do Komnaty Cienia.\n<br/>2. Dziewczynki układają 60 puzzli, odwracają i czytają zagadkę UV.\n<br/>3. Ustalają wysokość Kasprowego Wierchu: <b>1987 m n.p.m.</b> — kod kłódki <b>1987</b>. Nie wpisuje się go do aplikacji.\n<br/>4. Otwierają skrzynię, znajdują list Morthara, słodycze i kartkę ze słowem <b>WOLNOŚĆ</b>. Wypowiadają je i wpisują na obu tabletach.\n<br/>5. Gdy obie wpiszą poprawne słowo, zegar zatrzymuje się, pojawia się animowane zwycięstwo i dokładny czas ukończenia. Wręcz dyplomy.')
p('□ Kłódka naprawdę otwiera się kodem 1987. □ List jest w skrzyni. □ Kartka WOLNOŚĆ jest w skrzyni. □ Słodycze przygotowane. □ Przygotowany jest sposób na bezpieczne odwrócenie ułożonych puzzli, np. między dwoma sztywnymi kartonami.')
breakp()
h('LISTA OSTATECZNA · przed wpuszczeniem dzieci')
G.append(tbl([['Sprawdź','Stan'],['Dwa tablety + Wi-Fi + zsynchronizowany serwer','□'],['Przygotowane stanowiska, sprzęt i zasilanie','□'],['Sześć kart bestii w salonie','□'],['Trzy lustrzane kartki w sypialni','□'],['Działająca Enigma Morse’a w kuchni','□'],['Cztery osłonięte tarcze w gabinecie','□'],['Sześć ksiąg UV + długopis w piórniku','□'],['Sześć kopert rezystorów + mikroskop','□'],['Sześć kopert I–VI zawiera pieczęć i 10 puzzli','□'],['Skrzynia z kłódką 1987, listem, WOLNOŚĆ i nagrodami','□'],['Wszystkie 60 puzzli mają jedną wspólną wiadomość UV','□'],['Stare testowe dane gry zresetowano PRZED startem','□']], [435,70]));gap(10)
quote('OSTATNIA PRÓBA: uruchom obu Strażniczek w trybie testowym i sprawdź fizycznie wszystkie kryjówki, kody, rewers UV, jakość mikroskopu i działanie zamka. Nie resetuj ani nie zmieniaj materiałów, gdy dzieci już grają.')
p('Uwaga o źródłach: skecz i instrukcja elektroniczna pochodzą z bieżącego repozytorium. Ustalony komplet 60 puzzli i finał WOLNOŚĆ zastępują dawne warianty zakończenia. Sam dokument nie potwierdza, czy fizyczne układy są już poprawnie zmontowane — wymagana jest próba sprzętowa.')

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

def build_handouts(dst):
 story=[P('MATERIAŁY DO DRUKU','title'),P('Siedem światów · wszystko w jednym pliku','subtitle'),P('Wydrukuj pojedynczo lub wszystkie strony na A4. Materiały wycinaj po liniach lub ramkach. Tam, gdzie opis mówi „napisz UV”, po wydrukowaniu użyj niewidzialnego atramentu; zwykła drukarka nie wydrukuje niewidzialnego szyfru.'),P('W TYM PLIKU','h1')]
 story.append(tbl([['Świat','Karty / elementy do wydrukowania'],['I — salon','6 kart bestii + Pieczęć I + etykieta'],['II — sypialnia','3 kartki lustrzane + Pieczęć II'],['III — kuchnia','Instrukcja obrazkowa Enigmy + oznaczenia części + Pieczęć III'],['IV — gabinet','4 tarcze + 4 symbole + Pieczęć IV'],['V — pokój Emilki','6 symboli ksiąg + notatnik + Pieczęć V'],['VI — pokój Zosi','Karty Volta, tabela, mikroskop, notatnik + Pieczęć VI'],['VII — garderoba','60 puzzli, list Morthara, słowo WOLNOŚĆ, Pieczęć VII, dyplomy']], [145,360]));story.append(Spacer(1,18));story.append(P('DODATKOWE PRZYGOTOWANIE — NIE DA SIĘ WYDRUKOWAĆ ZWYKŁĄ DRUKARKĄ','h2'));story.append(P('Atramentem UV ręcznie oznacz strony sześciu książek i sześć kopert z rezystorami. Na rewersie całego arkusza 60 puzzli zapisz zagadkę o Kasprowym Wierchu PRZED rozcięciem. Kody rozwiązania i dokładne kryjówki znajdują się wyłącznie w PDF-ie organizatora.'));story.append(Spacer(1,12));story.append(P('UWAGA: kartę z magicznym słowem i list Morthara włóż do zamkniętej skrzyni. Nie zostawiaj wydrukowanych odpowiedzi na widoku.','quote'))
 guide_intro=OUT/'_print_intro.pdf'
 doc=SimpleDocTemplate(str(guide_intro),pagesize=A4,rightMargin=MARGIN,leftMargin=MARGIN,topMargin=47,bottomMargin=44)
 doc.build(story,onFirstPage=lambda c,d:page_frame(c,d,'DO WYDRUKU'),onLaterPages=lambda c,d:page_frame(c,d,'DO WYDRUKU'))

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
  dest=OUT/('_'+filename+'.pdf')
  SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=MARGIN,leftMargin=MARGIN,topMargin=47,bottomMargin=44).build(arr,onFirstPage=lambda c,d:page_frame(c,d,tag),onLaterPages=lambda c,d:page_frame(c,d,tag))
  return dest

 labelparts=[('title','ETYKIETY KOPERT I–VI'),('p','Wytnij i przyklej na sześciu kopertach z pieczęciami. Uwaga: sześciu małych kopert z rezystorami NIE podpisuj widzialnym tuszem; oznacz je ręcznie UV.')]
 for row in [('I — SALON','II — SYPIALNIA'),('III — KUCHNIA','IV — GABINET'),('V — POKÓJ EMILKI','VI — POKÓJ ZOSI')]:
  labelparts.extend([('table',tbl([[f'✦ KOPERTA {row[0]}',f'✦ KOPERTA {row[1]}']], [252,252],False)),('spacer','15')])
 labelparts += [('h2','WAŻNE: zawartość każdej koperty'),('p','Dokładnie jedna pieczęć świata i 10 losowych kawałków finałowej układanki. Nie kładź kartki z rozwiązaniem na zewnątrz koperty.')]
 labels=textpage('labels',labelparts)
 stations=textpage('enigma_stations',[
 ('title','ENIGMA DOKTORA MORSE’A'),('subtitle','Etykiety do przygotowania 7 stanowisk w kuchni'),
 ('table',tbl([[f'{i}. {txt}'] for i,txt in enumerate(['ARDUINO UNO — mózg maszyny','WYŚWIETLACZ LED 8×32 — cztery kwadraty','KLAWIATURA S1–S16','NIEBIESKA LED + rezystor 330 Ω','ZIELONA LED + rezystor 330 Ω','PŁYTKA STYKOWA I PRZEWODY','ZASILANIE — PODŁĄCZA DOROSŁY'],1)],[505],False)),
 ('spacer','15'),('h2','Legenda klawiatury — postaw obok urządzenia'),
 ('table',tbl([['Przycisk','Działanie'],['S1–S9','Cyfry 1–9'],['S10','0'],['S11','Usuń ostatnią cyfrę'],['S12','Zatwierdź'],['S13','Wyczyść'],['S14–S16','Nieużywane']],[165,340])),
 ('p','Program Arduino UNO musi być wgrany przed zabawą. Nie włączaj zasilania przed kontrolą dorosłego.')])
 clocknote=textpage('clock_notes',[
 ('title','DZIENNIK ZEGARMISTRZA'),('subtitle','Karta zapisu do Świata IV — dzieci korzystają z logicznych wskazówek NA TABLECIE'),
 ('quote','„Zatrzymać czas nie znaczy zatrzymać koło. Prawdziwa chwila ujawnia się tylko w odpowiednim świetle”. — Aureliusz'),
 ('table',tbl([['Symbol','Cyfra odczytana przez światło'],['KSIĘŻYC','………………………………'],['KRUK','………………………………'],['KLUCZ','………………………………'],['KLEPSYDRA','………………………………']],[240,265])),
 ('spacer','20'),('p','Nie ustawiajcie cyfr w kolejności ustawienia silników! Strażniczka II otrzymała na swoim tablecie zasady właściwej kolejności.')])
 booklog=textpage('book_logs',[
 ('title','DZIENNIK BEZIMIENNEJ BIBLIOTEKARKI'),('subtitle','Świat V — zapisujcie jedynie znaki UV z prawidłowych stron'),
 ('quote','„Morthar pozostawił na kartach fałszywe litery. Tylko właściwa strona każdej księgi przechowuje prawdę”.'),
 ('table',tbl([['Symbol księgi','Odnaleziona strona','Litera / litery UV'],['KSIĘŻYC','…………','…………'],['KRUK','…………','…………'],['KLUCZ','…………','…………'],['PAJĄK','…………','…………'],['WĄŻ','…………','…………'],['ŚWIECA','…………','…………']],[150,170,185])),
 ('spacer','25'),('h2','Kolejność symboli ustalona z obu tabletów'),('p','1. ………………………  2. ………………………  3. ………………………'),('p','4. ………………………  5. ………………………  6. ………………………'),('p','Tajemnicze imię: …………………………………………………………')])
 seven=textpage('seal7',[
 ('title','OSTATNIA PIECZĘĆ'),('subtitle','Jeśli chcesz, włóż ją do skrzyni obok listu Morthara, kartki z zaklęciem i słodyczy.'),('seal7','')])


 def seal_sheet(number,roman,title,code):
  return textpage('seal_'+str(number),[('title','PIECZĘĆ '+roman+' — '+title),('subtitle','Wytnij ozdobną kartę. Włóż do koperty świata '+str(number)+' razem z DOKŁADNIE 10 puzzlami.'),('seal_custom',(roman,title,code))])

 # Open all inputs: key assets, write handwritten cards as supplementary pages
 booknote=textpage('books_symbols_note',[('title','SYMBOLY KSIĄG'),('p','Wytnij znaki z kolejnej strony i przyklej na sześć książek. Nie pisz numerów stron ani ukrytych liter zwykłym długopisem. Atrament UV i prawidłowe strony opisano tylko w instrukcji organizatora.')])
 uvnote=textpage('uv_letter_note',[('title','KOPERTY PROFESORA VOLTA'),('subtitle','Świat VI — sześć małych kopert z rezystorami'),('quote','Sześć przesyłek. Sześć kolorowych kodów. Litery zobaczycie tylko w niewidzialnym świetle.'),('p','Użyj sześciu zwykłych małych kopert. Dopiero po przygotowaniu rezystorów dorosły zapisze na każdej JEDNĄ literę UV. Nie drukuj widzialnych liter i nie numeruj kopert, bo kolejność wyznaczą dopiero pomiary.')])

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
 sections=[]
 def add(title,filename,pages=None,kind='pdf'):
  sections.append((title,filename,pages,kind))
 add('Karta drukowania',guide_intro)
 add('Etykiety kopert',labels)
 add('I • Karty bestii',locate('monsters'),None,'image')
 add('I • Pieczęć',seals[1])
 add('II • Trzy lustrzane wiadomości',locate('world2'),[1])
 add('II • Pieczęć',seals[2])
 add('III • Instrukcja obrazkowa Enigmy',locate('enigma'),None)
 add('III • Etykiety i klawiatura',stations)
 add('III • Pieczęć',seals[3])
 add('IV • Cztery tarcze zegarmistrza',locate('discs'),[0,1,2,3])
 add('IV • Cztery symbole',locate('symbols4'),[0])
 add('IV • Dziennik obserwacji',clocknote)
 add('IV • Pieczęć',seals[4])
 add('V • Instrukcja do symboli',booknote)
 add('V • Sześć symboli ksiąg',locate('books5'),[2])
 add('V • Dziennik bibliotekarki',booklog)
 add('V • Pieczęć',seals[5])
 add('VI • Wprowadzenie, mikroskop i tabela',locate('world6'),[0,1,2,3])
 add('VI • Karta kopert UV',uvnote)
 add('VI • Pieczęć',seals[6])
 add('VII • Plansza 60 puzzli',locate('final7'),[4])
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
   if 'Wprowadzenie, mikroskop' in title:
    # Earlier PDFs used an unavailable emoji glyph at the start of three headings.
    # Replace only the missing glyph with a printable violet asterisk.
    fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    for k in (1,2,3):
     pg=doc2[k]
     pg.add_redact_annot(fitz.Rect(47,45,60,71),fill=(1,1,1))
     pg.apply_redactions(images=0,graphics=0,text=0)
     pg.insert_font(fontname='DejaCustom',fontfile=fontfile)
     pg.insert_text((49,65),'✦',fontname='DejaCustom',fontsize=18,color=(0.33,0.22,0.39),overlay=True)
  pages=indices if indices is not None else list(range(len(doc2)))
  for no in pages:result.insert_pdf(doc2,from_page=no,to_page=no)
  bookmarks.append([1,title,first]);doc2.close()
 result.set_toc(bookmarks)
 result.set_metadata({'title':'Klątwa Siedmiu Światów — wszystkie materiały do druku','author':'Kreatywny escape room — dokumentacja finałowa','keywords':'Siedem światów, puzzle, karty, pieczęcie, Zosia, Emilka'})
 result.save(str(dst),garbage=4,deflate=True)
 result.close()
 return sections

if __name__=='__main__':
 a=OUT/'01_INSTRUKCJA_ORGANIZATORA.pdf'; b=OUT/'02_MATERIALY_DO_DRUKU.pdf'
 build_guide(a);sections=build_handouts(b)
 print(a,a.stat().st_size,'bytes',len(fitz.open(a)),'pages')
 print(b,b.stat().st_size,'bytes',len(fitz.open(b)),'pages')
 for title,src,pg,kind in sections: print(title,('all' if pg is None else pg))