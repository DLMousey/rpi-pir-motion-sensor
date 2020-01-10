import RPi.GPIO as GPIO
import time
import sys, getopt

def get_time(): 
    return time.strftime("%H:%M:%S", time.gmtime())

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pinpir = 11
buzzer = 15
led_blue = 18
led_red = 12

if "--no-buzzer" in sys.argv:
    print("[" + get_time() + "] Buzzer is disabled (silent mode)")
    allow_buzzer = False
else:
    print("[" + get_time() + "] Buzzer is enabled (default mode)")
    allow_buzzer = True

GPIO.setup(pinpir, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(led_blue, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)

GPIO.output(buzzer, GPIO.LOW)
GPIO.output(led_blue, GPIO.HIGH)
GPIO.output(led_red, GPIO.HIGH)

currentstate = 0
previousstate = 0

print("[" + get_time() + "] PIR Module Test (CTRL+C to exit)")

try:
    print("[" + get_time() + "] Waiting for PIR to settle...")
    while GPIO.input(pinpir) == 1:
        currentstate = 0

    GPIO.output(led_blue, GPIO.LOW)
    GPIO.output(led_red, GPIO.HIGH)

    print("[" + get_time() + "] PIR settled, system ready")

    while True:
        currentstate = GPIO.input(pinpir)
        
        if currentstate == 1 and previousstate == 0:
            previousstate = 1

            print("[" + get_time() + "] Motion Detected!")

            GPIO.output(led_red, GPIO.HIGH)
            GPIO.output(led_blue, GPIO.LOW)
          
            if allow_buzzer:
                # Sound the buzzer twice
                GPIO.output(buzzer, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(buzzer, GPIO.LOW)
                time.sleep(0.1)
                GPIO.output(buzzer, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(buzzer, GPIO.LOW)

        elif currentstate == 0 and previousstate == 1:
            print("[" + get_time() + "] Motion has stopped, resetting")
            GPIO.output(buzzer, GPIO.LOW) # Reset the buzzer to low just in case
            GPIO.output(led_red, GPIO.LOW)
            GPIO.output(led_blue, GPIO.HIGH)
            previousstate = 0

        time.sleep(0.01)
except KeyboardInterrupt:
    print("    Quit")
    GPIO.cleanup()
