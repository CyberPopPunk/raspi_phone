from time import sleep
import RPi.GPIO as gpio
from story import StoryObj
from keypad import keypad
from pygame import mixer
from signal import pause

#************ SETUP STORY SOUND OBJECTS *************
info = StoryObj("411","audio/info.wav")
emergency = StoryObj("911", "audio/911.wav")
michael = StoryObj("5836215", "audio/videotape.wav")


directory_list = [emergency, michael, info]

#************ SETUP HOOK & KEYPAD*********************
HOOK_PIN = 4
gpio.setmode(gpio.BCM)
gpio.setup(HOOK_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)
phone_on_hook = True

row_pins = [23, 24, 25,5]
col_pins = [22,27,17]
pad_pins = row_pins + col_pins
kp = keypad(row_pins, col_pins)
#pad_pins = [,]
#keypad_map = {
#    "17":
#    }
dialed_number = ""

def input_number():
    global dialed_number
    finished_number = ""
    #print("awaiting input")
    if len(dialed_number) < 7:
        if dialed_number:
            print(dialed_number)
        if dialed_number == "911":
            print("911 dialed")
            finished_number = "911"
        elif dialed_number == "411":
            print("info number dialed")
            finished_number = "411"
        elif len(dialed_number) < 7:
            if kp.getKey():
                curr_number = str(kp.getKey())
                dialed_number = dialed_number + curr_number
                print(curr_number + " added, total number is " + dialed_number)
                sleep(0.3)
        elif len(dialed_number) == 7:
            finished_number = dialed_number
    if finished_number:
        print("number finished!")    
        dialed_number = ""
        return finished_number
        
#
#for pin in pad_pins:
#    gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_UP)
#    gpio.add_event_detect(pin, gpio.FALLING, callback = input_number, bouncetime=200)


mixer.init()
main_channel = mixer.Channel(0)

dial_tone = mixer.Sound("dialtone.wav")
first_run = True

# // setup the buttons

def main():
    while True:
        #print("phone is picked up? " + str(gpio.input(HOOK_PIN)))
        if gpio.input(HOOK_PIN):
            input_state()
        else:
            standby_state()

def input_state():
    
#    print("input state")
    #print("main_channel is {}".format(mixer.get_busy()))
    if mixer.get_busy() == False:
        print("playing dial tone")
        dial_tone.play()
    number_to_lookup = input_number()
    if number_to_lookup:
        print("number to lookup:  {}".format(number_to_lookup))
        audio_to_play = verify_number(number_to_lookup)
        if audio_to_play:
            play_state(audio_to_play)
            
    
def verify_number(number_to_lookup):
    #TODO is number belong with any of the objects
    print("verifying number: {}".format(number_to_lookup))
    for num, item in enumerate(directory_list):
        print("comparing {} to {}".format(number_to_lookup, item.get_number()))
        if number_to_lookup == directory_list[num].get_number():
            current_path = directory_list[num].get_path()
            print("found file: {}".format(current_path))
            return current_path
            

def play_state(audio_path):
    mixer.stop()
    print("playing file: {}".format(audio_path))
    current_sound = mixer.Sound(audio_path)
    current_sound.play()
    
def standby_state():
    mixer.stop()
    print("phone hung up!")

number_dialed = False

if __name__ == "__main__":
    try:
        main()
    finally:
        gpio.cleanup()