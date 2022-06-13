import os
from oled_091 import SSD1306
from subprocess import check_output
from time import sleep
from datetime import datetime
from os import path
import serial
import RPi.GPIO as GPIO
import csv
import open_door
import close_door
import threading
import schedule
import time

from datetime import datetime
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = path.join(DIR_PATH, "Fonts/GothamLight.ttf")

logs = "logs.csv"
chicken_list = "chicken_list.csv"
time_open = "11:09"
time_close = "11:10"
is_door_closed = False
class Chicken:
    def __init__(self, id, status, timestamp):
        self.id = id
        self.status = status
        self.timestamp = timestamp



class read_rfid:
    def read_rfid (self):
        ser = serial.Serial ("/dev/ttyS0")                             #Open named port 
        ser.baudrate = 9600                                            #Set baud rate to 9600
        data = ser.read(12)                                            #Read 12 characters from serial port to data
        # buzzer enable
        #if(data != " "):
        #    GPIO.output(17,GPIO.HIGH)
        #    sleep(.2)
        #    GPIO.output(17,GPIO.LOW)
        ser.close ()                                                   #Close port
        data=data.decode("utf-8")
        return data
        

def check_entry(id):
    # verify if chicken is in the database and what was its last status
    # if none => we create it
    f_logs = open(logs, "r+")

    chicken_detected = Chicken(id, 1, datetime.now())

    if is_chicken_in(id):
        leave(chicken_detected)
    else :
        enter(chicken_detected)

    f_logs.close()

## check if a chicken is in
def is_chicken_in(id):
    #read logs to check last chicken state
    f_logs = open(logs, "r+")
    #read csv
    csv_lines = f_logs.readlines() 

    row_count = sum(1 for row in csv_lines) - 1

    for i in range(row_count, -1, -1):
        #print(i)
        row_csv = csv_lines[i].split(",")
        
        #if ieme row id is equal to input, return status
        print(row_csv[0] + " " + id)
        if id == row_csv[0]:
            
            if (row_csv[1] == "1"):
                f_logs.close()
                return True
            else:
                f_logs.close()
                return False
    
    add_to_list(id)
    f_logs.close()
    return False

## Update chicken's status (entering)
def enter(chicken):
    f_logs = open(logs, "a+")
    chicken.status = 1
    chickenwriter = csv.writer(f_logs, delimiter=',')
    chickenwriter.writerow([chicken.id, chicken.status, chicken.timestamp])
    #change chicken status in file
    f_logs.close()

## Update chicken's status (leaving)
def leave(chicken):
    chicken.status = 0
    f_logs = open(logs, "a+")
    chickenwriter = csv.writer(f_logs, delimiter=',')
    chickenwriter.writerow([chicken.id, chicken.status, chicken.timestamp])
    # change chicken status in file
    f_logs.close()

## Add chicken to the list 
def add_to_list(id):
    f_chicken_list = open(chicken_list, "a+")
    chickenwriter = csv.writer(f_chicken_list)
    chickenwriter.writerow([id])
    f_chicken_list.close()
    return

## Check all chicken's status in register and return false if at least one is still out
def check_chicken_before_closing():
    ## TODO fix
    print("is there enough chicken bro?")
    #read all ids of chickens
    f_chicken_list = open(chicken_list, "r")
    chicken_lines = f_chicken_list.readlines() 
    #read logs to check last chickens' state) 

    for row_chicken in chicken_lines:
        if (is_chicken_in(row_chicken) != True):
            return False
    return True

## Display error and wait 2 minutes before trying to close the door again
def error_not_enough_chicken_in():
    print("Error : not enough chicken in")
    time.sleep(10)
    if (is_door_closed != True):
        close_door_call()
    return

## Call the opening door motor's script
def open_door_call():
    # open the door
    print("Open door")
    is_door_closed = False
    open_door.open_door()
    return

## Call the closing door motor's script but only if all chicken are insides.
def close_door_call():
    # close the door
    if check_chicken_before_closing():
        close_door.close_door()
        print("Close door")
        is_door_closed = True
    else :
        error_not_enough_chicken_in()
    return

## Thread of door management
def door_thread():

    while True :
        schedule.run_pending()
        time.sleep(2)


if __name__ == "__main__":

    f_logs = open(logs, "a+")
    f_logs.close()
    f_chicken_list = open(chicken_list, "a+")
    f_chicken_list.close()
    SB = read_rfid()
    # scheduling the time to open the door
    schedule.every().day.at(time_open).do(open_door_call)
    # scheduling the time to close the door
    schedule.every().day.at(time_close).do(close_door_call)
    x = threading.Thread(target=door_thread)
    x.start()
    while True:

        if is_door_closed != True :
            id=SB.read_rfid()
            check_entry(id)