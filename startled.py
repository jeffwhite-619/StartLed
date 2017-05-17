#! /usr/bin/python3

import sys
from time import sleep
import pifacedigitalio
from startledargumentparser import StartLedArgumentParser

class StartLed:
    pfio = pifacedigitalio.PiFaceDigital()
    piface_listener = None
    flash_speed_limit = None
    high_speed = None
    low_speed = None
    args = dict()
    
    def __init__(self):
        pifacedigitalio.init()
        self.start_listener()
        self.get_args()
        self.startled()

    def get_args(self):
        self.args = StartLedArgumentParser().args_dict
        print(self.args)        
        if not self.args or None == self.args['led']:
            self.get_args_from_input()
    
    def start_listener(self):
        self.piface_listener = pifacedigitalio.InputEventListener(chip = self.pfio)
        self.piface_listener.register(0, pifacedigitalio.IODIR_BOTH, self.listener_callback())
        self.piface_listener.activate()

    def listener_callback(self):
        pass

    def startled(self):
        self.set_flash_properties()
        self.flash_led()
        self.close()

    def get_args_from_input(self):
        print(self.args)
        self.args['led'] = int(input("LED number: "))
        self.args['toggle'] = int(input("Toggle on (1) or off (0): "))
        if self.args['toggle'] == 1:
            self.args['speed'] = int(input("Set flash speed (1-10): "))
            self.args['stop'] = False
        else:
            self.args['speed'] = 0
            self.args['stop'] = True

    def toggle_led(self):
        #this is the non-oop way
        #pifacedigitalio.digital_write(pin, i)
        #output_pins and leds seem to be the same array, leds has methods
        #self.pfio.output_pins[pin].value = i
        if self.args['toggle'] == 0:
            self.pfio.leds[self.args['led']].turn_off()
        else:
            self.pfio.leds[self.args['led']].turn_on()
            self.pfio.leds[self.args['led']].set_high()

    def set_flash_properties(self):
        self.set_flash_speed_properties()
        self.set_sleep_time()

    def set_flash_speed_properties(self):
        self.set_flash_speed_limit()
        self.set_flash_high_speed()
        self.set_flash_low_speed()
        self.transform_flash_speed()

    def set_flash_high_speed(self):
        self.high_speed = self.flash_speed_limit - 1

    def set_flash_low_speed(self):
        self.low_speed = 1

    def set_flash_speed_limit(self):
        self.flash_speed_limit = 11

    def transform_flash_speed(self):
        if self.args['speed'] > self.high_speed:
            self.args['speed'] = self.high_speed
        elif self.args['speed'] < self.low_speed:
            self.args['speed'] = self.low_speed

    def set_sleep_time(self):
        self.sleep_time = self.flash_speed_limit - self.args['speed']

    def flash_led(self):
        self.toggle_led()
        if self.args['stop']:
            return
        sleep(self.sleep_time)
        self.flip_toggle()
        self.flash_led()

    def flip_toggle(self):
        if self.args['toggle'] == 1:
            self.args['toggle'] = 0
        else:
            self.args['toggle'] = 1
    
    def read_input(self):
        #pifacedigitalio.digital_read(0)
        print(se1f.pfio.output_pins[self.led].value)

    def toggle_pin_pullups(self, pin_number, pin_state):
        digital_write_pullup(pin_number, pin_state)

    def close(self):
        self.pfio.deinit_board()

    def shut_off_all_leds(self):
        self.pfio.output_port.all_off()


def main():
    try:
        startled = StartLed()
    except pifacedigitalio.core.NoPiFaceDigitalError as e:
        excinfo = sys.exc_info()
        print (e, excinfo.tb_lineno)
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        #startled = StartLed()
        print("Name: ", __name__)

    except ImportError as e:
        print (e)
        sys.exit(1)
    

if __name__ == '__main__':
    main()




    

