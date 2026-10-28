/* Świat IV — Mechanizm Zatrzymanego Czasu
 * NodeMCU V3 (ESP8266), dwa L298N, cztery silniki DC 3–6 V.
 * Każdy silnik obraca się w jednym kierunku.
 * Na OBU L298N ZDEJMIJ zworki: ENA, ENB i 5V-EN.
 * IN1, IN3 -> +5V logiki; IN2, IN4 -> GND.
 * L298N 1: ENA -> D1, ENB -> D2.
 * L298N 2: ENA -> D5, ENB -> D6.
 * Każdy L298N: Vs/+12V -> +5V Xiaomi, 5V LOGIC -> +5V Xiaomi,
 * GND -> GND Xiaomi. NodeMCU: osobne USB 5V, wspólne GND.
 * NIE łącz dodatnich wyjść dwóch ładowarek.
 * L298N przy 5V może mieć za duży spadek napięcia.
 */
#include <Arduino.h>
const uint8_t MOTOR_PWM[4]={D1,D2,D5,D6};
const uint16_t MOTOR_SPEED[4]={1023,930,850,770};
const uint16_t STARTUP_MS=450;
const uint16_t START_DELAY_MS=650;
void setup(){
 analogWriteRange(1023);
 analogWriteFreq(1000);
 for(uint8_t i=0;i<4;i++){pinMode(MOTOR_PWM[i],OUTPUT);analogWrite(MOTOR_PWM[i],0);}
 delay(1200);
 for(uint8_t i=0;i<4;i++){
  analogWrite(MOTOR_PWM[i],1023);
  delay(STARTUP_MS);
  analogWrite(MOTOR_PWM[i],MOTOR_SPEED[i]);
  delay(START_DELAY_MS);
 }
}
void loop(){delay(1000);}
