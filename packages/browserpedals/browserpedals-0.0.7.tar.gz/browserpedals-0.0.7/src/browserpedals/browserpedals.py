import os
import sys
import time
import json
import pyperclip    # pip install pyperclip    # Linux: sudo apt-get install xclip
import math

from selenium.common.exceptions import (StaleElementReferenceException, NoSuchWindowException,
                                        WebDriverException, InvalidSessionIdException, TimeoutException,
                                        NoSuchFrameException)
from selenium.webdriver.common.by import By

try:
    from urllib.parse import urlparse, urljoin
    from urllib.request import pathname2url
except ImportError:
    # backwards compatability
    from urlparse import urlparse, urljoin
    from urllib import pathname2url

#try:
#    import importlib.resources as dist_resources
#except ImportError:
    # Try backported to PY<37 `importlib_resources`.
import importlib_resources as dist_resources

if __name__ == '__main__':
    import pedals, browserpedals_options, scripts, web_driver
    from pedals.usepedals import read_or_find_pedals
    from pedals.detect.detectpedals import pedals_file_path
    from pedals.detect.ui.browserui import ui_open_css_file_path
    from pedals.detect.ui.cmdlineui import CmdlineUI
    from browserauto.webdriverex import WebDriverEx
    from browserauto.multitab import to_active_tab
    from pedals.detect.ui.i18n.data_dirs.appdata import (get_user_data_dir,
                                                         install_resource, install_and_read_resource)
    from pedals.detect.ui.i18n.languages import init_languages, select_language, set_language, get_language
else:
    from . import pedals, browserpedals_options, scripts, web_driver
    from .pedals.usepedals import read_or_find_pedals
    from .pedals.detect.detectpedals import pedals_file_path
    from .pedals.detect.ui.browserui import ui_open_css_file_path
    from .pedals.detect.ui.cmdlineui import CmdlineUI
    from .browserauto.webdriverex import WebDriverEx
    from .browserauto.multitab import to_active_tab
    from .pedals.detect.ui.i18n.data_dirs.appdata import (get_user_data_dir,
                                                          install_resource, install_and_read_resource)
    from .pedals.detect.ui.i18n.languages import init_languages, select_language, set_language, get_language

import struct
def is_64bit():
    return (struct.calcsize('P') * 8 == 64)


MONITOR_PERIOD_SEC = 1.5
SITE_SETUPS_IN_ONE_RUN = 10
MAX_FRAMES_WITHOUT_SORTING = 2
GET_TIMEOUT_SEC = 10


APP_DATA_DIR = get_user_data_dir()


START_PAGE_DIR1 = "detect"
START_PAGE_DIR2 = "ui"
START_PAGE_DIR3 = "start"
START_PAGE_FILE_NAME = "browserpedals.html"

START_PAGE_DIR = "start"

WEB_DRIVER_DIR = "web_driver"
WEB_DRIVER_SUBDIR = None
FIREFOX_DRIVER_FILE_NAME = None
CHROME_DRIVER_FILE_NAME = None
EDGE_DRIVER_FILE_NAME = None
if sys.platform == "linux" or sys.platform == "linux2":
    if is_64bit():
        WEB_DRIVER_SUBDIR = "linux64"
    else:
        WEB_DRIVER_SUBDIR = "linux32"
    FIREFOX_DRIVER_FILE_NAME = "geckodriver"
    CHROME_DRIVER_FILE_NAME = "chromedriver"
    EDGE_DRIVER_FILE_NAME = 'msedgedriver'
elif sys.platform == "darwin":
    if is_64bit():
        WEB_DRIVER_SUBDIR = "macos64"
    else:
        WEB_DRIVER_SUBDIR = "macos32"
    FIREFOX_DRIVER_FILE_NAME = "geckodriver"
    CHROME_DRIVER_FILE_NAME = "chromedriver"
    EDGE_DRIVER_FILE_NAME = 'msedgedriver'
elif sys.platform == "win32":
    if is_64bit():
        WEB_DRIVER_SUBDIR = "win64"
    else:
        WEB_DRIVER_SUBDIR = "win32"
    FIREFOX_DRIVER_FILE_NAME = "geckodriver.exe"
    CHROME_DRIVER_FILE_NAME = "chromedriver.exe"
    EDGE_DRIVER_FILE_NAME = 'msedgedriver.exe'

