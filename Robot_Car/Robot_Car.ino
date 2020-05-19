/*
 * NOTE: * 
In order to keep everything simple Serial Communication uses
values from 0 to 3 to change Direction of DC Motors,
values 8 & 9 are used exclusively to turn off/on the lights
since ultrasonic sensor values are only reliable between 20-200cm
any distance further is non accurate enough to consider them as real values
*/


#include <Servo.h>
#include <DallasTemperature.h>
#include <OneWire.h>
#define trigPin 2
#define echoPin 3
#define ONE_WIRE_BUS 4 

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);            // Pass the oneWire reference to Dallas Temperature.
Servo servo;

//Parametros
const int Velocidad_Motor=115;



int value;
const int Led=12;
const float Longitude= 33.7;//Longitud de la Rueda
float DistanceRan=0;
int Res_Hall_Sens1=0;               //Contador de Iman1
int Hall_Sensor1;  //Lectura de Sensor Hall_1
bool Sensor1_Read=false;
unsigned long Time_Ref0=0;          //Tiempo de Referencia 0
unsigned long Time0;              //Tiempo de Rev 0
unsigned long previousMillis = 0;        // will store last time LED was updated
bool got_time=false;
// constants won't change:
const long interval = 100;           // interval at which to blink (milliseconds)
int Pos=0;
float Speed;                      //Velocidad
String Input_String;
bool String_Complete;

int vueltas=0;


int MeasureDistance(){
  long duration;
  int distance;
  digitalWrite(trigPin, LOW);
  
  delayMicroseconds(5);
 // Trigger the sensor by setting the trigPin high for 10 microseconds:
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read the echoPin. pulseIn() returns the duration (length of the pulse) in microseconds:
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance:
  distance = duration*0.034/2;
  
  if(distance>200){
    distance = 200;
  }
  if(distance<20){
    distance = 20;
  }
    delay(20);
  return distance;
}//Here ends the distance Range
  


void Data(){
  
  int Cal=501;  //Valor de Calibracion
  Hall_Sensor1=analogRead(A0);
  Serial.println("Hall Sensor "+String(Hall_Sensor1));
  delay(20);
  
  if( (Hall_Sensor1<500) || (Hall_Sensor1>600)){            //Deteccion del Primer Sensor
    
    if(Sensor1_Read == false){
    Res_Hall_Sens1++;
    Sensor1_Read=true;
    DistanceRan += Longitude;
    Serial.println("Vueltas:"+String(DistanceRan/33.7));
    delay(20);  
    }
    
    //Serial.println(Res_Hall_Sens1);
  }
  else{
    Sensor1_Read=false;
    Res_Hall_Sens1=Res_Hall_Sens1;
  }
  
  if(Res_Hall_Sens1==1){
      
      if(got_time==false){
      Time_Ref0=millis();
      //Serial.println("Tiempo Cero: "+String(Time_Ref0/1000));
      }
      got_time=true;
      delay(20);
    }
    
  if(Res_Hall_Sens1 >= 2){          //Termina la vuelta de la primera Rueda
    Res_Hall_Sens1 = 0;
    got_time = false;
    Time0 = millis();
    //Serial.println("Tiempo final de Rev: "+String(Time0/1000));
    
    unsigned long Time = Time0-Time_Ref0;
    unsigned long diff0 = Time/1000;
    //Serial.println("Tiempo de Revolucion: "+String(diff0));
             //Distancia Recorrida
    Speed = Longitude/diff0;         //Velocidad
  }
  
}

/*
void Data1(){
  if( (digitalRead(7)==HIGH) && Sensor1_Read==false ){
    vueltas++;
    Sensor1_Read=true;
    Serial.println("Vueltas: "+String(vueltas) );
  }
  else{
    Sensor1_Read=false;
  }
}
*/

void Serial_Commands(){
  
  while(Serial.available()){
    char inChar = (char)Serial.read();
    Input_String += inChar;  
    
    if (inChar == '\n') {
      String_Complete = true;
    }
    
  }
}//End Serial_Commands

void Motors(int Movement){
  value=Movement;

  switch (value){
    case 1:
      digitalWrite(6,LOW);
      digitalWrite(5,LOW);
    break;
    
    case 2:
      analogWrite(6,Velocidad_Motor);
      digitalWrite(5,LOW);
    break;

    case 3:
      analogWrite(5,Velocidad_Motor);
      digitalWrite(6,LOW);
      break;
  }//End Switch
  //analogWrite(9,110);
}

int ServoMove(int pos){
  servo.write(pos);
  return pos;
}

void setup() {
 
  Serial.begin(9600);
  servo.attach(11);
  sensors.begin();
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(7, INPUT);
  pinMode(Led,OUTPUT);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
}

void loop() {

  
  Serial_Commands();

    //Serial.println("Valor Enviado:"+Input_String);
    if (String_Complete==true) {

  if( (Input_String.toInt()>=1) &&((Input_String.toInt()<=4)) ) {
    Motors(Input_String.toInt());  
  }
  
  
  if( (Input_String.toInt()>=20) && (Input_String.toInt()<=160) ){
     Pos = ServoMove(Input_String.toInt());  
  }

  if((Input_String.toInt()==8)){
    digitalWrite(Led,HIGH);
  }
  if((Input_String.toInt()==9)){
    digitalWrite(Led,LOW);
  }
    // clear the string:
    Input_String = "";
    String_Complete = false;
  }
    int Distance_Measured = MeasureDistance();
 unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    

    sensors.requestTemperatures();               
     Data();
    Serial.println("Distance:"+String(Distance_Measured));
    Serial.println("Distancia Recorrida:" + String(DistanceRan));
    Serial.println("Velocidad:"+String(Speed));
    Serial.println("Temperatura:"+String(sensors.getTempCByIndex(0)));
    previousMillis = currentMillis;
    
  }

}
