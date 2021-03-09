A Python script to help me control my GMMK (Glorious Modular Mechanical Keyboard https://www.pcgamingrace.com/search?q=gmmk) outside of the official software.

This is very unfinished.
If you're looking for better control of the GMMK (or lots of other RGB hardware) take a look at OpenRGB. The GMMK shows up with a different name, but it's there. https://github.com/CalcProgrammer1/OpenRGB


# Documentation


## Development
Verify the value here with lsusb, a line such as `Bus 001 Device 013: ID 0c45:652f Microdia` should be present

Set udev to permit USB access, add a udev rule for like the following:
```
# /etc/udev/rules.d/99-usb.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="652f" MODE="0666"
```
and then reboot or reload the configuration with udevadm.

This corresponds to the information given by OpenRGB as well, see https://github.com/CalcProgrammer1/OpenRGB/blob/9767f97719aabde68c4386661589d9b1e490914a/60-openrgb.rules and search for 652f.


## Configuration per key

As mentioned, OpenRGB is an excellent source of information as well as more complete.
see https://github.com/CalcProgrammer1/OpenRGB/blob/843dacb43e6db7efc731082681358d64c039c6f4/Controllers/RedragonController/RedragonK556Controller.h for GMMK compatible details.

## Reverse engineering notes
moved from code:
```
These commands are sent along with the actual useful command from the
official software for every command. These seem to have no visible effect
on the keyboard, so they're unused until something breaks.
The second command would be the command with useful data.
FIRST_COMMAND = b'\x04\x01\x00\x01\x00\x00\x00\x00\x00' + ZEROES
THIRD_COMMAND = b'\x04\x0b\x00\x06\x01\x04\x00\x00\x00' + ZEROES
FOURTH_COMMAND = b'\x04\x02\x00\x02\x00\x00\x00\x00\x00' + ZEROES
```
"FIRST" is probably equal to "Keyboard Begin" from OpenRGB code base and 
"FOURTH" is "Keyboard End", looks as if you can send a buffer of commands before
executing. See https://github.com/CalcProgrammer1/OpenRGB/blob/dba814215d88d43b8d425b2a1c345e9b2a46a8d6/Controllers/RedragonController/RedragonK556Controller.cpp#L118