JS_DIR = "js"

PAUSE_PLAY_JS_FILE_NAME = "pause_play.js"
JUMP_BACK_JS_FILE_NAME = "jump_back.js"
SITE_SETUP_JS_FILE_NAME = "site_setup.js"
FIND_LAST_PLAYED_ELEMENT_JS_FILE_NAME = "find_last_played_element.js"
GET_TAB_SELECTION_TIME_JS_FILE_NAME = "get_tab_selection_time.js"
OPTIONS_PAGE_SETUP_JS_FILE_NAME = "options_page_setup.js"
OPTIONS_PAGE_UPDATE_JS_FILE_NAME = "options_page_update.js"


OPTIONS_FILE_NAME = "browserpedals_options.txt"

PROFILES_DIR_NAME = "profiles"

FIREFOX_PROFILE_NAME = "firefox"
CHROME_PROFILE_NAME = "chrome"
EDGE_PROFILE_NAME = "edge"

FIREFOX_PROFILE_PATH = os.path.join(APP_DATA_DIR, PROFILES_DIR_NAME, FIREFOX_PROFILE_NAME)
CHROME_PROFILE_PATH = os.path.join(APP_DATA_DIR, PROFILES_DIR_NAME, CHROME_PROFILE_NAME)
EDGE_PROFILE_PATH = os.path.join(APP_DATA_DIR, PROFILES_DIR_NAME, EDGE_PROFILE_NAME)


s = install_and_read_resource(APP_DATA_DIR, browserpedals_options, OPTIONS_FILE_NAME)
options_file_dict = eval(s)
options_file_path = os.path.join(APP_DATA_DIR, OPTIONS_FILE_NAME)

profiles_dir_path = os.path.join(APP_DATA_DIR, PROFILES_DIR_NAME)


WEB_DRIVER_DATA_DIR = os.path.join(APP_DATA_DIR, WEB_DRIVER_DIR, WEB_DRIVER_SUBDIR)

firefox_driver_path = install_resource(WEB_DRIVER_DATA_DIR, 
                                       web_driver, FIREFOX_DRIVER_FILE_NAME, WEB_DRIVER_SUBDIR)

chrome_driver_path = install_resource(WEB_DRIVER_DATA_DIR, 
                                      web_driver, CHROME_DRIVER_FILE_NAME, WEB_DRIVER_SUBDIR)

edge_driver_path = install_resource(WEB_DRIVER_DATA_DIR, 
                                    web_driver, EDGE_DRIVER_FILE_NAME, WEB_DRIVER_SUBDIR)


JUMP_BACK_SEC = options_file_dict['options']['jump_back_sec']['value']
BROWSER = options_file_dict['options']['browser']['value']
USER_INTERFACE = options_file_dict['options']['user_interface']['value']

SUBTITLES_TO_CLIPBOARD = options_file_dict['options']['subtitles_to_clipboard']['value']
MIN_GAP_BETWEEN_SUBTITLES_SEC = 0.02

PAUSE_PERIOD_SEC = options_file_dict['options']['pause_period_sec']['value']
PAUSE_ZONE_SEC = 0.2    # Video/Audio will pause when currentTime gets closer than +/-PAUSE_ZONE_SEC to pause time points.
PAUSE_PRECISION_SEC = 0.01    # Shift currentTime forward out of the pause zone by PAUSE_PRECISION_SEC so Video can play again.

PERIODIC_TIMESTAMP_FORMAT = options_file_dict['options']['periodic_timestamp_format']['value']


driver = None


pause_play_script = dist_resources.files(scripts).joinpath(JS_DIR).joinpath(PAUSE_PLAY_JS_FILE_NAME).read_text(encoding='utf-8')

jump_back_script = dist_resources.files(scripts).joinpath(JS_DIR).joinpath(JUMP_BACK_JS_FILE_NAME).read_text(encoding='utf-8')

site_setup_script = dist_resources.files(scripts).joinpath(JS_DIR).joinpath(SITE_SETUP_JS_FILE_NAME).read_text(encoding='utf-8')

