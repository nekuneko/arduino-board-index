# NekuNeko Package Lists for the Arduino v1.6.4+ Board Manager [![Build Status](https://travis-ci.org/adafruit/arduino-board-index.svg?branch=gh-pages)](https://travis-ci.org/adafruit/arduino-board-index)

This repo contains the custom `package_nekuneko_index.json` file that can be used to add new
third party boards to the Arduino v1.6.4+ IDE. Please copy this line and add it to your Arduino IDE preferences box:

`https://nekuneko.github.io/arduino-board-index/package_nekuneko_index.json`


## List of 3rd Party Boards

https://github.com/arduino/Arduino/wiki/Unofficial-list-of-3rd-party-boards-support-urls


## Updating instructions

You can read an extended explanation [here](https://learn.adafruit.com/using-board-package-tool-to-update-adafruit-arduino-packages), this is just a resume.
First install the following requirements:

```
sudo apt install python3 python3-pip
python3 -m pip install gitpython click configparser
```
Optionally install python findimports module to check if there are missing dependencies:

`python3 -m pip install findimports`

You can check missing import dependencies by:

`findimports bpt.py btp_modules.py`

Install the missing dependencies if so and next check for updates by issuing this command.

`python3 bpt.py check-updates`

Finally perfom the update by issuing one of these commands.

```
python3 bpt.py update-index "NeKuNeKo SAMD Boards"
python3 bpt.py update-index "NeKuNeKo nRF52 Boards"
```

Commit the changes and you are done.


It could be necessary to add manually the propper submodules on the repo's root. In example:

```
git submodule add https://github.com/adafruit/Adafruit_nRFCrypto.git libraries/Adafruit_nRFCrypto
git submodule add https://github.com/adafruit/Adafruit_TinyUSB_ArduinoCore.git cores/nRF5/TinyUSB/Adafruit_TinyUSB_ArduinoCore
```

Thanks to Adafruit, Ha Thatch, Tony DiCola and so many other maintainers to make this possible.