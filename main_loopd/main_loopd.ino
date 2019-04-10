#include <EEPROM.h>
#include "GravityTDS.h"
#include <OneWire.h>
#include "DFRobot_EC.h"


#define VOLTAGE 5.00    //system voltage
#define OFFSET 0        //zero drift voltage
#define LED 13         //operating instructions

#define TdsSensorPin 0
#define orpPin 1          //orp meter output,connect to Arduino controller ADC pin
#define SensorPin 3            //pH meter Analog output to Arduino Analog Input 0
byte ECsensorPin = 2;  //EC Meter analog output,pin on analog 1
byte DS18B20_Pin = 2; //DS18B20 signal, pin on digital 2
#define turpPin A5
/*ORP Variables*/
#define ArrayLenth  40    //times of collection
int orpArray[ArrayLenth];
int orpArrayIndex = 0;

#define SAMPLE_DELAY_TIME 0
#define SAMPLE_SIZE 50

/*TDS Variables*/

GravityTDS gravityTds;
DFRobot_EC ec;

float temperature = 25, tdsValue = 0;

/*PH varialbes*/

#define Offset 0.00            //deviation compensate 
#define samplingInterval 20
#define printinterval 800

int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex = 0;

/*Conductivity variables*/
#define StartConvert 0
#define ReadTemperature 1

const byte numReadings = 20;     //the number of sample times

unsigned int AnalogSampleInterval = 25, printInterval = 700, tempSampleInterval = 850; //analog sample interval;serial print interval;temperature sample interval
unsigned int readings[numReadings];      // the readings from the analog input
byte index = 0;                  // the index of the current reading
unsigned long ECReading = 0;                  // the running total
unsigned int AnalogAverage = 0, averageVoltage = 0;             // the average
unsigned long AnalogSampleTime, printTime, tempSampleTime;
float ECcurrent;

//Temperature chip i/o
OneWire ds(DS18B20_Pin);  // on digital pin 2

void setup() {

  Serial.begin(9600);
  
  //TDS SET UP
  gravityTds.setPin(TdsSensorPin);
  gravityTds.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
  gravityTds.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
  gravityTds.begin();  //initialization

  //PH SET UP

  //Conductivity SET UP
  // initialize all the readings to 0:
  for (byte thisReading = 0; thisReading < numReadings; thisReading++)
    readings[thisReading] = 0;
  TempProcess(StartConvert);   //let the DS18B20 start the convert
  AnalogSampleTime = millis();
  printTime = millis();
  tempSampleTime = millis();
 
}

void loop() {
  String currDate = "9/20/2018";
  String response = "{\" " + currDate + " \":[";
  int incomingByte;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    if (i >= SAMPLE_SIZE-1) {
      response += getSample();
    } else {
      response += getSample() + ",";
    }
    
  }
  response += "]}";
  Serial.println(response);
  
  while (Serial.available() <= 0);
  while (Serial.available()) {
    Serial.read();
  }
      // read the incoming byte:


}

String getSample() {
  float turp = getTurpidity();
  float cond = getConductivity();
  float PH = getPH();
  float ORP = getORP();
  double TDS = getTDS();
  
  float temperature = TempProcess(ReadTemperature);  // read the current temperature from the  DS18B20
  TempProcess(StartConvert); 
  //after the reading,start the convert for next reading
  String response = "{\"Conductivity\":" + (String)cond + ", \"PH\":" + (String)PH + ", \"ORP\":" + (String)ORP + ", \"TDS\":" + (String)TDS + ", \"Turp\": " + (String)turp + ", \"Temperature\": " + (String)temperature + "}";
  //Serial.println(response);
  return response;
}

/*Turpidity function*/
float getTurpidity() {
  int sensorValue = analogRead(A5);// read the input on analog pin 0:
  float voltage = sensorValue * (5.0 / 1024.0); // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  return voltage;
}

/*Conductivity functions*/

