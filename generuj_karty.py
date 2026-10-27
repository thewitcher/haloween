#!/usr/bin/env python3
"""Generuje jednostronne karty A4 — 6 bestii na jednej stronie."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

DEST=Path(__file__).resolve().parent/"01_Salon_Krypta_Szesciu_Bestii"/"KARTY_POTWOROW.pdf"
DEST.parent.mkdir(parents=True,exist_ok=True)
for name,path in [("DejaVu","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),("DejaVuBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name,path))
W,H=A4
c=canvas.Canvas(str(DEST),pagesize=A4)
c.setTitle("Krypta Szesciu Bestii - karty do druku")
cards=[("WAMPIR","7"),("WILKOŁAK","2"),("MUMIA","9"),("WIEDŹMA","4"),("DUCH","1"),("KOŚCIOTRUP","6")]
margin=24;gap=12;cardw=(W-2*margin-gap)/2;cardh=(H-2*margin-2*gap)/3
def monster(kind,cx,cy):
    c.setLineWidth(3)
    if kind=="WAMPIR":
        c.setFillColorRGB(.17,.12,.24);p=c.beginPath();p.moveTo(cx-53,cy-30);p.lineTo(cx-32,cy+46);p.lineTo(cx+32,cy+46);p.lineTo(cx+53,cy-30);p.close();c.drawPath(p,fill=1)
        c.setFillColorRGB(.97,.84,.77);c.circle(cx,cy+17,27,fill=1,stroke=0)
        c.setFillColorRGB(.15,.08,.15);c.circle(cx-9,cy+22,4,fill=1,stroke=0);c.circle(cx+9,cy+22,4,fill=1,stroke=0)
        c.setStrokeColorRGB(.6,.06,.09);c.line(cx-12,cy+4,cx+12,cy+4)
        c.setStrokeColorRGB(.9,.9,.9);c.line(cx-7,cy+4,cx-4,cy-3);c.line(cx+7,cy+4,cx+4,cy-3)
    elif kind=="WILKOŁAK":
        c.setFillColorRGB(.45,.31,.22);p=c.beginPath();p.moveTo(cx-36,cy+18);p.lineTo(cx-38,cy+59);p.lineTo(cx-11,cy+42);p.lineTo(cx+11,cy+42);p.lineTo(cx+38,cy+59);p.lineTo(cx+36,cy+18);p.curveTo(cx+45,cy-25,cx-45,cy-25,cx-36,cy+18);c.drawPath(p,fill=1)
        c.setFillColorRGB(.95,.78,.31);c.circle(cx-13,cy+20,6,fill=1,stroke=0);c.circle(cx+13,cy+20,6,fill=1,stroke=0)
        c.setFillColorRGB(.16,.09,.08);c.circle(cx,cy+2,8,fill=1,stroke=0)
    elif kind=="MUMIA":
        c.setFillColorRGB(.88,.82,.66);c.roundRect(cx-34,cy-35,68,91,23,fill=1,stroke=0)
        c.setStrokeColorRGB(.55,.49,.39);c.setLineWidth(6)
        for offset in [-25,-8,9,26,43]: c.line(cx-28,cy+offset,cx+28,cy+offset+13)
        c.setFillColorRGB(.16,.13,.10);c.circle(cx-10,cy+21,5,fill=1,stroke=0);c.circle(cx+10,cy+21,5,fill=1,stroke=0)
    elif kind=="WIEDŹMA":
        c.setFillColorRGB(.30,.15,.38);p=c.beginPath();p.moveTo(cx,cy+70);p.lineTo(cx-39,cy+12);p.lineTo(cx+39,cy+12);p.close();c.drawPath(p,fill=1)
        c.ellipse(cx-51,cy+5,cx+51,cy+20,fill=1,stroke=0)
        c.setFillColorRGB(.65,.82,.54);c.circle(cx,cy-14,29,fill=1,stroke=0)
        c.setFillColorRGB(.14,.14,.14);c.circle(cx-10,cy-10,4,fill=1,stroke=0);c.circle(cx+10,cy-10,4,fill=1,stroke=0)
        c.setStrokeColorRGB(.17,.11,.17);c.line(cx-8,cy-27,cx+8,cy-27)
    elif kind=="DUCH":
        c.setFillColorRGB(.85,.93,.98);p=c.beginPath();p.moveTo(cx-37,cy-36);p.lineTo(cx-37,cy+19);p.curveTo(cx-37,cy+74,cx+37,cy+74,cx+37,cy+19);p.lineTo(cx+37,cy-36);p.lineTo(cx+21,cy-22);p.lineTo(cx+6,cy-36);p.lineTo(cx-9,cy-22);p.lineTo(cx-23,cy-36);p.close();c.drawPath(p,fill=1)
        c.setFillColorRGB(.10,.10,.16);c.ellipse(cx-20,cy+15,cx-8,cy+34,fill=1,stroke=0);c.ellipse(cx+8,cy+15,cx+20,cy+34,fill=1,stroke=0);c.ellipse(cx-7,cy-9,cx+7,cy+11,fill=1,stroke=0)
    else:
        c.setFillColorRGB(.94,.89,.77);c.circle(cx,cy+25,34,fill=1,stroke=0);c.roundRect(cx-25,cy-27,50,40,8,fill=1,stroke=0)
        c.setFillColorRGB(.12,.11,.13);c.circle(cx-12,cy+31,9,fill=1,stroke=0);c.circle(cx+12,cy+31,9,fill=1,stroke=0);c.ellipse(cx-6,cy+8,cx+6,cy+18,fill=1,stroke=0)
        c.setStrokeColorRGB(.3,.28,.27)
        for x in [-13,0,13]: c.line(cx+x,cy-18,cx+x,cy-26)
for i,(name,num) in enumerate(cards):
    col=i%2;row=i//2;x=margin+col*(cardw+gap);y=H-margin-(row+1)*cardh-row*gap
    c.setStrokeColorRGB(.5,.3,.15);c.setLineWidth(1.5);c.roundRect(x,y,cardw,cardh,12,stroke=1,fill=0)
    c.setFillColorRGB(.14,.09,.20);c.roundRect(x+7,y+7,cardw-14,cardh-14,10,stroke=0,fill=1)
    c.setFillColorRGB(.96,.75,.40);c.setFont("DejaVuBold",16);c.drawCentredString(x+cardw/2,y+cardh-33,name)
    monster(name,x+cardw/2,y+cardh/2+2)
    c.setFillColorRGB(.97,.81,.49);c.setFont("DejaVuBold",37);c.drawCentredString(x+cardw/2,y+27,num)
c.showPage();c.save()
print(DEST)
