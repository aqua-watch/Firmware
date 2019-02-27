#include <EEPROM.h>
#include "GravityTDS.h"
#include <OneWire.h>

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

#define SAMPLE_DELAY_TIME 500
#define SAMPLE_SIZE 50

/*TDS Variables*/

GravityTDS gravityTds;
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

  if (Serial.available() > 0) {
      // read the incoming byte:
      incomingByte = Serial.read();
  }
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
  Serial.println(response);
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

  AnalogSampleTime = millis();
  // subtract the last reading:
  //ECReading = ECReading - readings[index];
  // read from the sensor:
  int ECReading = analogRead(ECsensorPin);
  //readings[index] = analogRead(ECsensorPin);

  // add the reading to the total:
  //ECReading = ECReading + readings[index];
  // advance to the next position in the array:
  index = index + 1;
  // if we're at the end of the array...
  if (index >= numReadings)
    // ...wrap around to the beginning:
    index = 0;
  // calculate the average:
  //AnalogAverage = ECReading / numReadings;

  /*
    Every once in a while,MCU read the temperature from the DS18B20 and then let the DS18B20 start the convert.
    Attention:The interval between start the convert and read the temperature should be greater than 750 millisecond,or the temperature is not accurate!
  */

  tempSampleTime = millis();
  temperature = TempProcess(ReadTemperature);  // read the current temperature from the  DS18B20
  TempProcess(StartConvert);                   //after the reading,start the convert for next reading

  /*
    Every once in a while,print the information on the serial monitor.
  */

  printTime = millis();
  averageVoltage = ECReading * (float)5000 / 1024;
  /*
    Serial.print("Analog value:");
    Serial.print(ECReading);   //analog average,from 0 to 1023
    Serial.print("    Voltage:");
    Serial.print(averageVoltage);  //millivolt average,from 0mv to 4995mV
    Serial.print("mV    ");
    Serial.print("temp:");
    Serial.print(temperature);    //current temperature
    Serial.print("^C     EC:");*/

  float TempCoefficient = 1.0 + 0.0185 * (temperature - 25.0); //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.0185*(fTP-25.0));
  float CoefficientVolatge = (float)averageVoltage / TempCoefficient;
  if (CoefficientVolatge < 150)Serial.println("No solution!"); //25^C 1413us/cm<-->about 216mv  if the voltage(compensate)<150,that is <1ms/cm,out of the range
  else if (CoefficientVolatge > 3300)Serial.println("Out of the range!"); //>20ms/cm,out of the range
  else
  {
    if (CoefficientVolatge <= 448)ECcurrent = 6.84 * CoefficientVolatge - 64.32; //1ms/cm<EC<=3ms/cm
    else if (CoefficientVolatge <= 1457)ECcurrent = 6.98 * CoefficientVolatge - 127; //3ms/cm<EC<=10ms/cm
    else ECcurrent = 5.3 * CoefficientVolatge + 2278;                     //10ms/cm<EC<20ms/cm
    ECcurrent /= 1000;  //convert us/cm to ms/cm
    //Serial.print(ECcurrent,2);  //two decimal
    //Serial.println("ms/cm");
  }

  return ECcurrent;
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
