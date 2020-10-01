
#include <AFMotor.h>


  
//Motores 1=IA,2=DA,3=DE,4=IE
AF_DCMotor M1(1);//Atras Izquierda
AF_DCMotor M2(2);//Atras Derecha
AF_DCMotor M3(3);//Enfrente Derecha
AF_DCMotor M4(4);//Enfrente Izquierda


int rot=255;
int vel=200;
int timRot=600;
int timMov=600;

int envioPulso =35;
// Los pines deben ser modificados entre 31-39
int pulsoAtras=33;//Azul
int pulsoIzquierda=31;//Gris
int pulsoDerecha=39;//Rosa
int pulsoFrenteD=37;//Verde
//int pulsoFrenteI=28;//Blanco

void setup() {
  Serial.begin(9600);
  pinMode(envioPulso,OUTPUT);
  pinMode(pulsoAtras,INPUT);
  pinMode(pulsoFrenteD,INPUT);
  //pinMode(pulsoFrenteI,INPUT);
  pinMode(pulsoDerecha,INPUT);
  pinMode(pulsoIzquierda,INPUT);
  M1.setSpeed(100);
  M2.setSpeed(100);
  M3.setSpeed(100);
  M4.setSpeed(100);
  M1.run(RELEASE);
  M2.run(RELEASE);
  M3.run(RELEASE);
  M4.run(RELEASE);
}
boolean verDerecha(){
  long t1;
  long d1;
  digitalWrite(envioPulso,HIGH);
  delay(10);
  digitalWrite(envioPulso,LOW);
  t1=pulseIn(pulsoDerecha,HIGH);
  delay(10);
  d1=t1/59;
  if(d1>3500 || d1<4){
    delay(50);
    digitalWrite(envioPulso,HIGH);
    delay(10);
    digitalWrite(envioPulso,LOW);
    t1=pulseIn(pulsoDerecha,HIGH);
    delay(10);
    d1=t1/59;
  }
  Serial.print("Derecha ");
  Serial.println(d1);
  if(d1>35){
    return true;
  }else{
    return false;
  }
}
boolean verIzquierda(){
  long t1;
  long d1;
  digitalWrite(envioPulso,HIGH);
  delay(10);
  digitalWrite(envioPulso,LOW);
  t1=pulseIn(pulsoIzquierda,HIGH);
  delay(10);
  d1=t1/59;
  if(d1>3500 || d1<4){
    delay(50);
    digitalWrite(envioPulso,HIGH);
    delay(10);
    digitalWrite(envioPulso,LOW);
    t1=pulseIn(pulsoIzquierda,HIGH);
    delay(10);
    d1=t1/59;
  }
  Serial.print("Izquierda ");
  Serial.println(d1);
  if(d1>35){
    return true;
  }else{
    return false;
  }
}
boolean verFrente(){
  long t1,t2;
  long d1,d2;
  digitalWrite(envioPulso,HIGH);
  delay(10);
  digitalWrite(envioPulso,LOW);
  t2=pulseIn(pulsoFrenteD,HIGH);
  delay(10);
  d2=t2/59;
  if(d2>3500 || d2<4){
    delay(50);
    digitalWrite(envioPulso,HIGH);
    delay(10);
    digitalWrite(envioPulso,LOW);
    t2=pulseIn(pulsoFrenteD,HIGH);
    delay(10);
    d2=t2/59;
  }
  Serial.print("Frente 2 ");
  Serial.println(d2);
  if(d2>35){
    return true;
  }else{
    return false;
  }
}
boolean verAtras(){
  long t1;
  long d1;
  digitalWrite(envioPulso,HIGH);
  delay(10);
  digitalWrite(envioPulso,LOW);
  t1=pulseIn(pulsoAtras,HIGH);
  delay(10);
  d1=t1/59;
  if(d1>3500 || d1<4){
    delay(50);
    digitalWrite(envioPulso,HIGH);
    delay(10);
    digitalWrite(envioPulso,LOW);
    t1=pulseIn(pulsoAtras,HIGH);
    delay(10);
    d1=t1/59;
  }    
  Serial.print("Atras ");
  Serial.println(d1);
  if(d1>35){
    return true;
  }else{
    return false;
  }
}
void avanzar(){
  M1.run(FORWARD);
  M2.run(FORWARD);
  M3.run(FORWARD);
  M4.run(FORWARD);
  delay(timMov);
  M1.run(RELEASE);
  M2.run(RELEASE);
  M3.run(RELEASE);
  M4.run(RELEASE);
  delay(500);
}
void girarDerecha(){
    M1.setSpeed(rot);
    M2.setSpeed(rot);
    M3.setSpeed(rot);
    M4.setSpeed(rot);
    M1.run(FORWARD);
    M2.run(BACKWARD);
    M3.run(BACKWARD);
    M4.run(FORWARD);  
    delay(timRot);
    M1.run(RELEASE);
    M2.run(RELEASE);
    M3.run(RELEASE);
    M4.run(RELEASE);
    M1.setSpeed(vel);
    M2.setSpeed(vel);
    M3.setSpeed(vel);
    M4.setSpeed(vel);
    delay(500);
}
void girarIzquierda(){
    M1.setSpeed(rot);
    M2.setSpeed(rot);
    M3.setSpeed(rot);
    M4.setSpeed(rot);
    M1.run(BACKWARD);
    M2.run(FORWARD);
    M3.run(FORWARD);
    M4.run(BACKWARD);
    delay(timRot);
    M1.run(RELEASE);
    M2.run(RELEASE);
    M3.run(RELEASE);
    M4.run(RELEASE);
    M1.setSpeed(vel);
    M2.setSpeed(vel);
    M3.setSpeed(vel);
    M4.setSpeed(vel);
    delay(500);
}
void loop() {
  if(verDerecha()){
     girarDerecha();
     avanzar();
  }else{
     if(verFrente()){
        avanzar();
     }else{
        if(verIzquierda()){
          girarIzquierda();
          avanzar();
        }else{
          if(verAtras()){
            girarDerecha();
            girarDerecha();
            avanzar();
          }else{
            delay(100);
          }
       }
    }
  }
  //delay(2000);
  //girarDerecha();
}
