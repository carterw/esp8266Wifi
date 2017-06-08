# esp8266Wifi
The ESP8266 is a pretty amazing IoT device with built-in WiFi capability. It is the size of a postage stamp and  you can get it in single quantity for about 3 bucks on Ebay if you don't mind wiring it up yourself. A development board with breakouts and a USB port is available [on Amazon at 2 for $15](https://www.amazon.com/gp/product/B01IK9GEQG/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1).

This project is a python application that can serve up a little website on the ESP8266 running as a WiFi access point. It can scan for other visible access points, indicates if they are open or require a password, and lets you record their password to a file on the ESP8266. Very cool that a device the size of a postage stamp with 25kb of program RAM can do this.

## Motivation

For myself, I write Python apps for the 8266 that attempt to connect to a remote server over WiFi. The 8266 can scan for and connect to open access points with no problem, but at my house everything that's visible requires a password. This app lets me bring up a webpage served by the 8266 itself and enter in passwords for access points. These are preserved in a file on the device. Then other programs running on the device later could read the file and know how to connect.

## Preparation

I assume you have at least some minimal ESP8266 developer chops in order to install and run this software.

You must have [Micropython firmware flashed](https://learn.adafruit.com/building-and-running-micropython-on-the-esp8266/overview) to the ESP8266, there are plenty of tutorials around on how to do this. You will also need to have a way to send program files to it. I use [Adafruit ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) but you may prefer some other technique such as [webrepl](https://micropython.org/webrepl/). Also you will want a serial port terminal app such as Putty so that you can access a command-line Python prompt. And, of course, typically some form of USB-to-serial connection to the 8266.

## Installation

Installation consists of transporting the three Python files in this project to the device, and then at the Python prompt;

    >>> import webserv

You should see a "server at IP 192.168.4.1" message printed to the console. 

## Connecting

Pick up your cellphone, go to Settings (on Android phones) and look at the available WiFi access points. One of them should be **ESP-AP**, if you see this you are golden. Connect to it, you will initially be asked for a password. It is **micropythoN** (lower case with a capital N). On Android you may very well see a popup alerting that this access point has no internet connection, and you will need to check OK to remain connected. Which you will obviously do.

## The web app

Assuming you were able to connect, you can now bring up a browser on your phone - Chrome or whatever - and for the URL you will **enter the IP address 192.168.4.1**. This should bring up the initial web page. 