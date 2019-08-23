import RPi.GPIO as GPIO
import time

BUZZ_PIN = 23
DUTY = 10

c =  [ 32,  65, 131, 262, 523]
d =  [ 36,  73, 147, 294, 587]
e =  [ 41,  82, 165, 330, 659]
f =  [ 43,  87, 175, 349, 698]
g =  [ 49,  98, 196, 392, 784]
a =  [ 55, 110, 220, 440, 880]
b =  [ 61, 123, 246, 492, 984]

WHOLE = 0.8
HALF  = WHOLE / 2
QUART = WHOLE / 4

song_pitches   = [  c[3],    d[3],    e[3],    f[3],    g[3],    g[3],    a[3],    a[3],    a[3],    a[3],    g[3],    f[3],    f[3],    f[3],    f[3],    e[3],    e[3],    d[3],    d[3],    d[3],    d[3],    c[3] ]
song_durations = [ QUART,   QUART,   QUART,   QUART,    HALF,    HALF,   QUART,   QUART,   QUART,   QUART,   WHOLE,   QUART,   QUART,   QUART,   QUART,    HALF,    HALF,   QUART,   QUART,   QUART,   QUART,   WHOLE ]
song_words     = [ 'Lis',    'a', ' gikk',  ' til',   ' sko',  'len.',' Tripp',' tripp',' tripp',  ' det',  ' sa.',    ' I',  ' den',   ' ny',     'e',  ' kjo',   'len',' tripp',    'et',  ' hun',   ' så',' glad.' ]
song = []

# Put pitch, durations and words in same list
for i in range(len(song_pitches)):
    song.append([song_pitches[i], song_durations[i], song_words[i]])


# BCM pin naming
GPIO.setmode(GPIO.BCM)

# Turn off GPIO warnings
GPIO.setwarnings(False)

# Set buzzer pin to output
GPIO.setup(BUZZ_PIN, GPIO.OUT)

p = GPIO.PWM(BUZZ_PIN, 250) # channel=12 frequency=50Hz
p.start(0)

try:
    # Loop until user terminates program

    for note in song:
        print(note[2], end="")
        p.ChangeDutyCycle(DUTY)
        p.ChangeFrequency(note[0])
        time.sleep(note[1]/2)
        p.ChangeDutyCycle(0)
        time.sleep(note[1]/2)
    # Print a 'newline'
    print('\n')

        
except KeyboardInterrupt:
    print("Terminated by user")

finally:
    # Cleanup
    GPIO.cleanup()
    print("Goodbye")
    p.stop()
