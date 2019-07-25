#include "DualVNH5019MotorShield.h"



#define V_MAX 500
#define V_STEP 25

#define CMD_RATE 40

#define MSG_SIZE 10

#define POLY 0x8408

DualVNH5019MotorShield md;


unsigned long next_cmd_time_;
int m1_cmd_ = 0;
int m2_cmd_ = 0;
int target_v1_ = 0;
int target_v2_ = 0;
char rx_buffer_[MSG_SIZE];
int next_write_ = 0;
bool msg_complete_ = false;




void stopIfFault()
{
  if (md.getM1Fault())
  {
    Serial.println("M1 fault");
    while(1);
  }
  if (md.getM2Fault())
  {
    Serial.println("M2 fault");
    while(1);
  }
}

int calculateCommand(int current_speed, int target_speed)
{
  int error;
  int command;

  // Make sure target is within legal range
  if (abs(target_speed) > V_MAX)
  {
    target_speed = V_MAX * (target_speed / abs(target_speed));
  }

  // Calculate error
  error = target_speed - current_speed;

  if (abs(error) < V_STEP)
  {
    command = target_speed;
  }
  else
  {
    command = current_speed + V_STEP * (error / abs(error));
  }

  return command;
  
}




// Checksum
unsigned short crc16(char *data_p, unsigned short length)
{
  unsigned char i;
  unsigned int data;
  unsigned int crc = 0x0000;

  if (length == 0)
    return (~crc);

  do
  {
    for (i=0, data=(unsigned int)0xff & *data_p++;
         i < 8; 
         i++, data >>= 1)
    {
          if ((crc & 0x0001) ^ (data & 0x0001))
                crc = (crc >> 1) ^ POLY;
          else  crc >>= 1;
    }
  } while (--length);


  return (crc);
}



void setup()
{
  Serial.begin(115200);
  Serial.println("Dual VNH5019 Motor Shield");
  md.init();
  next_cmd_time_ = millis();
}

void loop()
{
    unsigned long current_time = millis();

    if (msg_complete_)
    {
      target_v1_ = (int)( (rx_buffer_[1] << 8) | (rx_buffer_[2]) );
      target_v2_ = (int)( (rx_buffer_[3] << 8) | (rx_buffer_[4]) );
      msg_complete_ = false;
    }

    if (current_time > next_cmd_time_)
    {
      m1_cmd_ = calculateCommand(m1_cmd_, target_v1_);
      m2_cmd_ = calculateCommand(m2_cmd_, target_v2_);
      next_cmd_time_ += 1000 / CMD_RATE;

    }
    
    md.setM1Speed(m1_cmd_);
    md.setM2Speed(m2_cmd_);
    stopIfFault();
    
    


 
}


void serialEvent()
{
  int bytes_read = 0;
  
  while (Serial.available() && bytes_read < 100 && !msg_complete_)
  {
    char in_char = (char)Serial.read();
    if (next_write_ == 0)
    {
      if (in_char == 'c')
      {
        rx_buffer_[next_write_] = in_char;
        next_write_++;
      }
      else
      {
        Serial.println("BAD HEADER");
      }
    }
    else
    {
      rx_buffer_[next_write_] = in_char;
      next_write_++;
    }

    if (next_write_ == MSG_SIZE)
    {
      msg_complete_ = true;
      next_write_ = 0;
    }
    
    
  }

}
