#Import needed libraries
import socket
import sys
import RPi.GPIO as GPIO
import time

#Create a socket for receiving
receivesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Create a socket for sending
sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#The port we will communicate on
port = 10000

#Our ip address
ip = "172.16.158.138"

#Next ip address
nextip = "172.16.150.232"

#Set up the server on our ip and a port
receivesocket.bind((ip,port))

#Listen in on that port
receivesocket.listen(5)

#The pi the led is on
ledpin = 18

#Boolean for if the led is on or off
ledon = False

#Some GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledpin, GPIO.OUT)
GPIO.output(ledpin, GPIO.LOW)
#The person to start the connection
if len(sys.argv) >= 2:
    sendsocket.connect(nextip, port)
    sendsocket.send("toggle")
    print "toggled"

#Accept the connection and get a socket (c) and a  address (addr)
c, addr = receivesocket.accept()

#Everyone else can connect
if len(sys.argv) == 1:
    sendsocket.connect((nextip, port))

#Do this indefinitely until the program is stopped
while True:
    
    #Check to see if anything was sent
    text = str(c.recv(1024))

    #If we got any new info
    if text != "":
        print(text)
        #Toggle the led 
        if ledon:
            GPIO.output(ledpin, GPIO.LOW)
        else:
            GPIO.output(ledpin, GPIO.HIGH)
        ledon = not ledon
        
        #Pause for a bit
        time.sleep(1)

        #Send a toggle message again
        sendsocket.send("toggle")
    
    #Reset the text
    text = ""

