const String ver = "1.0";
const int analogInPin = A0; // Analog input pin
const int analogOutPin = 9; // Analog output pin that the LED is attached to
const int statusPin = 13;

//potentiometer
const int analogPotLeft = A1;
const int analogPotCenter = A2;
const int analogPotRight = A3;


 

//HARDWARE PARAMS
float maxOutV = 5.0; //your Arduino board maximal PWM output
//float maxRefInV = 1.1; //refernce analog input voltage for 1023 value! analogReference(INTERNAL); //1.1 V
float maxRefInV = 5.0;


float R = 470.0; //resistor for current feadback, Ohm

//CONFIGURABLE PARAMS
float target_mA = 0.5; //this current will be passed through your brain!!!
float epsilon_mA = 0.03; //maximal difference between target_mA and real current without correction
float max_mA = 2.0; //maximal difference between target_mA and real current without correction


//INIT GLOBALS
float outV = maxOutV; //voltage on PWM output
int state = -1; /*    -1 - brain is not detected, sorry)))
                       0 - voltage is changing to set target current
                       1 - all fine. you have target current
                  */


//FEEDBACK HELPERS
float computeOutVoltage(float V, float new_mA){
  if(abs(new_mA-target_mA)<epsilon_mA){ //current is fine enough
    state = 1;
    return V;
    }
  if(new_mA<0.01){
     state = -1; 
     return maxOutV;
    }
  float new_V = (target_mA/new_mA)*V; //voltage can be changed proportional to mA gain
  if(new_V>maxOutV){
    state = -1; //resistance is too big, no brain in chain?
    return maxOutV;
    //return maxOutV/5.0;//for safety
    }
  state = 0;
  return 0.1*new_V+0.9*V;//some output smoothing
  //return new_V;
  }

int convertVtoOutputValue(float V){
   return constrain(int(V/maxOutV*255), 0, 255);
  }

float sensorValue2mA(int sensorValue){
  float sensorVoltage = sensorValue/1023.0*maxRefInV;
  float sensor_mA = sensorVoltage/R*1000.0;
  return sensor_mA;
  }



void process_serial(){

  
  }

void process_feedback(){
  int sensorValue = analogRead(analogInPin);
  int potValue = analogRead(analogPotCenter);
  target_mA = potValue/1023.0*max_mA;
  float new_mA = sensorValue2mA(sensorValue);
  float V = outV;
  outV = computeOutVoltage(V, new_mA);
  analogWrite(analogOutPin, convertVtoOutputValue(outV));
  if(state == 1){
    digitalWrite(statusPin, HIGH);
  }else{
    digitalWrite(statusPin, LOW);
  }
  // print the results to the serial monitor:
  Serial.print("target_mA: "); Serial.print(target_mA); Serial.print("  ");
  Serial.print("new_mA: "); Serial.print(new_mA); Serial.print("  ");
  Serial.println("uT");


  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);  
  }


//SETUP AND MAIN LOOP
void setup() {
  pinMode(analogPotLeft, OUTPUT);
  pinMode(analogPotRight, OUTPUT);
  digitalWrite(analogPotLeft, LOW);
  digitalWrite(analogPotRight, HIGH);
  Serial.begin(115200);
  //analogReference(INTERNAL); //1.1 V
}

void loop(){
  process_feedback();


}
