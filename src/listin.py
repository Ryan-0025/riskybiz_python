import serial
import time
import os

PORT = "/dev/ttyUSB0"  # Change as needed
BAUD = 115200

def main():
    try:
        with serial.Serial(PORT, BAUD, timeout=0.1) as ser:
            print(f"Connected to {PORT} at {BAUD} baud.")

            print("Ready. Listening for button presses...\n")

            while True:
                #if ser.in_waiting > 0:
                if ser.in_waiting != '':
                    #print(ser.in_waiting)
                    line = ser.readline(1)
                    decoded = line.decode()

                    if len(decoded):
                        os.system("amixer sset Master toggle")
                
                    ser.reset_output_buffer()

    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()
