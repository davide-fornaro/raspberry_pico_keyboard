import board
import digitalio
import storage
import usb_cdc

# Configurazione del pin di Escape (Selezionato GP0)
# Il pull-up interno mantiene il livello logico alto (True/1) di default.
escape_pin = digitalio.DigitalInOut(board.GP0)
escape_pin.direction = digitalio.Direction.INPUT
escape_pin.pull = digitalio.Pull.UP

# Valutazione dello stato al momento del boot
if escape_pin.value:
    pass
    # Condizione normale (Pin flottante): Modalità stealth armata.
    # Il sistema host non riceverà i descrittori per il Mass Storage e la Seriale.
    # storage.disable_usb_drive()
    # usb_cdc.disable()
    print("Modalità stealth: Mass Storage e Seriale disabilitati.")
else:
    # Condizione di manutenzione (Pin a GND): Modalità sviluppo.
    # L'enumerazione procederà normalmente esponendo CIRCUITPY e la porta COM.
    print("Modalità sviluppo: Mass Storage e Seriale abilitati.")
    pass
