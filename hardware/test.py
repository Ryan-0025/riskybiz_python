import serial

PORT = "/dev/ttyUSB1"   # Change this to your actual port
BAUD = 9600

def main():
    try:
        with serial.Serial(PORT, BAUD, timeout=0.1) as ser:
            print(f"Listening on {PORT} at {BAUD} baud...\n")
            while True:
                if ser.in_waiting:
                    data = ser.readline().decode(errors="replace")
                    print(data, end="")  # Avoid double newlines
                #ser.reset_input_buffer()
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()