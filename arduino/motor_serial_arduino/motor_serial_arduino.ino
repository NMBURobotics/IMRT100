#include "DualVNH5019MotorShield.h"
#include "NewPing.h"



#define V_MAX 500
#define V_STEP 25

#define CMD_RATE 40
#define FEEDBACK_RATE 10

#define MSG_SIZE 10

#define POLY 0x8408

#define CMD_MSG_TIMEOUT_DURATION 500


#define SONIC_NUM 4
#define MAX_DISTANCE 255

NewPing sonics_[SONIC_NUM] = {NewPing( 3,  3, MAX_DISTANCE),
                              NewPing(11, 11, MAX_DISTANCE),
                              NewPing(A2, A2, MAX_DISTANCE),
                              NewPing(A3, A3, MAX_DISTANCE)                          
                             };

DualVNH5019MotorShield md;


unsigned long next_cmd_time_;
unsigned long next_feedback_time_;
unsigned long prev_cmd_msg_time_;
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
  md.init();
  next_cmd_time_ = millis();
  next_feedback_time_ = millis();
  prev_cmd_msg_time_ = millis() + CMD_MSG_TIMEOUT_DURATION;
}

void loop()
{

  // Get current time
  unsigned long current_time = millis();

  // Check if we have received a complete message through serial
  // if we have, we set target speed as specified in msg
  if (msg_complete_)
  {
    // Calculate checksum and compare to the checksum included in message
    unsigned short crc_msg = ( (rx_buffer_[MSG_SIZE-3] & 0xff) << 8 ) | ( (rx_buffer_[MSG_SIZE-2] & 0xff) );
    unsigned short crc_calc = crc16(rx_buffer_, MSG_SIZE - 3);

    // If the checkums match, we accept the command
    if (crc_msg == crc_calc)
    {
      target_v1_ = ( (rx_buffer_[1] & 0xff) << 8 ) | ( (rx_buffer_[2] & 0xff) );
      target_v2_ = ( (rx_buffer_[3] & 0xff) << 8 ) | ( (rx_buffer_[4] & 0xff) );
      prev_cmd_msg_time_ = current_time;
    }
    else
    {
      Serial.println("BAD CRC!");
    }
    msg_complete_ = false;
  }


  // If we stop receiving serial messages we want the target speed to be zero
  if (current_time > prev_cmd_msg_time_ + CMD_MSG_TIMEOUT_DURATION)
  {
    target_v1_ = 0;
    target_v2_ = 0;
  }


  // We want to update commands at a set frequency
  if (current_time > next_cmd_time_)
  {
    m1_cmd_ = calculateCommand(m1_cmd_, target_v1_);
    m2_cmd_ = calculateCommand(m2_cmd_, target_v2_);
    next_cmd_time_ += 1000 / CMD_RATE;
  }


  // Send commands to motor controller
  md.setM1Speed(m1_cmd_);
  md.setM2Speed(m2_cmd_);
  stopIfFault();


  // Get and transmit feedback
  if (current_time > next_feedback_time_)
  {
    int sonic_1 = sonics_[0].ping_cm();
    int sonic_2 = sonics_[1].ping_cm();
    int sonic_3 = sonics_[2].ping_cm();
    int sonic_4 = sonics_[3].ping_cm();
    
    if (sonic_1 == 0)
      sonic_1 = MAX_DISTANCE;
    if (sonic_2 == 0)
      sonic_2 = MAX_DISTANCE;
    if (sonic_3 == 0)
      sonic_3 = MAX_DISTANCE;
    if (sonic_4 == 0)
      sonic_4 = MAX_DISTANCE;
    
    char tx_msg[MSG_SIZE];
    tx_msg[0] = 'f';
    tx_msg[1] = (sonic_1) & 0xff;
    tx_msg[2] = (sonic_2) & 0xff;
    tx_msg[3] = (sonic_3) & 0xff;
    tx_msg[4] = (sonic_4) & 0xff;
    tx_msg[MSG_SIZE - 1] = '\n';

    short crc = crc16(tx_msg, MSG_SIZE - 3);
    
    tx_msg[MSG_SIZE - 3] = (crc >> 8) & 0xff;
    tx_msg[MSG_SIZE - 2] = (crc) & 0xff;

    Serial.write(tx_msg, MSG_SIZE);
    
    next_feedback_time_ += 1000 / FEEDBACK_RATE;
  }
  
    


 
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
