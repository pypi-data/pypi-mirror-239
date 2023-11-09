# browserpedals


[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![ru](https://img.shields.io/badge/язык-рус-red.svg)](README.ru.md)


This program can be used to control any video/audio in a web browser with foot pedals - pause/play or jump back - even when the web browser is not in focus.

This may be helpful during transcribing - listening to a video in a web browser and typing the spoken text on a keyboard, while using foot pedals to periodically pause the video or jump back in time.


## Prerequisites:

- Python 3
- Mozilla Firefox web browser


## Installation:

On Linux, open command line and type:
```
~> python3 -m pip install --no-cache-dir browserpedals
```

On Windows, open command line or Windows PowerShell and type:
```
~> py -m pip install --no-cache-dir browserpedals
```


## Usage:

Plug the pedals into a USB port.

Run the program. If the program was installed as shown above, a shortcut (`BrowserPedals` icon) was automatically created on the Desktop and in the Applications menu. In this case the program can be launched using this shortcut, or by right-clicking on the video or audio file which we want to open and selecting `BrowserPedals` program from the drop-down menu.

Technically, the program `browserpedals.py` (as well as its submodules `usepedals.py` (just test pedals) and `detectpedals.py` (just detect pedals)) can also be run as Python scripts from command line as follows:
```
~> python3 browserpedals.py
```

The program uses web browser as user interface.

Wait for a new browser window to appear. It may take up to a minute.

The home page will open with information about the program.

Also, a dialog window with step-by-step instructions will open, where the user will be asked to test the pedals to make sure they are working, and to automatically recognize the pedals if they are unknown. The dialog window will close after the pedals pass the test.

In the browser window, navigate to any Web site containing a video/audio (or to a local video/audio file: In Firefox press `Alt` key to open the browser menu and choose `File--Open File`. In Chrome and Edge press `Ctrl+O` key).

### How to start controlling a video/audio with pedals:

To start controlling a video/audio with pedals, click `Play` button on the video with the mouse at least once.

To stop controlling the video/audio with pedals, click `Pause` button on the video with the mouse (not with pedals).
After that, you can start controlling any other video on the site by clicking it's `Play` button.

You may have to wait for about a minute before the program starts controlling the video, or click `Play` button on the video with the mouse several times.

### How to control the video/audio with pedals:

To pause/play the video, press right pedal (or other pedal of your choice).

To jump back in the video, press left pedal (or other pedal of your choice).

### Additional option to create subtitles:

The program can be used to create subtitles: after every Play and Pause using pedals, SRT subtitle data for the played fragment is copied to the clipboard and can be pasted into any text.

So, plain text file like this one:
```
What's up guys? This is the first subtitle.
And this is the second subtitle.
```
after pasting subtitle data from the clipboard will become an SRT subtitle file:
```
1
00:00:00,100 --> 00:00:01,900
What's up guys? This is the first subtitle.

2
00:00:02,000 --> 00:00:04,266
And this is the second subtitle.

```

To use subtitles option on Linux, additionally install xclip:
```
sudo apt-get install xclip
```

Also, the program can be used to periodically pause a video and copy timestamps to clipboard.


## Automatic pedals detection:

Currently, the program supports just one specific type of pedals out of the box - the "Thrustmaster wheel" foot pedals (Thrustmaster 360 SPIDER PC).

If other pedals are used, the program will attempt to recognize them automatically. Just plug the pedals into the PC, run the program, and follow the instructions on the screen. If the pedals are recognized successfully, the information is saved to the file `auto_detected_pedals.txt`, and next time the program is run the new pedals will be recognized automatically.

Users who use pedals which where successfully recognized by the program, can send the above file to the program's developer so new versions of the program could support these pedals out of the box:

[Email](mailto:shmygov@rambler.ru)

[Site](https://github.com/shmygov/browserpedals)

Exact location of this and other files used by the program can be found on the informational page - the first page opened by the browser when the program starts.

Currently supported pedal roles are "Pause/Play pedal" and "Jump Back pedal". User can assign any role to any pedal, can use both pedals or just one. This is done automatically by running the program and following the instructions on the screen.

(Technically, the `auto_detected_pedals.txt` file can also be edited manually.)


## Changing the program's options:

The `browserpedals_options.txt` text file contains several options which users can edit to change the way the program behaves.
This file is located in the application's editable data directory:

On Linux:
```
/home/<user_name>/.local/share/browserpedals/browserpedals_options.txt
```

On Windows:
```
C:\Users\<user_name>\AppData\Local\dmitrish\browserpedals\browserpedals_options.txt
```

Exact location of this and other files used by the program can be found on the informational page - the first page opened by the browser when the program starts.

Available options:

*browser*: By default, the program opens Firefox browser. To use another browser, change the *value* of the *browser* option in the options file correspondingly. So far, the program was tested with Firefox, Chrome, and Edge browsers.

*user_interface*: By default, the program uses web browser as graphical user interface during pedals recognition. To use command line for pedals recognition, change the *value* of the *user_interface* option in the options file from "browser" to "command_line".

*jump_back_sec*: By default, pressing the "jump back" pedal rewinds the video 5 seconds back. To use another time jump, change the *value* of the *jump_back_sec* option in the options file correspondingly. It may be any number, possibly with a fractional part. 

*subtitles_to_clipboard*: If this feature is enabled, every time user presses the pedal to Play the video and then presses the pedal to Pause it, subtitle timing data in SRT format is created for the video fragment just played (Play starts the subtitle, Pause ends the subtitle), and this SRT data is copied to the clipboard, so the user can paste it into any text file. To enable this feature, set the *value* of the *subtitles_to_clipboard* option in the options file to 1. To disable this feature, set it to 0. To copy just timestamps to clipboard every time Pause pedal is pressed, instead of copying subtitle data (timestamp format is specified in the option called *periodic_timestamp_format*), set the value to -1.  
*Important:* On Linux, to use this feature instal *xclip*: `sudo apt-get install xclip`

*pause_period_sec*: If this feature is enabled, the video/audio periodically pauses at certain time points in the video. During each such pause, current time point in the video/audio is copied to the clipboard, so the user can paste it into any text file. The string copied to the clipboard will have the format specified in the next option of the options file called *periodic_timestamp_format*. To enable this feature, set the *value* of the *pause_period_sec* option in the options file to desired time interval between pauses, in seconds, possibly with a fractional part. To disable this feature, set the value to 0.  
*Important:* On Linux, to use this feature instal *xclip*: `sudo apt-get install xclip`

*periodic_timestamp_format*: If the feature *pause_period_sec* is enabled or the value of feature *subtitles_to_clipboard* is set to -1, this option specifies the format of the timestamp string which is copied to the clipboard during each periodic pause. Set the *value* of the *periodic_timestamp_format* option in the options file to a Python format string, for example it can contain format elements such as {SS:04d} - in this string you can use variables SS (time in seconds), MM (time in minutes), hh (hours), mm (minutes), ss (seconds), uu (milliseconds).


## Browser data:

When this program opens a web browser, it uses a browser user's profile which is different from default profile used when the browser is opened standard way. All browser data (including user preferences, browser cache, history, bookmarks, installed extensions, etc.) used by web browsers opened by this program are stored in the following location:

On Linux:
```
home/<user_name>/.local/share/browserpedals/profiles/
```

On Windows:
```
C:\Users\<user_name>\AppData\Local\dmitrish\browserpedals\profiles\
```

Exact location of this and other files used by the program can be found on the informational page - the first page opened by the browser when the program starts.


## Installing the Web Driver (optional):

The program comes with a pre-installed Web Driver for Firefox browser, so if you want to use Firefox it will work out of the box. However, if you want to use another browser like Chrome or Edge, you have to install corresponding Web Driver manually as described below. Also, in case of Chrome or Edge you will have to periodically upgrade the Web Driver to match the current version of automatically upgraded Chrome or Edge browser.

Install the Web Driver for the browser you want to use. The download links are on the site:

[Download a Web Driver](https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location/#download-the-driver)

**Important**: For all browsers except Firefox, the version of Web Driver file should match the current version of your browser.

Open the downloaded archive and extract the Web Driver executable. For Firefox browser the Web Driver file name is usually `geckodriver`. For Chrome browser the Web Driver file name is usually `chromedriver`. For Edge browser the Web Driver file name is usually `msedgedriver.exe`.

Place the Web Driver file into the corresponding sub-directory of the program's data directory:

On Linux:
```
/home/<user_name>/.local/share/browserpedals/web_driver/linux64
```

On Windows:
```
C:\Users\<user_name>\AppData\Local\dmitrish\browserpedals\web_driver\win64
```

Exact location of this and other files used by the program can be found on the informational page - the first page opened by the browser when the program starts.


## Supported platforms:

This code was tested on Linux (Ubuntu) with Firefox and Chrome browsers, and on Windows with Firefox, Chrome, and Edge browsers.

Following software is used by the program (If the program is installed using PIP, everything is installed automatically):

"Selenium" project to control the browser:

[https://www.selenium.dev/selenium/docs/api/py/api.html](https://www.selenium.dev/selenium/docs/api/py/api.html)

"evdev" package to manage the pedals (if Linux is used):

[https://pypi.org/project/evdev/](https://pypi.org/project/evdev/)

[https://github.com/gvalkov/python-evdev](https://github.com/gvalkov/python-evdev)

[https://python-evdev.readthedocs.io/en/latest/](https://python-evdev.readthedocs.io/en/latest/)

"PyWinUSB" package to manage the pedals (if Windows is used):

[https://pypi.org/project/pywinusb/](https://pypi.org/project/pywinusb/)

[https://github.com/rene-aguirre/pywinusb](https://github.com/rene-aguirre/pywinusb)



