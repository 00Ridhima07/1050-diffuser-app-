import serial  #Library for serial communication
import time  #Library for time

#Class to handle communication with an Arduino over a serial connection
class ArduinoController:
    def __init__(self, port, baudrate=9600):

        #Initialize the ArduinoController with a specified serial port and baud rate.
        self.port = port
        self.baudrate = baudrate
        self.connection = None  #Serial connection object

    def connect(self):
        """
        Establish a connection to the Arduino via the specified serial port.
        
        :return True if the connection is successful, False otherwise.
        """
        try:
            #Attempt to open a serial connection
            self.connection = serial.Serial(self.port, self.baudrate)
            time.sleep(2)  #Allow time for the Arduino to reset and initialize
            print("Connection established")
            return True
        except serial.SerialException:
            #Handle the exception if the connection fails
            print("Failed to connect to Arduino")
            return False

    def send_dimness(self, value):
    
        #Send a brightness (dimness) value to the Arduino.
        if self.connection:
            command = f"DIM:{value}\n"  #Format the dimness command
            self.connection.write(command.encode())  #Send the command over the serial connection
        else:
            #Warn if there is no active connection
            print("No connection to Arduino")

    def send_color(self, r, g, b): #we can remove this if we dont get rgb LEDs
        """
        Send an RGB color value to the Arduino.
        
        :param r: Red component (0-255).
        :param g: Green component (0-255).
        :param b: Blue component (0-255).
        """
        if self.connection:
            command = f"RGB:{r},{g},{b}\n"  #Format the RGB command
            self.connection.write(command.encode())  #Send the command over the serial connection
        else:
            # Warn if there is no active connection
            print("No connection to Arduino")

    def disconnect(self):
        """
        Close the serial connection to the Arduino.
        """
        if self.connection:
            self.connection.close()  #Close the serial connection
            print("Connection closed")
