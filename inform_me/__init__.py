# for executing the alert commands
import subprocess as sp
# for setting up custom timer
from threading import Timer

#GLOBAL VARIABLES
__version__ = '0.1.2'
m=0
s=0
msg=''


def execute(command):
    '''
    Executes command as a subprocess.
    
    Possible format for command
    1) String
        ex: "cd Downloads" or "pip install numpy --user"

    2) List of Strings (first string in List should be the name of command, rest are Arguments)
        ex: ["cd", "Downloads"] or ["pip", "install", "numpy", "--user"]

    Returns: CompletedProcess Object (https://docs.python.org/3.6/library/subprocess.html#subprocess.CompletedProcess)
    '''

    # convert to list of string format
    if not isinstance(command, list):
        command = command.split(' ')

    # run command and capture output, redirect stderr to stdout
    result = sp.run(command, stdin=None, stdout=sp.PIPE, stderr=sp.STDOUT, shell=False)
    return result


def inform(sound_duration=0.5, notification=True, popup=True, message='Your process has completed!'):
    '''
    This method sends an alert on the screen when it gets executed.
    This method would come handy when you're working on something (a piece of code) which runs for a long time and you would like to be notified when it completes.
    An alert (sound, popup window and notification box) be sent when this method executes.
    Placing it right after the 'time consuming' piece of code would enable know 
    duration (in seconds): how long to generate the sound
    alert (bool): show the popup alert window if true, else do not show the popup window 
    '''
    try:
        # make a sound 
        # command: "timeout --kill-after=0.5s --signal=KILL 0.5s speaker-test --test sine --frequency 1000"
        duration_str = "{dur}s".format(dur=sound_duration)
        command = ["timeout", "--kill-after={dur}".format(dur=duration_str), "--signal=KILL",
                   duration_str, "speaker-test", "--test", "sine", "--frequency", "1000"]
        execute(command)

        # show notification box
        # command: "notify-send 'Title' 'Message'"
        if notification:
            command = ["notify-send", "Notification from inform_me", message]
            execute(command)

        # show popup message
        # command: "zenity --info --text 'message' --title 'Title' --width 250 --height 50"
        if popup:
            command = ["zenity", "--info", "--text", message, "--title",
                       "Popup message from inform_me", "--width", "250", "--height", "50"]
            execute(command)
    except Exception as e:
        print('An error occured.\n',e)


#helper mehtod for notify_after method.
def timer():
    message=msg if msg else 'Your '+str(m)+' Minutes and '+str(s)+' Seconds timer has lapsed!'
    inform(message = message)


def inform_after(seconds=10, minutes=0, notification=True, popup=True, message=None):
    '''
    This function sends an alert (sound, popup window and notification box) when the after the specified time.
    This method can be used as a timer.
    '''
    try:
        total_sec = (minutes*60) + seconds
        t = Timer(total_sec, timer)
        t.start()
        global m
        m = minutes
        global s
        s = seconds
        global msg
        msg = message
    
    except Exception as e:
        print('An error occured.\n',e)

