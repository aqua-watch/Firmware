
/*
 * sensor readings.h 
 */


#ifndef sensorReadings_h

//	The #define statement defines this file as the myFirstLibrary
//	Header File so that it can be included within the source file.                                           
#define sensorReadings_h

//	The #include of Arduino.h gives this library access to the standard
//	Arduino types and constants (HIGH, digitalWrite, etc.). It's 
//	unneccesary for sketches but required for libraries as they're not
//	.ino (Arduino) files.
#include "Arduino.h"

class sensorReadings{

	public:
	
		float getTurpidity();
        float getConductivity();
        float TempProcess(bool ch);
        double getPH();
        double getTDS();
        int getORP();
        int StartConvert = 0;
        int ReadTemperature = 1;
        int ArrayLenth = 40;    //times of collection
        float VOLTAGE = 5.0;
        float OFFSET = 0;
        int LED = 13;
        int TdsSensorPin = 4;
        int orpPin = 1  ;        //orp meter output,connect to Arduino controller ADC pin
        int phPin = 3 ;           //pH meter Analog output to Arduino Analog Input 0
        unsigned char ECsensorPin = 2;  //EC Meter analog output,pin on analog 1
        unsigned char  DS18B20_Pin = 2; //DS18B20 signal, pin on digital 2
        int turpPin = 5;
        
	private:         

		
        
};

//	The end wrapping of the #ifndef Include Guard
#endif