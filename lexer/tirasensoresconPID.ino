#include <QTRSensors.h>
#define NUM_SENSORS  8     // num sensores
#define TIMEOUT       2000  // espera
#define EMITTER_PIN   2     // led on
#define led1           5  
#define mot1          13
#define mot2          12
#define sensores      6

//NOTAS PARA ENCONTRAR VALORES DE PID
// KP constante proporcional para determinarla, comienzar por algo pequeño, e ir incrementado (el robot irá más lento entre más pequeño sea este parametro)
// KD Constante diferencial para determinar, aumentar lentamente las velocidades y ajuste este valor. (Nota: Kp <Kd)
 
QTRSensorsRC qtrrc((unsigned char[]) {4, 5, 6, 7, 8, 9, 10, 11},NUM_SENSORS, TIMEOUT, EMITTER_PIN);
 
unsigned int sensorValues[NUM_SENSORS];
unsigned int position=0;

//Ajustes PID 
int velocidad=120;              //vel max 255
float Kp=0.2, Kd=3, Ki=0.001;  //constantes
//tipolinea
int linea=0;                    //  0 negra, 1 blanca
int flanco_color =0;      // aumenta o disminuye el valor del sensado
int en_linea=3500;         //valor al que considerara si el sensor esta en linea o no
  
/// variables para el pid
int  derivativo=0, proporcional=0, integral=0; //parametros
int  salida_pwm=0, proporcional_pasado=0;
 
void setup()
{
 delay(800);
 pinMode(mot1, OUTPUT);// i1
 pinMode(mot2, OUTPUT);// d2
 pinMode(led1, OUTPUT); //led1
 
  int i;      
 for (int i = 0; i <40; i++)//calibracion 2.5 seg
 {                                
  digitalWrite(led1, HIGH);
  delay(20);
  qtrrc.calibrate();    //funcion para calibrar sensores   
  digitalWrite(led1, LOW);  
  delay(400);
 }
  digitalWrite(led1, HIGH); // fin calibracion 
  delay(2000);
  while(true)
   break;
}
 
 
void loop()
{
 
 //pid(linea valores 0 o 1, velocidad pwm, constante proporcional, constante integral,constante derivativa );
  pid(0,100,0.2,0.001,3); //algoritmo pid 
                                 
  //frenos_contorno(Linea blanca o negra,Intervalo de 0 a 1000 para ver si está en negro o blanco);
  frenos_contorno(0,700); //Función para curvas
}
 
//Control
 void pid(int linea, int velocidad, float Kp, float Ki, float Kd)
{
  position = qtrrc.readLine(sensorValues, QTR_EMITTERS_ON, linea); //0 para linea negra, 1 para linea blanca
  proporcional = (position) - 3500; // 3500 para centrar en la línea
  integral=integral + proporcional_pasado; //integral
  derivativo = (proporcional - proporcional_pasado); //derivativo
  if (integral>1000) integral=1000; //limitar integral a un rango
  if (integral<-1000) integral=-1000;
  salida_pwm =( proporcional * Kp ) + ( derivativo * Kd )+(integral*Ki);
   
  if (  salida_pwm > velocidad )  salida_pwm = velocidad; //limitar pwm
  if ( salida_pwm < -velocidad )  salida_pwm = -velocidad;
   
  if (salida_pwm < 0)
 {
  motores(velocidad+salida_pwm, velocidad);
 }
 if (salida_pwm >0)
 {
  motores(velocidad, velocidad-salida_pwm);
 }
 
 proporcional_pasado = proporcional;  
}
 
//funcion para control de motores
void motores(int motor1, int motor2)
{
  if ( motor1 >= 0 )  //motor 1
 {
  analogWrite(mot1,255-motor1);
 }
 else
 {
  motor1 = motor1*(-1); //cambio de signo
  analogWrite(mot1,motor1); 
 }
 
  if ( motor2 >= 0 ) //motor 2
 {
  analogWrite(mot2,255-motor2);
 }
 else
 {

  motor2= motor2*(-1);
  analogWrite(mot2,motor2);
 }
 
   
}
 
void frenos_contorno(int tipo,int flanco_comparacion)
{
   
if(tipo==0) //linea negra
{
  if(position<=50)
 {
  motores(0,90);
                                  
  while(true)  
  {
   qtrrc.read(sensorValues); //lectura de sensor   
   if( sensorValues[0]>flanco_comparacion || sensorValues[1]>flanco_comparacion ) 
   //asegurar que esta en linea
   {
    break;
   } 
  }
 }
 
 if (position>=6550) 
 { 
  motores(90,0);
  while(true)
  {
   qtrrc.read(sensorValues);
   if(sensorValues[7]>flanco_comparacion || sensorValues[6]>flanco_comparacion )
   {
    break;
   }  
  }
 }
}
 
if(tipo==1) //para linea blanca con fondo negro
{
 if(position<=50) 
 {
  motores(0,90); 
                   
  while(true)  
  {
   qtrrc.read(sensorValues); //lectura en bruto de sensor
   if(sensorValues[0]<flanco_comparacion || sensorValues[1]<flanco_comparacion )   //asegurar que esta en linea
   {
    break;
   }
  }
 }
 
 if(position>=6550)
 { 
  motores(90,0);
  while(true)
  {
   qtrrc.read(sensorValues);
   if(sensorValues[7]<flanco_comparacion || sensorValues[6]<flanco_comparacion)
   {
    break;
   }  
  }
 }
}
}
