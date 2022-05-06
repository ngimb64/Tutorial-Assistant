# Tutorial Assistant
![alt text](https://github.com/ngimb64/Tutorial-Assistant/blob/master/TutorialAssistant.png?raw=true)

## Prereqs
> This script runs on Windows and Linux, written in Python 3.8

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example:<br>
> python3 setup.py "venv name"

- Once virtual env is built traverse to the Scripts directory in the environment folder just created.
- In the Scripts directory, execute the "activate" script to activate the virtual environment.

## Purpose
> This project adopts the features of the screenshotAssistant project in my repository.
> The big difference is that this program also logs keys in sentence structures and logs to a file.
> Then that file is reformatted and saved in a new file with a clean, easily readable format.

## How to use
- Open up shell such as command prompt or terminal
- Enter directory containing program and execute in shell
- Open the graphical file manager and go to path specified in program
- Click on the open CMD and hit enter
- Check out the file manager to visualize the screenshots and logging data
- Any keys pressed will be buffered into a variable and will be entered as a sentence when enter is pressed
- Hit escape to pause program and cleanly format key logs to be written to a new file
- If you want to start again hit enter again
- OR if you would like to exit hit Ctrl + C (KeyboardInterrupt)
 