find_last_played_element_script = dist_resources.files(scripts).joinpath(JS_DIR).joinpath(FIND_LAST_PLAYED_ELEMENT_JS_FILE_NAME).read_text(encoding='utf-8')

get_tab_selection_time_script = dist_resources.files(scripts).joinpath(JS_DIR).joinpath(GET_TAB_SELECTION_TIME_JS_FILE_NAME).read_text(encoding='utf-8')



options_page_setup_script = dist_resources.files(scripts).joinpath(JS_DIR).joinpath(OPTIONS_PAGE_SETUP_JS_FILE_NAME).read_text(encoding='utf-8')

options_page_update_script = dist_resources.files(scripts).joinpath(JS_DIR).joinpath(OPTIONS_PAGE_UPDATE_JS_FILE_NAME).read_text(encoding='utf-8')

start_page_path = install_resource(os.path.join(APP_DATA_DIR, START_PAGE_DIR), 
                                   pedals, START_PAGE_FILE_NAME,
                                   START_PAGE_DIR1, START_PAGE_DIR2, START_PAGE_DIR3)
s = ""
with open(start_page_path, 'r', encoding='utf_8') as f:
    s = f.read()
s = s.replace("application_data_directory", APP_DATA_DIR)
s = s.replace("ui_appearance_css_file", ui_open_css_file_path)
s = s.replace("options_text_file", options_file_path)
s = s.replace("browser_profiles_directory", profiles_dir_path)
s = s.replace("auto_detected_pedals_file", pedals_file_path)
s = s.replace("web_driver_directory", WEB_DRIVER_DATA_DIR)
with open(start_page_path, 'w', encoding='utf_8') as f:
    f.write(s)


def path2url(path):
    return urljoin('file:', pathname2url(path))

current_url = path2url(start_page_path)


def try_alternative_navigate(url):
    driver.set_page_load_timeout(GET_TIMEOUT_SEC)
    driver.get(url) #may block

def go_to_start():
    global current_url

    current_url = path2url(start_page_path)
    while True:
        driver.wait_for_page()
        time.sleep(1)
        try:
            try_alternative_navigate(current_url)
            break
        except:
            pass
    if driver.err_msg != '':
        driver.execute_script(options_page_setup_script, driver.err_msg)

def update_start():
    lang = get_language()
    driver.execute_script(options_page_update_script, lang)


def switch_to_frame(elem):
    return driver.switch_to.frame(elem, (StaleElementReferenceException, NoSuchWindowException,
                                         InvalidSessionIdException, TimeoutException, NoSuchFrameException))

def sort_frames(frames):
    if len(frames) <= MAX_FRAMES_WITHOUT_SORTING:
        return (True, frames)

    scroll_x = driver.execute_script("return window.pageXOffset;", exceptions=(NoSuchWindowException, WebDriverException))
    scroll_y = driver.execute_script("return window.pageYOffset;", exceptions=(NoSuchWindowException, WebDriverException))
    inner_width = driver.execute_script("return window.innerWidth;", exceptions=(NoSuchWindowException, WebDriverException))
    inner_height = driver.execute_script("return window.innerHeight;", exceptions=(NoSuchWindowException, WebDriverException))
    condition = (((not scroll_x) and (scroll_x != 0)) or 
                 ((not scroll_y) and (scroll_y != 0)) or 
                 ((not inner_width) and (inner_width != 0)) or 
                 ((not inner_height) and (inner_height != 0)))
    if condition:
        return (False, frames)
    visible_min_x = scroll_x
    visible_max_x = scroll_x + inner_width
    visible_min_y = scroll_y
    visible_max_y = scroll_y + inner_height

    visible_frames = []

    for element in frames:
        try:
            element_rect = element.rect
        except (StaleElementReferenceException, WebDriverException):
            continue
        if not element_rect:
            continue
        elem_min_x = element_rect['x']
        elem_max_x = elem_min_x + element_rect['width']
        elem_min_y = element_rect['y']
        elem_max_y = elem_min_y + element_rect['height']

        elem_is_visible = ((elem_max_y > visible_min_y) and (elem_min_y < visible_max_y) and 
                           (elem_max_x > visible_min_x) and (elem_min_x < visible_max_x))
        if elem_is_visible:
            visible_frames.append(element)

    return (True, visible_frames)