float getConductivity() {
  /*
    Every once in a while,sample the analog value and calculate the average.
  */

   float voltage = analogRead(ECsensorPin)/1024.0*5000;   // read the voltage
   temperature = TempProcess(ReadTemperature);  // read the current temperature from the  DS18B20
   TempProcess(StartConvert);                   //after the reading,start the convert for next reading
    //after the reading,start the convert for next reading
   float ecValue =  ec.readEC(voltage,temperature);  // convert voltage to EC with temperature compensation

  return ecValue;
}



float TempProcess(bool ch)
{
  //returns the temperature from one DS18B20 in DEG Celsius
  static byte data[12];
  static byte addr[8];
  static float TemperatureSum;
  if (!ch) {
    if ( !ds.search(addr)) {
      //Serial.println("no more sensors on chain, reset search!");
      ds.reset_search();
      return 0;
    }
    if ( OneWire::crc8( addr, 7) != addr[7]) {
      Serial.println("CRC is not valid!");
      return 0;
    }
    if ( addr[0] != 0x10 && addr[0] != 0x28) {
      Serial.print("Device is not recognized!");
      return 0;
    }
    ds.reset();
    ds.select(addr);
    ds.write(0x44, 1); // start conversion, with parasite power on at the end
  }
  else {
    byte present = ds.reset();
    ds.select(addr);
    ds.write(0xBE); // Read Scratchpad
    for (int i = 0; i < 9; i++) { // we need 9 bytes
      data[i] = ds.read();
    }
    ds.reset_search();
    byte MSB = data[1];
    byte LSB = data[0];
    float tempRead = ((MSB << 8) | LSB); //using two's compliment
    TemperatureSum = tempRead / 16;
  }
  return TemperatureSum;
}

/* PH functions*/
double getPH() {
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue, voltage;
  pHArray[pHArrayIndex++] = analogRead(SensorPin);
  int PHsensorVal = analogRead(SensorPin);

  voltage = PHsensorVal * 5.0 / 1024;

  pHValue = 3.5 * voltage + Offset;
  samplingTime = millis();
  return pHValue;
  
}

/* TDS functions*/

double getTDS() {
  //temperature = readTemperature();  //add your temperature sensor and read it
  gravityTds.setTemperature(temperature);  // set the temperature and execute temperature compensation
  gravityTds.update();  //sample and calculate
  tdsValue = gravityTds.getTdsValue();  // then get the value
  //Serial.print(tdsValue,0);
  //Serial.println("ppm");


  return tdsValue;

}

/*ORP FUNCTION*/

int getORP() {

  static unsigned long orpTimer = millis(); //analog sampling interval
  static unsigned long printTime = millis();

  orpTimer = millis() + 20;
  int ORPData = analogRead(orpPin);
  int data[40];
  int temp;
  for (int i = 0 ; i < 40; i++) {
    temp = analogRead(orpPin);
    data[i] = ((30 * (double)2.0 * 1000) - (75 * temp * 5.0 * 1000 / 1024)) / 75 - OFFSET;
  }

  double finalVal = avergearray(data, 10);

  if (orpArrayIndex == ArrayLenth) {
    orpArrayIndex = 0;
  }
  int orpValue = ((30 * (double)5.0 * 1000) - (75 * ORPData * 5.0 * 1000 / 1024)) / 75 - OFFSET;
  return ((int)orpValue);
  //return finalVal;
}


double avergearray(int* arr, int number) {
  int i;
  int max, min;
  double avg;
  long amount = 0;
  if (number <= 0) {
    printf("Error number for the array to avraging!/n");
    return 0;
  }
  if (number < 5) { //less than 5, calculated directly statistics
    for (i = 0; i < number; i++) {
      amount += arr[i];
    }
    avg = amount / number;
    return avg;
  } else {
    if (arr[0] < arr[1]) {
      min = arr[0]; max = arr[1];
    }
    else {
      min = arr[1]; max = arr[0];
    }
    for (i = 2; i < number; i++) {
      if (arr[i] < min) {
        amount += min;      //arr<min
        min = arr[i];
      } else {
        if (arr[i] > max) {
          amount += max;  //arr>max
          max = arr[i];
        } else {
          amount += arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount / (number - 2);
  }//if
  return avg;
}

byte stringChecksum(char *s)
{
  byte c = 0;
  while (*s != '\0')
    c ^= *s++;
  return c;
}
