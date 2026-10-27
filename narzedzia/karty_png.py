#!/usr/bin/env python3
"""Czarno-białe karty sześciu bestii: jeden arkusz PNG A4, cyfry z przodu."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parent/"01_Salon_Krypta_Szesciu_Bestii"/"KARTY_POTWOROW_CZARNO_BIALE.png"
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=2480,3508
im=Image.new("RGB",(W,H),"white");d=ImageDraw.Draw(im)
reg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font=ImageFont.truetype(bold,86);digit=ImageFont.truetype(bold,190);small=ImageFont.truetype(reg,32)
cards=[("WAMPIR","7"),("WILKOŁAK","2"),("MUMIA","9"),("WIEDŹMA","4"),("DUCH","1"),("KOŚCIOTRUP","6")]
def line(points,width=12): d.line(points,fill="black",width=width,joint="curve")
def monster(kind,cx,cy):
    if kind=="WAMPIR":
        d.polygon([(cx-260,cy+260),(cx-180,cy-120),(cx-100,cy+40),(cx,cy-200),(cx+100,cy+40),(cx+180,cy-120),(cx+260,cy+260)],outline="black",width=14)
        d.ellipse((cx-110,cy-130,cx+110,cy+100),outline="black",width=13)
        d.ellipse((cx-60,cy-30,cx-32,cy-2),fill="black");d.ellipse((cx+32,cy-30,cx+60,cy-2),fill="black")
        line([(cx-40,cy+45),(cx+40,cy+45)],7)
        line([(cx-24,cy+45),(cx-14,cy+85)],7);line([(cx+24,cy+45),(cx+14,cy+85)],7)
    elif kind=="WILKOŁAK":
        d.polygon([(cx-160,cy+135),(cx-205,cy-200),(cx-60,cy-100),(cx,cy-170),(cx+60,cy-100),(cx+205,cy-200),(cx+160,cy+135),(cx+75,cy+220),(cx-75,cy+220)],outline="black",width=14)
        d.ellipse((cx-90,cy-20,cx-35,cy+25),fill="black");d.ellipse((cx+35,cy-20,cx+90,cy+25),fill="black")
        d.polygon([(cx-35,cy+80),(cx+35,cy+80),(cx,cy+115)],fill="black")
        line([(cx-95,cy+145),(cx,cy+190),(cx+95,cy+145)],8)
    elif kind=="MUMIA":
        d.rounded_rectangle((cx-150,cy-230,cx+150,cy+230),radius=110,outline="black",width=14)
        for j in range(-190,220,55):line([(cx-130,cy+j),(cx+130,cy+j+45)],8)
        d.ellipse((cx-82,cy-95,cx-24,cy-37),fill="black");d.ellipse((cx+24,cy-95,cx+82,cy-37),fill="black")
    elif kind=="WIEDŹMA":
        d.polygon([(cx,cy-290),(cx-190,cy-10),(cx+190,cy-10)],outline="black",width=13)
        d.ellipse((cx-240,cy-28,cx+240,cy+22),outline="black",width=13)
        d.ellipse((cx-125,cy+25,cx+125,cy+245),outline="black",width=13)
        d.ellipse((cx-75,cy+110,cx-40,cy+145),fill="black");d.ellipse((cx+40,cy+110,cx+75,cy+145),fill="black")
        line([(cx-40,cy+190),(cx+40,cy+190)],8)
    elif kind=="DUCH":
        d.arc((cx-170,cy-260,cx+170,cy+120),180,360,fill="black",width=13)
        line([(cx-170,cy-65),(cx-170,cy+230),(cx-100,cy+165),(cx-35,cy+230),(cx+35,cy+165),(cx+100,cy+230),(cx+170,cy+165),(cx+170,cy-65)],13)
        d.ellipse((cx-90,cy-65,cx-30,cy+20),fill="black");d.ellipse((cx+30,cy-65,cx+90,cy+20),fill="black")
        d.ellipse((cx-35,cy+65,cx+35,cy+150),fill="black")
    else:
        d.ellipse((cx-155,cy-220,cx+155,cy+105),outline="black",width=14)
        d.rounded_rectangle((cx-110,cy+80,cx+110,cy+230),radius=25,outline="black",width=14)
        d.ellipse((cx-100,cy-95,cx-20,cy+5),fill="black");d.ellipse((cx+20,cy-95,cx+100,cy+5),fill="black")
        d.polygon([(cx,cy+10),(cx-25,cy+55),(cx+25,cy+55)],fill="black")
        for xx in [-65,-22,22,65]:line([(cx+xx,cy+150),(cx+xx,cy+210)],6)
for i,(name,n) in enumerate(cards):
    col=i%2;row=i//2
    x=70+col*1210;y=90+row*1130
    d.rounded_rectangle((x,y,x+1130,y+1060),radius=45,outline="black",width=10)
    d.rounded_rectangle((x+25,y+25,x+1105,y+1035),radius=28,outline="black",width=4)
    d.text((x+565,y+75),name,font=font,anchor="mt",fill="black")
    monster(name,x+565,y+520)
    d.text((x+565,y+820),n,font=digit,anchor="mt",fill="black")
im.save(OUT,optimize=True)
print(OUT)