site_setups_count = 0

RES_UNDEF = 0
RES_FOUND = 1
RES_SETUP = 2
RES_ONE_RUN = 3
RES_ERROR = 4

def in_browser_and_frames(func):
    res = func();
    if res in [RES_FOUND, RES_ONE_RUN, RES_ERROR]:
        return res

    if site_setups_count > SITE_SETUPS_IN_ONE_RUN:
        return RES_ONE_RUN

    frames = driver.find_elements(By.TAG_NAME, "IFRAME", (NoSuchWindowException, WebDriverException))
    if not frames:
        return RES_ERROR

    res = sort_frames(frames)
    if not res[0]:
        return RES_ERROR
    sorted_frames = res[1]


    for element in sorted_frames:
        r = switch_to_frame(element)
        if not r:
            return RES_ERROR

        res = in_browser_and_frames(func)
        if res in [RES_FOUND, RES_ONE_RUN, RES_ERROR]:
            return res

        r = driver.switch_to.parent_frame((StaleElementReferenceException, NoSuchWindowException,
                                           InvalidSessionIdException, TimeoutException,
                                           NoSuchFrameException))
        if not r:
            return RES_ERROR

    return RES_UNDEF

def do_in_browser_and_frames(func):
    global site_setups_count

    r = driver.switch_to.default_content((TimeoutException,))
    if not r:
        return

    site_setups_count = 0

    res = in_browser_and_frames(func)
    if res in [RES_ONE_RUN, RES_ERROR]:
        r = driver.switch_to.default_content((TimeoutException,))
        if not r:
            return


subtitle_start_time = 0
subtitle_index = 0

def copy_subtitle_to_clipboard(subtitle_stop_timestamp):
    global subtitle_start_time
    global subtitle_index

    # SRT subtitles file format:

    # 1
    # 00:00:00,100 --> 00:00:01,900
    # What's up guys? Just in here with
    #
    # 2
    # 00:00:02,000 --> 00:00:04,266
    # BCGessentials.com back with
    #

    # hours:minutes:seconds,milliseconds

    subtitle_stop_time = float(subtitle_stop_timestamp)

    # Following case can happen after Jump Back in the video:
    if subtitle_stop_time <= subtitle_start_time:
        subtitle_start_time = subtitle_stop_time
        subtitle_index -= 1
        if subtitle_index < 0:
            subtitle_index = 0
        pyperclip.copy('')
        return

    # If user copied previous index to the clipboard, we use it to change the current index.
    # We asume that this is the case if the clipboard contains a string representing some integer.
    si = pyperclip.paste()
    if si.isdigit():
        subtitle_index = int(si)

    subtitle_index += 1

    floor_1 = math.floor(subtitle_start_time)
    hours_1 = floor_1 // 3600
    minutes_1 = (floor_1 - (hours_1 * 3600)) // 60
    seconds_1 = floor_1 - (hours_1 * 3600) - (minutes_1 * 60)
    milliseconds_1 = math.floor((subtitle_start_time - floor_1) * 1000)

    hh_1 = f'{hours_1:02d}'
    mm_1 = f'{minutes_1:02d}'
    ss_1 = f'{seconds_1:02d}'
    uuu_1 = f'{milliseconds_1:03d}'

    floor_2 = math.floor(subtitle_stop_time)
    hours_2 = floor_2 // 3600
    minutes_2 = (floor_2 - (hours_2 * 3600)) // 60
    seconds_2 = floor_2 - (hours_2 * 3600) - (minutes_2 * 60)
    milliseconds_2 = math.floor((subtitle_stop_time - floor_2) * 1000)

    hh_2 = f'{hours_2:02d}'
    mm_2 = f'{minutes_2:02d}'
    ss_2 = f'{seconds_2:02d}'
    uuu_2 = f'{milliseconds_2:03d}'

    si = str(subtitle_index)

    pyperclip.copy(si+'\n'+hh_1+':'+mm_1+':'+ss_1+','+uuu_1+' --> '+hh_2+':'+mm_2+':'+ss_2+','+uuu_2+'\n')

    subtitle_start_time = float(subtitle_stop_timestamp) + MIN_GAP_BETWEEN_SUBTITLES_SEC

