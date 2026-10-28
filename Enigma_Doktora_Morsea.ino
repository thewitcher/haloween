// Enigma Doktora Morse'a — Arduino UNO, MAX7219 8x32, klawiatura 4x4
// Biblioteki: Keypad, MD_Parola, MD_MAX72XX
#include <Keypad.h>
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define DATA_PIN 11
#define CS_PIN 10
#define CLK_PIN 13
#define BLUE_PIN A0
#define GREEN_PIN A1
MD_Parola display(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);
const byte ROWS=4,COLS=4;
char keys[ROWS][COLS]={{'1','2','3','4'},{'5','6','7','8'},{'9','0','<','='},{'C','X','Y','Z'}};
byte rowPins[ROWS]={6,7,8,9};
byte colPins[COLS]={5,4,3,2};
Keypad keypad=Keypad(makeKeymap(keys),rowPins,colPins,ROWS,COLS);
const char* words[]={"NIE","MAM","SKRZYDEL","A","POTRAFIE","LATAC","NIE","MAM","UST","A","MOGE","GWIZDAC","NIE","MAM","DLONI","A","PORUSZAM","GALEZIAMI","NIE","ZOBACZYSZ","MNIE","CHOC","POCZUJESZ","KIEDY","PRZEJDE","OBOK","KIM","JESTEM"};
const byte wordCount=sizeof(words)/sizeof(words[0]);
const char* morse(char c){
 switch(c){case 'A':return ".-";case 'B':return "-...";case 'C':return "-.-.";case 'D':return "-..";case 'E':return ".";case 'F':return "..-.";case 'G':return "--.";case 'H':return "....";case 'I':return "..";case 'J':return ".---";case 'K':return "-.-";case 'L':return ".-..";case 'M':return "--";case 'N':return "-.";case 'O':return "---";case 'P':return ".--.";case 'Q':return "--.-";case 'R':return ".-.";case 'S':return "...";case 'T':return "-";case 'U':return "..-";case 'V':return "...-";case 'W':return ".--";case 'X':return "-..-";case 'Y':return "-.--";case 'Z':return "--..";default:return "";}
}
const unsigned long UNIT=260, WORD_GAP=5000, START_GAP=5000;
byte phase=0,wordIndex=0,charIndex=0,symbolIndex=0;
unsigned long deadline=0;
bool solved=false;
String entry="";
unsigned long temporaryUntil=0;
void showEntry(){display.displayClear();display.displayText(entry.c_str(),PA_CENTER,0,0,PA_PRINT,PA_NO_EFFECT);display.displayReset();}
void showText(const char* s){display.displayClear();display.displayText(s,PA_CENTER,65,0,PA_SCROLL_LEFT,PA_SCROLL_LEFT);display.displayReset();}
void startCycle(unsigned long now){digitalWrite(GREEN_PIN,LOW);digitalWrite(BLUE_PIN,HIGH);phase=0;wordIndex=charIndex=symbolIndex=0;deadline=now+START_GAP;}
void stepMorse(unsigned long now){
 if(solved||now<deadline)return;
 if(phase==0){digitalWrite(BLUE_PIN,LOW);phase=1;}
 else if(phase==1){digitalWrite(GREEN_PIN,LOW);phase=2;deadline=now+UNIT;return;}
 else if(phase==2){symbolIndex++;phase=1;}
 else if(phase==3){charIndex++;symbolIndex=0;phase=1;}
 else if(phase==4){wordIndex++;charIndex=symbolIndex=0;phase=1;}
 if(wordIndex>=wordCount){startCycle(now);return;}
 const char* word=words[wordIndex];
 if(!word[charIndex]){phase=4;deadline=now+WORD_GAP;return;}
 const char* code=morse(word[charIndex]);
 if(!code[symbolIndex]){phase=3;deadline=now+2*UNIT;return;}
 digitalWrite(GREEN_PIN,HIGH);
 deadline=now+(code[symbolIndex]=='-'?3*UNIT:UNIT);
}
void setup(){pinMode(BLUE_PIN,OUTPUT);pinMode(GREEN_PIN,OUTPUT);digitalWrite(BLUE_PIN,LOW);digitalWrite(GREEN_PIN,LOW);display.begin();display.setIntensity(2);showText("ENIGMA");startCycle(millis());}
void loop(){
 unsigned long now=millis();
 char key=keypad.getKey();
 if(key && !solved){
  if(key>='0'&&key<='9'&&entry.length()<5)entry+=key;
  else if(key=='<'&&entry.length())entry.remove(entry.length()-1);
  else if(key=='C')entry="";
  else if(key=='='){
   if(entry=="94287"){solved=true;digitalWrite(BLUE_PIN,LOW);digitalWrite(GREEN_PIN,LOW);showText("BURZA");}
   else{entry="";showText("BLAD");temporaryUntil=now+1500;}
  }
  if(!solved && key!='='){showEntry();temporaryUntil=0;}
 }
 if(!solved){stepMorse(now);if(temporaryUntil && now>=temporaryUntil){temporaryUntil=0;showEntry();}}
 if(display.displayAnimate())display.displayReset();
}
