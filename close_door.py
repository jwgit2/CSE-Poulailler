import RPi.GPIO as GPIO
import time


def close_door():
    GPIO.setmode(GPIO.BCM)
    OUT1 = 22
    OUT2 = 23
    OUT3 = 24
    OUT4 = 27
    delay = 0.005
    SECONDS_WORKING = 2

    GPIO.setup(OUT1, GPIO.OUT)
    GPIO.setup(OUT2, GPIO.OUT)
    GPIO.setup(OUT3, GPIO.OUT)
    GPIO.setup(OUT4, GPIO.OUT)

    try:
        for x in range(50 * SECONDS_WORKING):
            GPIO.output(OUT1, GPIO.HIGH)
            GPIO.output(OUT2, GPIO.HIGH)
            GPIO.output(OUT3, GPIO.LOW)
            GPIO.output(OUT4, GPIO.LOW)
            time.sleep(delay)
            GPIO.output(OUT1, GPIO.LOW)
            GPIO.output(OUT2, GPIO.HIGH)
            GPIO.output(OUT3, GPIO.HIGH)
            GPIO.output(OUT4, GPIO.LOW)
            time.sleep(delay)
            GPIO.output(OUT1, GPIO.LOW)
            GPIO.output(OUT2, GPIO.LOW)
            GPIO.output(OUT3, GPIO.HIGH)
            GPIO.output(OUT4, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(OUT1, GPIO.HIGH)
            GPIO.output(OUT2, GPIO.LOW)
            GPIO.output(OUT3, GPIO.LOW)
            GPIO.output(OUT4, GPIO.HIGH)
            time.sleep(delay)
    except: 
        GPIO.output(OUT4, GPIO.LOW)
        GPIO.output(OUT3, GPIO.LOW)
        GPIO.output(OUT2, GPIO.LOW)
        GPIO.output(OUT1, GPIO.LOW)
        GPIO.cleanup() # cleanup all GPIO 

    finally:
        GPIO.output(OUT4, GPIO.LOW)
        GPIO.output(OUT3, GPIO.LOW)
        GPIO.output(OUT2, GPIO.LOW)
        GPIO.output(OUT1, GPIO.LOW)
        #GPIO.cleanup() # cleanup all GPIO 

if __name__ == "__main__":
    close_door()