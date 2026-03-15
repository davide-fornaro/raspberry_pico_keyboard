import board
import digitalio
import storage
import usb_cdc

escape_pin = digitalio.DigitalInOut(board.GP0)
escape_pin.direction = digitalio.Direction.INPUT
escape_pin.pull = digitalio.Pull.UP

if escape_pin.value:
    # storage.disable_usb_drive()
    # usb_cdc.disable()
    pass
else:
    pass
