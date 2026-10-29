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
// Jednostka Morse'a: kropka = 1, kreska = 3.
// Odstęp między elementami litery = 1 UNIT.
// Odstęp między literami / słowami liczony od zgaśnięcia ostatniego błysku.
const unsigned long UNIT=700, LETTER_GAP=5000, WORD_GAP=15000, START_GAP=5000;
enum TxState { BLUE_START, GREEN_ON, GREEN_OFF };
TxState txState=BLUE_START;
byte wordIndex=0, charIndex=0, symbolIndex=0;
unsigned long deadline=0;
bool solved=false;
String entry="";
unsigned long temporaryUntil=0;
void showEntry(){
 display.displayClear();
 display.displayText(entry.c_str(),PA_CENTER,0,0,PA_PRINT,PA_NO_EFFECT);
 display.displayReset();
}
void showText(const char* s){
 display.displayClear();
 display.displayText(s,PA_CENTER,65,0,PA_SCROLL_LEFT,PA_SCROLL_LEFT);
 display.displayReset();
}
void startCycle(unsigned long now){
 digitalWrite(GREEN_PIN,LOW);
 digitalWrite(BLUE_PIN,HIGH);
 txState=BLUE_START;
 wordIndex=charIndex=symbolIndex=0;
 deadline=now+START_GAP;
}
void startSymbol(unsigned long now){
 if(wordIndex>=wordCount){startCycle(now);return;}
 const char* code=morse(words[wordIndex][charIndex]);
 char symbol=code[symbolIndex];
 if(symbol!='.' && symbol!='-'){startCycle(now);return;}
 digitalWrite(GREEN_PIN,HIGH);
 txState=GREEN_ON;
 deadline=now+(symbol=='-'?3*UNIT:UNIT);
}
void stepMorse(unsigned long now){
 if(solved || (long)(now-deadline)<0)return;
 if(txState==BLUE_START){
  digitalWrite(BLUE_PIN,LOW);
  startSymbol(now);
  return;
 }
 if(txState==GREEN_OFF){
  startSymbol(now);
  return;
 }
 // Koniec błysku: dopiero teraz odmierzamy ciszę.
 digitalWrite(GREEN_PIN,LOW);
 const char* code=morse(words[wordIndex][charIndex]);
 symbolIndex++;
 if(code[symbolIndex]){
  deadline=now+UNIT; // przerwa wewnątrz litery
 }else{
  symbolIndex=0;
  charIndex++;
  if(words[wordIndex][charIndex]){
   deadline=now+LETTER_GAP; // przerwa między literami
  }else{
   wordIndex++;
   charIndex=0;
   deadline=now+(wordIndex<wordCount?WORD_GAP:3*UNIT);
  }
 }
 txState=GREEN_OFF;
}
void setup(){pinMode(BLUE_PIN,OUTPUT);pinMode(GREEN_PIN,OUTPUT);digitalWrite(BLUE_PIN,LOW);digitalWrite(GREEN_PIN,LOW);display.begin();display.setIntensity(2);showText("ENIGMA");startCycle(millis());}
void loop(){
 unsigned long now=millis();
 char key=keypad.getKey();
 if(key && !solved){
  if(key>='0'&&key<='9'&&entry.length()<5)entry+=key;
  else if(key=='<'&&entry.length())entry.remove(entry.length()-1);
  else if(key=='C')entry="";
  else if(key=='Z')startCycle(now); // S16 — restart Morse od początku
  else if(key=='='){
   if(entry=="94287"){solved=true;digitalWrite(BLUE_PIN,LOW);digitalWrite(GREEN_PIN,LOW);showText("BURZA");}
   else{entry="";showText("BLAD");temporaryUntil=now+1500;}
  }
  if(!solved && key!='='){showEntry();temporaryUntil=0;}
 }
 if(!solved){stepMorse(now);if(temporaryUntil && now>=temporaryUntil){temporaryUntil=0;showEntry();}}
 if(display.displayAnimate())display.displayReset();
}
