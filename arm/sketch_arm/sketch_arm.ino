#include <Servo.h> 
 
// create "servo objects"
Servo extend, updown, claw, clawturn, base; //extend is left, updown is right servo

int ct_p, extend_p, updown_p, claw_p, base_p;
int updown_flag = 0;
int extend_flag = 0;
int base_flag = 0;
void setup() 
{ 
  Serial.begin(9600); 
  claw.attach(9);  // attaches the servo on pin 11 to the middle object
  clawturn.attach(10);  
  base.attach(11);
  extend.attach(13); 
  updown.attach(12);
  
  ct_p = 50;
  claw_p = 50;
  updown_p = 20; //up down, 0 is up
  extend_p = 70; // 90 is retracted in, 10 is extended out
  base_p = 0;//initialization values
  //20 to 80 is our range for right_p AKA updown

  claw.write(claw_p);
  clawturn.write(ct_p);
  
  updown.write(updown_p);
  extend.write(extend_p);
  base.write(base_p);
} 
 
void loop() 
{ 
  base.write(base_p);
    
  if(base_p == 0 && updown_p == 20){ //in position zero
    delay(500);
    while(updown_p < 80 ){ //move claw down
      updown_p+=1;
      updown.write(updown_p); //go down to 80
      delay(35);
    }
    delay(2000);
    while(updown_p > 20 ){ //move claw back up
      updown_p-=1;
      updown.write(updown_p); //go up to 20
      delay(35); 
    }
    delay(500);
    base_flag = 1;
    }else if(base_p == 90 && updown_p == 20){ //in poistion 90
      delay(500);
      while(updown_p < 80 ){ //move claw down
        updown_p+=1;
        updown.write(updown_p); //go down to 80
        delay(35);
      } 
      delay(2000);
      while(updown_p > 20 ){ //move claw back up
        updown_p-=1;
        updown.write(updown_p); //go up to 20
        delay(35); 
      }
      delay(500);
      base_flag = 0;
     }
  delay(35);
  if ((base_p > 0) && base_flag == 0){
    base_p -= 1;
  }else if(base_flag == 1){
      base_p += 1;
    }
}
