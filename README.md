# esp8266Wifi
The ESP8266 is a pretty amazing IoT device with built-in WiFi capability. It is the size of a postage stamp and  you can get it in single quantity for about 3 bucks on Ebay if you don't mind wiring it up yourself. A development board with breakouts and a USB port is available [on Amazon at 2 for $15](https://www.amazon.com/gp/product/B01IK9GEQG/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1).

This project is a python application that can serve up a little website on the ESP8266 running as a WiFi access point. It can scan for other visible access points, indicates if they are open or require a password, and lets you record their password to a file on the ESP8266. Very cool that a cheap little device with 25kb of program RAM can do this.

## Motivation

For myself, I write Python apps for the 8266 that attempt to connect to a remote server over WiFi. The 8266 can scan for and connect to open access points with no problem, but at my house everything that's visible requires a password. This app lets me bring up a webpage served by the 8266 itself and enter in passwords for access points. These are preserved in a file on the device. Then other programs running on the device later could read the file and know how to connect.

## Preparation

I assume you have at least some minimal ESP8266 developer chops in order to install and run this software.

You must have [Micropython firmware flashed](https://learn.adafruit.com/building-and-running-micropython-on-the-esp8266/overview) to the ESP8266, there are plenty of tutorials around on how to do this. You will also need to have a way to send program files to it. I use [Adafruit ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) but you may prefer some other technique such as [webrepl](https://micropython.org/webrepl/). Also you will want a serial port terminal app such as Putty so that you can access a command-line Python prompt. And, of course, typically some form of USB-to-serial connection to the 8266 that let's you initially invoke the application.

## Installation

Installation consists of transporting the three Python files in this project to the device filesystem, and then initiating a terminal session to get to the Python prompt over the serial port;

    >>> import webserv

You should see a "server at IP 192.168.4.1" message printed to the console (possibly other messages as well from the firmware). 

## Connecting

Pick up your cellphone, go to Settings (on Android phones) and look at the available WiFi access points. One of them should be **ESP-AP**, if you see this you are golden. Connect to it, you will initially be asked for a password. It is **micropythoN** (lower case with a capital N). On Android you may very well see a popup alerting that this access point has no internet connection, and you will need to check OK to remain connected. Which you will obviously do.

## The web app

Assuming you were able to connect, you can now bring up a browser on your phone - Chrome or whatever - and for the URL you will **enter the IP address 192.168.4.1**. This should bring up the initial web page.

*image to be placed here*

The initial page has a *scan button* and an on/off button for what may or may not be an LED on pin 2 just for fun. Press the scan button and the device will spend a few seconds looking for visible access points, then print them to a table.

*image to be placed here*

The table will show;
* the access point name (if not hidden)
* whether of not it requires a password
* the signal strength in negative decibels, lower is stronger
* whether or not you have successfully connected to it in the "known" column (Y or N)
* a radio button in the Set column

If you press the radio button associated with an access point you will be sent to a page where you can type in the password and an optional name for that access point.

*image to be placed here*

You will see a *test*, *save*, and the usual *scan* button. 

If you press "test" the device will attempt to connect to that access point. This can take a while, so in the meantime you get sent back to the initial page. Wait 10-15 seconds, the results will be saved to a file. Subsequently initiating a scan again, you should see a Y or N indicating success or failure. You can try again if you like.

If you press "save" your input is merely saved to the file as-is with no connect attempt. Or you can "scan" and get back to the table of access points.

## Caveats

At the time of this writing, version 1.9 of Micropython was recently released. I've found that with the previous version the ESP8266 was able to attempt connection to other remote access points with no problem while still serving as an access point itself. With 1.9 this seems somewhat broken. If you attempt to connect and it fails, your connection to the web app is scrogged. You will need to WiFi disconnect from the 8266 device and reconnect in order to recover. The program will have recorded the results of the connect attempt, however.

## Acknowledgement

I didn't originally have a clue about how to do this, but I came across [this posting](https://lab.whitequark.org/notes/2016-10-20/controlling-a-gpio-through-an-esp8266-based-web-server/) from "whitequark’s lab notebook" with Python source code for serving up a web page and controlling a pin. That gave me the basic technique, and I went from there (still no small effort).