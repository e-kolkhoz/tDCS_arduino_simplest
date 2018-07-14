const String ver = "1.0";
const int analogInPin = A0; // Analog input pin
const int analogOutPin = 9; // Analog output pin that the LED is attached to


//HARDWARE PARAMS
float maxOutV = 5.0; //your Arduino board maximal PWM output
float maxRefInV = 1.1; //refernce analog input voltage for 1023 value! analogReference(INTERNAL); //1.1 V


float R = 470.0; //resistor for current feadback, Ohm

//CONFIGURABLE PARAMS
float target_mA = 0.5; //this current will be passed through your brain!!!
float epsilon_mA = 0.03; //maximal difference between target_mA and real current without correction


//INIT GLOBALS
float outV = maxOutV; //voltage on PWM output
int state = -10; /*    -1 - brain is not detected, sorry)))
                       0 - voltage is changing to set target current
                       1 - all fine. you have target current
                     -10 - turn V off
                  */
int debounced_state = 0; //for debounce
int zeros_len = 0; //for debounce
float smoothed_mA=0;

String commandString = ""; //for CLI

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

int debounced_state_compute(int state){
  if(state < 0) {
    zeros_len = 0;
    return state;
  }
  if(state == 1){ // 1 has priority
    zeros_len = 0;
    return 1; 
  }
  if(debounced_state == 0){
    return 0;    
  }
  if(state == 0){
    zeros_len++;
    if(zeros_len>5) return 0; //only long sequence of zeros makes 0
  }
  return 1;
}

void process_feedback(){
  int sensorValue = analogRead(analogInPin);
  float new_mA = sensorValue2mA(sensorValue);
  smoothed_mA = 0.2*new_mA+0.8*smoothed_mA;
  float V = outV;
  outV = computeOutVoltage(V, new_mA);
  analogWrite(analogOutPin, convertVtoOutputValue(outV));

  // print the results to the serial monitor:
  debounced_state = debounced_state_compute(state);
  Serial.print("V = ");
  Serial.print(V);
  Serial.print("\t target_mA = ");
  Serial.print(target_mA);
  Serial.print("\t smoothed_mA = ");
  Serial.print(smoothed_mA);
  Serial.print("\t debounced_state = ");
  Serial.println(debounced_state);

  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);  
  }

void stop_device(){
  state = -10;
  analogWrite(analogOutPin, 0);  
  }



//CLI HELPERS
void clearAndHome() 
{ 
  Serial.write(27); 
  Serial.print("[2J"); // clear screen 
  Serial.write(27); // ESC 
  Serial.print("[H"); // cursor to home 
}

void help(){
  Serial.println("tDSC arduino, ver "+ver);
  Serial.println("'?' - help");
  Serial.println("'target_mA X' - set target mA to X");
  Serial.println("'epsilon_mA X' - set epsilon_mA mA to X");
  Serial.println("'start' - start the brain stimulation");
  Serial.println("*command needs escape value at the end (byte 13)");
  Serial.print("status: target_mA = ");
  Serial.print(target_mA);
  Serial.print(" epsilon_mA = ");
  Serial.println(epsilon_mA);
  }

bool parse_param(String &cmdString){
  int spacePos = cmdString.indexOf(' ');
  if(spacePos<=0) return false;  
  String command = cmdString.substring(0, spacePos);
  String fval = cmdString.substring(spacePos+1);
  float val = fval.toFloat();
  if(command=="target_mA"){    
    if(val<=0.0 or val>2.0){
      return false;
      }
    target_mA = val;
  }else if(command=="epsilon_mA"){
    if(val<=0.0 or val>0.3){
      return false;
    }
    epsilon_mA = val;
  }else if(command=="R"){
    R = val;
  }else{
    return false;  
  }
  return true;
}

//SETUP AND MAIN LOOP
void setup() {
  Serial.begin(115200);
  analogReference(INTERNAL); //1.1 V
}

void loop(){
  if(state!=-10){
    process_feedback();
    }
  if (Serial.available() > 0){      
      char v = Serial.read();
      if (v == '?'){
        stop_device();
        }      
      if (byte(v) == 13){         
         if (commandString=="?"){
                clearAndHome();
                help();
         }else if (commandString == "stop"){
                stop_device();
         }else if (commandString == "start"){
                state = -1;
                outV = maxOutV/5.0;
         }else{//         
                bool ok = parse_param(commandString);
                if(!ok){
                  Serial.println("!unrecognized " + commandString);
                }
         }   
         commandString = "";
      }else{
         commandString+=v;
         if(state==-10){
            Serial.print(v);
         }
      }      
   }
  

  

}
