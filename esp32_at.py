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
AT_CONNECT_AT = 'AT+CWJAP'
AT_GET_VERSION = 'AT+GMR'

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

    def get_version(self):
        self.send_command(AT_GET_VERSION)


    def get_connected_ap(self):
        command = f'{AT_CONNECT_AT}?'
        self.send_command(command)

    def connect_ap(self, ssid, pwd, mac = None):
        # AT+CWJAP=[<"ssid">],[<"pwd">][,<"bssid">][,<pci_en>][,<reconn_interval>][,<listen_interval>][,<scan_mode>][,<jap_timeout>][,<pmf>]
        command = f'{AT_CONNECT_AT}="{ssid}","{pwd}"'
        if mac != None:
            command = command + f",{mac}"
        self.send_command(command)
    
    def list_available_ap(self):
        mask = 0x7FF
        command = f"{AT_LIST_AVAILABLE_AP_CONFIG}=,{str(mask)}"
        self.send_command(command)
        self.send_command(AT_LIST_AVAILABLE_AP)
    
        # <mode>:
        # 0: Null mode. Wi-Fi RF will be disabled.
        # 1: Station mode.
        # 2: SoftAP mode.
        # 3: SoftAP+Station mode.
        # <auto_connect>: Enable or disable automatic connection to an AP when you change the mode of the ESP32 from the SoftAP mode or null mode to the station mode or the SoftAP+Station mode. Default: 1. If you omit the parameter, the default value will be used, i.e. automatically connecting to an AP.
        # 0: The ESP32 will not automatically connect to an AP.
        # 1: The ESP32 will automatically connect to an AP if the configuration to connect to the AP has already been saved in flash before.
    def set_wifi_mode(self, mode, autoConnect = 0):
        # AT+CWMODE=<mode>[,<auto_connect>]
        if mode < 0 or mode > 3:
            print(f"Error: invalid wifi mode ({mode})")
            return
        if autoConnect <0 or autoConnect > 1:
            print(f"Error: invalid autoConnect ({autoConnect})")
            return
        
        command = f'{AT_SET_MODE}={mode},{autoConnect}'
        self.send_command(command)

    def get_adc(channel, atten):
        # AT+DRVADC=<channel>,<atten>
        ...

    def send_http_client_request(self, method, content):
        # AT+HTTPCLIENT=<opt>,<content-type>,<"url">,[<"host">],[<"path">],<transport_type>[,<"data">][,<"http_req_header">][,<"http_req_header">][...]
        if method < 1 or method > 5:
            print(f"Error: invalid methoc ({method})")
            return
    

    def start_receive_thread(self):
        reader_thread = threading.Thread(target=read_serial, args=(self.serial,self.debug))
        reader_thread.daemon = True  # So it exits when the main script ends
        reader_thread.start()       

