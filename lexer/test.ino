#include <Firmata.h>

int led = 13; 
int algo = 0x3dfe45;
int algo = 0x3dfe45;
const int BUTTON = X < Y ? HIGH : LOW;
void setup() {
  pinMode(led, OUTPUT); 
  Serial.begin(9600);
}

led++; //Comentario
led += 3;
/*
nada más para ver
*/
void loop() {
  digitalWrite(led, HIGH);
  if(led >= 0)
    Serial.write("Cadena");
  else
    Serial.wite("Otra cosa");
    for(i=0 ; i < 10; i++){
      algo += i + 2;
    }
}


