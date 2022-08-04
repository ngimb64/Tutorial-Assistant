# Tutorial Assistant
![alt text](https://github.com/ngimb64/Tutorial-Assistant/blob/master/TutorialAssistant.gif?raw=true)
![alt text](https://github.com/ngimb64/Tutorial-Assistant/blob/master/TutorialAssistant.png?raw=true)

&#9745;&#65039; Bandit verified<br>
&#9745;&#65039; Synk verified<br>
&#9745;&#65039; Pylint verified 9.07/10

## Prereqs
This script runs on Windows and Linux, written in Python 3.8

## Purpose
This project adopts the features of the Screenshot-Assistant project in my repository.<br>
The big difference is that this program also logs keys in sentence structures and logs to a file.<br>
Then that file is reformatted and saved in a new file with a clean, easily readable format.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example: `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows in the Scripts directory, for execute the `./activate` script to activate the virtual environment.
- For Linux in the bin directory, run the command `source activate` to activate the virtual environment.

## How to use
- Open up shell such as command prompt or terminal
- Enter directory containing program and execute in shell
- Open the graphical file manager and go to path specified in program
- Click on the open CMD and hit enter
- Check out the file manager to visualize the screenshots and logging data
- Any keys pressed will be buffered into a variable and will be entered as a sentence when enter is pressed
- Hit escape to pause program and cleanly format key logs to be written to a new file
- If you want to start again hit enter again
- OR if you would like to exit hit Ctrl + C
 
## Function Layout
-- tutorial_assistant.py --

> on_press &nbsp;-&nbsp; For key listener, write sentence to file if enter is pressed, kill screenshot capturing
> process if escape is pressed, otherwise append the entered key to the key capture list to form sentence.<br>
> screenshots &nbsp;-&nbsp; Loop that actively takes screenshots.<br>
> regex_formatting &nbsp;-&nbsp; Parses the logged pynput keys into human-readable format.<br>
> main &nbsp;-&nbsp; Facilitates key listener thread and screenshot capture.

## Exit Codes
-- tutorial_assistant.py --

> 0 - Successful operation<br>
> 1 - Unexpected exception occurred<br>
> 2 - Error occurred during file operation saving output keys to file<br>
> 3 - Error occurred during file operation reformatting output keys to human format
