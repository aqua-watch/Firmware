int conductPin = A2;     // conductivity connected to digital pin 2
int turbPin = 4;
int TDSPin = 6;
int PHPin = A2;
int ORDPin = 10;



void setup()
{
  Serial.begin(9600);
  pinMode(conductPin, INPUT);        
  pinMode(turbPin, INPUT);
  pinMode(TDSPin, INPUT);        
  pinMode(PHPin, INPUT);
  pinMode(ORDPin, INPUT);        
  
  
  Serial.println("Getting started");
  readAll();
}

void readAll()
{
  float conduct = analogRead(conductPin);
  float turb = analogRead(turbPin);
  float TDS = analogRead(TDSPin);
  float PH = analogRead(PHPin);
  float ORP = analogRead(ORDPin);
  

  
  Serial.print(conduct);
  Serial.println("Seimens");

  Serial.print(turb);
  Serial.println("Turbs");

  Serial.print(TDS);
  Serial.println("TDS's");
  
  Serial.print(PH);
  Serial.println("PH's");  
  
  Serial.print(ORP);
  Serial.println("ORP's");  
  
}


void loop()
{
  return;
  //val = digitalRead(inPin);     // read the input pin
  //Serial.println(val);    // sets the LED to the button's value
}
