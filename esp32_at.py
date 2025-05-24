import time
import serial
import threading


# thread
def read_serial(ser, debug):
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode(errors='ignore').strip()
                if debug:
                    print(f"R:{line}")
        except serial.SerialException as e:
            print(f"[ERROR] Serial disconnected: {e}")
            break


AT_GET_ADC = 'AT+DRVADC'
AT_LIST_AVAILABLE_AP = 'AT+CWLAP' # AT+CWLAP=[<"ssid">][,<"mac">][,<channel>][,<scan_type>][,<scan_time_min>][,<scan_time_max>][,<ext_channel_bitmap>]
AT_LIST_AVAILABLE_AP_CONFIG = 'AT+CWLAPOPT' # AT+CWLAPOPT=<reserved>,<print mask>[,<rssi filter>][,<authmode mask>]
AT_SET_MODE = 'AT+CWMODE' # AT+CWMODE=<mode>[,<auto_connect>]
AT_CONNECT_AT = 'T+CWJAP'

class ESP32_AT:
    def __init__(self, serial, debug = False, delayAfterSend = 0):
        self.serial = serial
        self.debug = debug
        self.delayAfterSend = delayAfterSend
        self.start_receive_thread()

    def send_command(self, cmd):
        full_cmd = cmd + '\r\n'
        self.serial.write(full_cmd.encode())
        if self.debug:
            print(f"\n>>> Sent: {cmd}")
        time.sleep(self.delayAfterSend)  # Wait a bit for response

    def connect_ap(self, ssid, pwd):
        # AT+CWJAP=[<"ssid">],[<"pwd">][,<"bssid">][,<pci_en>][,<reconn_interval>][,<listen_interval>][,<scan_mode>][,<jap_timeout>][,<pmf>]
        command = f'{AT_CONNECT_AT}={ssid},{pwd}'
        self.send_command(command)
    
    def list_available_ap(self):
        mask = 0x7FF
        command = f"{AT_LIST_AVAILABLE_AP_CONFIG}=,{str(mask)}"
        self.send_command(command)
        
    def set_wifi_mode(self, mode):
        command = f'{AT_SET_MODE}={mode}'
        self.send_command(command)

    def get_adc(    channel, atten):
        # AT+DRVADC=<channel>,<atten>
        ...

    def start_receive_thread(self):
        reader_thread = threading.Thread(target=read_serial, args=(self.serial,self.debug))
        reader_thread.daemon = True  # So it exits when the main script ends
        reader_thread.start()       


# Configure your serial port here
PORT = 'COM11'        # Replace with your ESP32's COM port
BAUD = 115200         # Default AT command baud rate
TIMEOUT = 0.1         # Read timeout in seconds

def test():
    delay = 0.1
    with serial.Serial(PORT, BAUD, timeout=TIMEOUT) as ser:
        esp = ESP32_AT(serial = ser, debug = True, delayAfterSend = 0.05)
        esp.set_wifi_mode(1)
        time.sleep(delay)
        esp.list_available_ap()
        time.sleep(10)
        esp.list_available_ap()
        time.sleep(delay)
        esp.list_available_ap()
        time.sleep(delay)
        esp.connect_ap("Giovani", "qwertyuiop")
        time.sleep(delay)
        esp.connect_ap("Giovani", "qwertyuiop")
        time.sleep(delay)
        esp.connect_ap("Giovani", "qwertyuiop")
        time.sleep(delay)
        esp.connect_ap("Giovani", "qwertyuiop")
        time.sleep(delay)
        esp.connect_ap("Giovani", "qwertyuiop")
        time.sleep(delay)

test()