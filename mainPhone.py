from time import sleep
import RPi.GPIO as gpio
from story import StoryObj
from keypad import keypad
from pygame import mixer
from signal import pause
from random import choice

#************ SETUP STORY SOUND OBJECTS *************
story_path = "audio_final/stories/"
sfx_path = "audio_final/sfx/"
info = StoryObj("411",sfx_path + "read_card_or_instructor.wav")
emergency = StoryObj("911", sfx_path + "disconnected.wav")
michael = StoryObj("5554679", story_path + "michael.wav")
denise = StoryObj("5553325", story_path + "denise.wav")
callie = StoryObj("5554981", story_path + "callie.wav")
dara = StoryObj("5556472", story_path + "dara.wav")
devon = StoryObj("5558032", story_path + "devon.wav")

directory_list = [emergency, michael, info, callie, devon, dara, denise]

mixer.init()
main_channel = mixer.Channel(0)

dial_tone = mixer.Sound(sfx_path + "dialtone.wav")
button_1 = mixer.Sound(sfx_path + "button_1.wav")
button_2 = mixer.Sound(sfx_path + "button_2.wav")
button_3 = mixer.Sound(sfx_path + "button_3.wav")
wrong_number = mixer.Sound(sfx_path + "read_card_or_instructor.wav")

#************ SETUP HOOK & KEYPAD*********************
HOOK_PIN = 4
gpio.setmode(gpio.BCM)
gpio.setup(HOOK_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)
phone_on_hook = True

row_pins = [23, 22, 27,17]
col_pins = [24,25,5]
kp = keypad(row_pins, col_pins)

dialed_number = ""

def main():
    while True:
        if phone_off_hook():
            input_state()
        else:
            standby_state()

def input_state():
    number_to_lookup = ""
    if mixer.get_busy() == False:
        play_sfx(dial_tone)
    number_to_lookup = get_input_number()
    if number_to_lookup:
        print("number to lookup:  {}".format(number_to_lookup))
        audio_to_play = verify_number(number_to_lookup)
        if audio_to_play is not -1:
            try:
                play_state(audio_to_play)
            except:
                print("Cant play audio")
        else:
            play_sfx(wrong_number)
        clear_dialed()
        
def get_input_number():
    global dialed_number
    finished_number = ""
    if dialed_number == "911":
        print("911 dialed")
        finished_number = "911"
    elif dialed_number == "411":
        print("info number dialed")
        finished_number = "411"
    elif len(dialed_number) < 7:
        current_val = kp.getKey()
        if current_val or current_val == 0:
            curr_number = str(kp.getKey())
            dialed_number = dialed_number + curr_number
            print(curr_number + " added, total number is " + dialed_number)
            button_tone = choice([button_1, button_2, button_3])
            play_sfx(button_tone)
            # prevents multiple triggers when held
            while kp.getKey() == current_val: 
                sleep(0.25)
    elif len(dialed_number) == 7:
        finished_number = dialed_number
    if finished_number:
        print("number finished!")
        dialed_number = ""
        return finished_number
               
def play_sfx(sfx):
    sfx.play()
        
def verify_number(number_to_lookup):
    print("verifying number: {}".format(number_to_lookup))
    for num, item in enumerate(directory_list):
        print("comparing {} to {}".format(number_to_lookup, item.get_number()))
        if number_to_lookup == directory_list[num].get_number():
            current_path = directory_list[num].get_path()
            print("found file: {}".format(current_path))
            return current_path
    return -1

def play_state(audio_path):
    mixer.stop()
    print("playing file: {}".format(audio_path))
    current_sound = mixer.Sound(audio_path)
    current_sound.play()
    
def standby_state():
    clear_dialed()
    mixer.stop()
    print("phone hung up!")
    
def clear_dialed():
    global dialed_number
    if dialed_number:
        print("dialed number cleared")
        dialed_number = ""

def phone_off_hook():
    return gpio.input(HOOK_PIN)
    
number_dialed = False

if __name__ == "__main__":
    try:
        main()
    finally:
        gpio.cleanup()