def copy_time_to_clipboard(current_time):
    SS = math.floor(current_time)    # If only seconds are used to express time
    MM = SS // 60    # If only minutes are used to express time
    hh = SS // 3600    # Hours
    mm = (SS - (hh * 3600)) // 60    # Minutes remaining after hours
    ss = SS - (hh * 3600) - (mm * 60)    # Seconds remaining after remaining minutes
    uu = math.floor((current_time - SS) * 1000)    # milliseconds

    txt = PERIODIC_TIMESTAMP_FORMAT.format(SS=SS, MM=MM, hh=hh, mm=mm, ss=ss, uu=uu)

    pyperclip.copy(txt)

def copy_timestamp_to_clipboard(current_timestamp):
    current_time = float(current_timestamp)
    copy_time_to_clipboard(current_time)

def copy_periodic_timestamp_to_clipboard(periodic_timestamp):
    periodic_time = float(periodic_timestamp)
    periodic_time -= PAUSE_ZONE_SEC + PAUSE_PRECISION_SEC
    copy_time_to_clipboard(periodic_time)

last_manually_played_element_time = 0

def pause_play():
    global last_manually_played_element_time

    resStr = driver.execute_script(pause_play_script, last_manually_played_element_time, 
                                   exceptions=(NoSuchWindowException,))

    resDict = None
    if resStr and (resStr != ""):
        try:
            resDict = json.loads(resStr)
        except:
            return False
    else:
        return False

    if resDict:
        manually_played_element_timestamp = resDict.get("timestamp")
        pause_timestamp = resDict.get("pause_timestamp")
        play_timestamp = resDict.get("play_timestamp")
    else:
        return False

    if not manually_played_element_timestamp:
        return False
    manually_played_element_time = int(manually_played_element_timestamp)
    if manually_played_element_time > last_manually_played_element_time:
        last_manually_played_element_time = manually_played_element_time
    elif manually_played_element_time == 0:
        last_manually_played_element_time = 0
    if SUBTITLES_TO_CLIPBOARD > 0:
        if pause_timestamp and pause_timestamp != "0":
            copy_subtitle_to_clipboard(pause_timestamp)
    elif SUBTITLES_TO_CLIPBOARD < 0:
        if pause_timestamp and pause_timestamp != "0":
            copy_timestamp_to_clipboard(pause_timestamp)
    if PAUSE_PERIOD_SEC > 0:
        if play_timestamp and play_timestamp != "0":
            copy_periodic_timestamp_to_clipboard(play_timestamp)
    return True

def jump_back():
    global last_manually_played_element_time
    global subtitle_start_time
    global subtitle_index

    resStr = driver.execute_script(jump_back_script, last_manually_played_element_time,
                                   JUMP_BACK_SEC, exceptions=(NoSuchWindowException,))

    resDict = None
    if resStr and (resStr != ""):
        try:
            resDict = json.loads(resStr)
        except:
            return False
    else:
        return False

    if resDict:
        manually_played_element_timestamp = resDict.get("timestamp")
        jump_timestamp = resDict.get("jump_timestamp")
    else:
        return False

    if not manually_played_element_timestamp:
        return False
    manually_played_element_time = int(manually_played_element_timestamp)
    if manually_played_element_time > last_manually_played_element_time:
        last_manually_played_element_time = manually_played_element_time
    elif manually_played_element_time == 0:
        last_manually_played_element_time = 0
    # If we pressed "Pause" pedal after an interval of silence, we should press "Jump Back" pedal.
    # After that, silence preiod will not increase the subtitle index counter,
    # and the start time will be set slightly prior to the end time of silence period.
    if SUBTITLES_TO_CLIPBOARD != 0:
        if jump_timestamp and jump_timestamp != "0":
            subtitle_start_time = float(jump_timestamp) - JUMP_BACK_SEC
            if subtitle_start_time < 0:
                subtitle_start_time = 0
            subtitle_index -= 2
            if subtitle_index < 0:
                subtitle_index = 0
    return True

def site_setup():
    return driver.execute_script(site_setup_script, PAUSE_PERIOD_SEC, PAUSE_ZONE_SEC, PAUSE_PRECISION_SEC,
                                 exceptions=(NoSuchWindowException, InvalidSessionIdException))

