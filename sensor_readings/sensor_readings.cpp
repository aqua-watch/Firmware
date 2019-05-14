#include "Arduino.h"
#include "sensor_readings.h"
#include <EEPROM.h>
#include "GravityTDS.h"
#include <OneWire.h>

#define samplingInterval 20
#define printinterval 0


sensorReadings SensorReadings;
GravityTDS gravityTds;


int orpArrayIndex = 0;

int pHArray[40];   //Store the average value of the sensor feedback
int pHArrayIndex = 0;

float temperature = 25, tdsValue = 0;

OneWire ds(SensorReadings.DS18B20_Pin);  // on digital pin 2



avergearray(int* arr, int number) {
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

/*Turpidity function*/
float sensorReadings::getTurpidity() {
  int sensorValue = analogRead(SensorReadings.turpPin);// read the input on analog pin 0:
  float voltage = sensorValue * (5.0 / 1024.0); // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  return voltage;
}

/*Conductivity functions*/

float sensorReadings::getConductivity() {
  float ECcurrent;
  float averageVoltage;
  int index;
  unsigned long AnalogSampleTime, printTime, tempSampleTime;
  AnalogSampleTime = millis();
  
  int ECReading = analogRead(SensorReadings.ECsensorPin);
 
  index = index + 1;
  if (index >= SensorReadings.ArrayLenth)
    index = 0;
  /*
    Every once in a while,MCU read the temperature from the DS18B20 and then let the DS18B20 start the convert.
    Attention:The interval between start the convert and read the temperature should be greater than 750 millisecond,or the temperature is not accurate!
  */
  tempSampleTime = millis();
  temperature = TempProcess(ReadTemperature);  // read the current temperature from the  DS18B20
  TempProcess(StartConvert);                   //after the reading,start the convert for next reading

  printTime = millis();
  averageVoltage = ECReading * (float)5000 / 1024;

  float TempCoefficient = 1.0 + 0.0185 * (temperature - 25.0); //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.0185*(fTP-25.0));
  float CoefficientVolatge = (float)averageVoltage / TempCoefficient;
  {
    if (CoefficientVolatge <= 448)ECcurrent = 6.84 * CoefficientVolatge - 64.32; //1ms/cm<EC<=3ms/cm
    else if (CoefficientVolatge <= 1457)ECcurrent = 6.98 * CoefficientVolatge - 127; //3ms/cm<EC<=10ms/cm
    else ECcurrent = 5.3 * CoefficientVolatge + 2278;                     //10ms/cm<EC<20ms/cm
    ECcurrent /= 1000;  //convert us/cm to ms/cm
  }

  return ECcurrent;
}



float sensorReadings::TempProcess(bool ch)
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
float sensorReadings::getPH() {
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue,voltage, analog_ph;
  int printInterval  = 800;
  if(millis()-samplingTime > samplingInterval)
  {
      // pHArray[pHArrayIndex++]=analogRead(SensorReadings.phPin);
      // if(pHArrayIndex==ArrayLenth)pHArrayIndex=0;
      analog_ph = analogRead(SensorReadings.phPin);
      voltage = analog_ph * 5.0 / 1024;
      pHValue = 3.5 * voltage + SensorReadings.OFFSET;
      samplingTime=millis();
  }
  return pHValue;
}

/* TDS functions*/

double sensorReadings::getTDS() {
  gravityTds.setPin(SensorReadings.TdsSensorPin);
  gravityTds.setAref(SensorReadings.VOLTAGE);  //reference voltage on ADC, default 5.0V on Arduino UNO
  gravityTds.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
  gravityTds.begin();  //initialization
  //temperature = readTemperature();  //add your temperature sensor and read it
  gravityTds.setTemperature(temperature);  // set the temperature and execute temperature compensation
  gravityTds.update();  //sample and calculate
  tdsValue = gravityTds.getTdsValue();  // then get the value
  return tdsValue;
}

/*ORP FUNCTION*/

int sensorReadings::getORP() {

  static unsigned long orpTimer = millis(); //analog sampling interval
  static unsigned long printTime = millis();

  orpTimer = millis() + 20;
  int ORPData = analogRead(SensorReadings.orpPin);
  int data[40];
  int temp;
  for (int i = 0 ; i < 40; i++) {
    temp = analogRead(SensorReadings.orpPin);
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

/******************  TESTS  ******************/

int sensorReadings::testAllSensors(){
  float ph = SensorReadings.getPH();
  int ORP = SensorReadings.getORP();
  double TDS = SensorReadings.getTDS();
  float cond = SensorReadings.getConductivity();
  float turb = SensorReadings.getTurpidity();

  //pH
  if(ph <= 0 || ph >= 14) return 0;
  //ORP
  if(ORP <= -2000 || ORP >= 2000) return 0; 
  //TDS
  if(TDS <= 0 || TDS > 1000) return 0;
  //Conductivity
  if(cond < 1 || cond > 15) return 0;
  //TODO write a test for turb
  if(turb <= 0) return 0;
  return 1;
}