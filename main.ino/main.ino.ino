#include <sensor_readings.h>

sensorReadings readingsObj;

void setup() {

  Serial.begin(115200);
  //Turpidity SET UP
  //add everything in to json object
  int NUM_SAMPLE = 1500;
  int WAIT_TIME = 0;
  String currDate = "key";
  String response = "{\" " + currDate + " \":[";
  Serial.print(response);
  for (int i = 0; i < NUM_SAMPLE; i++) {
    //Serial.println(i);
    if (i == NUM_SAMPLE - 1) {
      getSample();
      //response += getSample();
      break;
    } else {
      getSample();
      //response += getSample() + ",";
      Serial.print(",");
    }
    delay(WAIT_TIME);
  }
  Serial.println("]}");
  //response += "]}";
  //Serial.println(response);
}

void loop() {
  // put your main code here, to run repeatedly:
  return;
}

String getSample() {
  float turp = readingsObj.getTurpidity();
  float cond = readingsObj.getConductivity();
  float PH = readingsObj.getPH();
  float ORP = readingsObj.getORP();
  double TDS = readingsObj.getTDS();
  
  float temperature = readingsObj.TempProcess(readingsObj.ReadTemperature);  // read the current temperature from the  DS18B20
  readingsObj.TempProcess(readingsObj.StartConvert); 
  //after the reading,start the convert for next reading
  String response = "{\"Conductivity\":" + (String)cond + ", \"PH\":" + (String)PH + ", \"ORP\":" + (String)ORP + ", \"TDS\":" + (String)TDS + ", \"Turp\": " + (String)turp + ", \"Temperature\": " + (String)temperature + "}";
  Serial.print(response);
  return response;
}
