# DAC_Reference
This is a DAC Voltage Reference project for controling via SCPI standard library

## Features
* Very quick control of output voltage, clock speed can achieve up to 3.5MHz
* Voltages in range [-5V,5V] with 2^19 stepping
* Remote control via Ethernet using SCPI standard commands
* Autonomic device based on BeagleBone Black board, external connection only for configuration

## Connection and installation

It is possible to remotely connect to Linux kernel of Beaglebone and therfore control it from simple built in class included in spi_set.py file.

The device also runs server on IP 192.168.0.20 on 5555 PORT. You can control it via SPCI commands. The server starts by using methods from SCPI_server.py that take Message class instance as a parameter to parse and execute client requests. 
