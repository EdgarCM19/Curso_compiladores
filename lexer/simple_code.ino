int led = 13; // the pin the LED is connected to
int algo = 0x3dfe45;
float x = 0.13f ? algo < 1 : 3.4f;
void setup() {
  pinMode(led, OUTPUT) // Declare the LED as an output
}

led++;
led += 3;
/*
nada más para ver
*/
void loop() {
  digitalWrite(led, HIGH) // Turn the LED on
}
