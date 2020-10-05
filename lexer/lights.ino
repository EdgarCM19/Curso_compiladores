#include"notes_bits.h"

const int latchPin = 9;
const int clockPin = 8;
const int dataPin = 10;

int pitch, cmd, velocity;
int light;
boolean state;

byte lightData1 = 0, lightData2 = 0, lightData3 = 0; 

void setup() {
    pinMode(latchPin, OUTPUT);
    pinMode(dataPin, OUTPUT);  
    pinMode(clockPin, OUTPUT);
    Serial.begin(38400);
}

void loop() {
    if(Serial.available()>2) {
        cmd = Serial.read();
        pitch = Serial.read();
        velocity = Serial.read();

        //the lights are set according to the data on MIDI ch.1
        if(cmd==144) state=0;               
        else if(cmd==128) state=1;        

        // so that lights don't change while the new data is being shifted
        digitalWrite(latchPin, LOW);

        light = getBit(pitch);
        if(light<8)
        bitWrite(lightData1, light, state);
        else if(light<16){
        light-=8;
        bitWrite(lightData2, light, state);
        }
        else {
        light-=16;
        bitWrite(lightData3, light, state);
        }
        // shift out the data
        shiftOut(dataPin, clockPin, MSBFIRST, lightData3);
        shiftOut(dataPin, clockPin, MSBFIRST, lightData2);
        shiftOut(dataPin, clockPin, MSBFIRST, lightData1);

        // turn on the lights according to the new data
        digitalWrite(latchPin, HIGH);
    }
}