#include <Servo.h> 
 
Servo clawturn, left, right, claw,base ;  // creates 4 "servo objects"

int ct_p,left_p,right_p,claw_p,base_p;

void setup() 
{ 
  Serial.begin(9600);
  right.attach(12);
  claw.attach(9);  // attaches the servo on pin 11 to the middle object
  clawturn.attach(10);  // attaches the servo on pin 10 to the left object
  base.attach(11);  // attaches the servo on pin 9 to the right object
  left.attach(13);  // attaches the servo on pin 6 to the claw object
  ct_p = 90;
  claw_p = 50;
  right_p = 50;
  left_p = 80;
  base_p = 90;//initialization values

} 
 
void loop() 
{ 
  right.write(right_p);
  claw.write(claw_p);
  clawturn.write(ct_p);
  left.write(left_p);
  base.write(base_p);
  delay(15);
  if ((millis() > 5000) && (base_p > 0))
  {
    base_p -= 2;
  }
}