def find_last_played_element():
    global last_manually_played_element_time
    global site_setups_count

    manually_played_element_timestamp = driver.execute_script(find_last_played_element_script,
                                                              exceptions=(NoSuchWindowException, TimeoutException))
    if not manually_played_element_timestamp:
        return RES_ERROR
    if manually_played_element_timestamp == "none":
        site_setup()
        site_setups_count = site_setups_count + 1
        return RES_SETUP
    manually_played_element_time = int(manually_played_element_timestamp)
    if manually_played_element_time > last_manually_played_element_time:
        last_manually_played_element_time = manually_played_element_time
        return RES_FOUND
    return RES_UNDEF


find_last_played_in_frames_call_count = 0

def find_last_played_in_frames():
    global find_last_played_in_frames_call_count

    if find_last_played_in_frames_call_count > 0:
        return
    find_last_played_in_frames_call_count = find_last_played_in_frames_call_count + 1

    do_in_browser_and_frames(find_last_played_element)

    find_last_played_in_frames_call_count = find_last_played_in_frames_call_count - 1


def do_site_setup():
    global last_manually_played_element_time

    while True:
        to_active_tab(driver, get_tab_selection_time_script)
        find_last_played_in_frames()
        if last_manually_played_element_time > 0:
            break
        time.sleep(MONITOR_PERIOD_SEC)


def prepare_pedals_cmd():
    if USER_INTERFACE == "command_line":
        select_language(CmdlineUI())
        read_or_find_pedals()


def prepare_pedals():
    if USER_INTERFACE == "browser":
        if __name__ == '__main__':
            from pedals.detect.ui.browserui import BrowserDialogUI
        else:
            from .pedals.detect.ui.browserui import BrowserDialogUI

        dlg = BrowserDialogUI(driver)
        select_language(dlg)
        read_or_find_pedals(act=dlg, dlg=dlg)
        dlg.close()


class BrowserActions:

    def on_pedal_pressed(self, role_name):
        res = False
        if role_name == 'PausePedal':
            res = pause_play()
        elif role_name == 'JumpPedal':
            res = jump_back()
        else:
            raise ValueError
        if not res:
            return False
        return (last_manually_played_element_time > 0)

    def on_pedal_released(self, role_name):
        return True

    def on_timeout(self):
        h = driver.current_window_handle()

        manually_played_element_timestamp = driver.execute_script(find_last_played_element_script,
                                                                  exceptions=(NoSuchWindowException, TimeoutException))
        if (not manually_played_element_timestamp) or (manually_played_element_timestamp == "none"):
            return False
        if manually_played_element_timestamp == "0":
            return False

        return True


def run_loop():
    act = BrowserActions()
    dlg = CmdlineUI()
    while True:
        do_site_setup()
        time.sleep(1)
        read_or_find_pedals(act=act, is_test=False, dlg=dlg)
        time.sleep(1)


def open_file(args):
    global current_url

    if len(args) >= 1:
        if os.path.isfile(args[0]):
            current_url = path2url(args[0])
        else:
            current_url = args[0]
        driver.wait_for_page()
        time.sleep(1)
        try:
            try_alternative_navigate(current_url)
        except TimeoutException:
            driver.wait_for_page()
            time.sleep(1)
            url = driver.current_url()
            hasBody = driver.execute_script("return (document.body != null)")
            if (url != current_url) or not hasBody:
                go_to_start()
        except:
            go_to_start()
    else:
        go_to_start()


def run_main(*args):
    global driver

    init_languages()
    set_language("en")
    prepare_pedals_cmd()

    print("\n" + _("Wait for new browser window to open.") + "\n")

    driver = WebDriverEx(BROWSER, FIREFOX_PROFILE_PATH, CHROME_PROFILE_PATH, EDGE_PROFILE_PATH,
                         FIREFOX_DRIVER_FILE_NAME, CHROME_DRIVER_FILE_NAME, EDGE_DRIVER_FILE_NAME,
                         firefox_driver_path, chrome_driver_path, edge_driver_path)
    open_file(args)
    prepare_pedals()
    update_start()
    run_loop()

if __name__ == '__main__':
    run_main(*sys.argv[1:])

