/* Świat IV — Mechanizm Zatrzymanego Czasu
 * WERSJA: JEDEN SILNIK i cztery wymienne tarcze.
 *
 * NodeMCU V3 (ESP8266), jeden kanał L298N, jeden silnik DC 3–6 V.
 * Połączenia jak w dawnym kanale pierwszego silnika:
 *   ENA -> D1 (PWM), IN1 -> +5 V logiki, IN2 -> GND.
 *   Zdejmij zworkę ENA przed podłączeniem PWM.
 *
 * Zasilanie L298N zgodnie z użytym modułem i jego dokumentacją.
 * Nie łącz plusów dwóch niezależnych zasilaczy; zapewnij wspólną masę.
 * L298N powoduje znaczny spadek napięcia, zwłaszcza przy zasilaniu 5 V.
 * Przed zmianą przewodów zawsze odłącz zasilanie.
 *
 * UWAGA: dorosły wyłącza silnik i czeka na całkowite zatrzymanie
 * przed zdjęciem lub przyklejeniem kolejnej tarczy. Stosuj osłonę.
 */
#include <Arduino.h>

const uint8_t MOTOR_PWM = D1;
const uint16_t MOTOR_SPEED = 1023; // 0..1023, dostrój po próbie sprzętowej
const uint16_t STARTUP_MS = 450;

void setup() {
  analogWriteRange(1023);
  analogWriteFreq(1000);
  pinMode(MOTOR_PWM, OUTPUT);
  analogWrite(MOTOR_PWM, 0);
  delay(1200);
  analogWrite(MOTOR_PWM, 1023); // rozruch
  delay(STARTUP_MS);
  analogWrite(MOTOR_PWM, MOTOR_SPEED);
}

void loop() {
  delay(1000);
}
