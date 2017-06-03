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
    started = False
    
    def __init__(self):
        pifacedigitalio.init()
        self.start_listener()
        self.get_args()
        self.set_flash_speed_properties()
        self.started = True

    def get_args(self):
        self.args = StartLedArgumentParser().args_dict
        if not self.args or None == self.args['led']:
            self.get_args_from_input()
        elif self.args:
            self.catch_stop_all()    
        if self.args['toggle'] == 0:
            self.args['speed'] = 0

    def get_args_from_input(self):
        self.args['led'] = int(input("LED number: "))
        self.args['toggle'] = int(input("Toggle on (1) or off (0): "))
        if self.args['toggle'] == 1:
            self.args['speed'] = int(input("Set flash speed (1-10): "))
            if self.args['speed'] == None:
                self.args['speed'] = 0
            self.args['stop'] = False
        else:
            self.args['speed'] = 0
            self.args['stop'] = True
    
    def start_listener(self):
        self.piface_listener = pifacedigitalio.InputEventListener(chip = self.pfio)
        self.piface_listener.register(0, pifacedigitalio.IODIR_BOTH, self.listener_callback())
        self.piface_listener.activate()

    def listener_callback(self):
        pass

    def catch_stop_all(self):
        print(self.args['stopall'])
        print(self.args['stop'])
        if self.args['stopall'] == True:
            print('shutting off all leds')
            self.shut_off_all_leds()
            sys.exit()
        elif self.args['stop'] == True:
            self.close()
            sys.exit()

    def startled(self):
        self.flash_led()
        self.close()

    def flash_led(self):
        while self.started == True:
            self.toggle_led()
            if self.args['stop']:
                self.started = False
                return
            sleep(self.sleep_time)

    def toggle_led(self):
        #this is the non-oop way
        #pifacedigitalio.digital_write(pin, i)
        #output_pins and leds seem to be the same array, leds has methods
        #self.pfio.output_pins[pin].value = i
        if self.args['toggle'] == 0:
            self.pfio.leds[self.args['led']].turn_off()
            self.args['toggle'] = 1
        else:
            self.pfio.leds[self.args['led']].turn_on()
            self.pfio.leds[self.args['led']].set_high()
            self.args['toggle'] = 0

    def set_flash_speed_properties(self):
        self.set_flash_speed_limit()
        self.set_flash_high_speed()
        self.set_flash_low_speed()
        self.transform_flash_speed()
        self.set_sleep_time()

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

    #stub for future, this is not oop
    def read_input(self):
        #pifacedigitalio.digital_read(0)
        print(se1f.pfio.output_pins[self.led].value)

    def toggle_pin_pullups(self, pin_number, pin_state):
        digital_write_pullup(pin_number, pin_state)

    def reset(self):
        self.started = False

    def close(self):
        self.pfio.deinit_board()
        sys.exit()

    def shut_off_all_leds(self):
        print('shutting off all leds')
        self.pfio.output_port.all_off()
        self.close()


def main():
    startled = StartLed()
    try:
        startled.startled()
    except pifacedigitalio.core.NoPiFaceDigitalError as e:
        excinfo = sys.exc_info()
        print (e, excinfo.tb_lineno)
        sys.exit(1)
    except KeyboardInterrupt:
        startled.reset()
    except ImportError as e:
        print (e)
        sys.exit(1)
    

if __name__ == '__main__':
    main()

sys.exit()


    

