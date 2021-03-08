A Python script to help me control my GMMK (Glorious Modular Mechanical Keyboard https://www.pcgamingrace.com/search?q=gmmk) outside of the official software.

This is very unfinished.
If you're looking for better control of the GMMK (or lots of other RGB hardware) take a look at OpenRGB. The GMMK shows up with a different name, but it's there. https://github.com/CalcProgrammer1/OpenRGB

# Development notes
Verify the value here with lsusb, a line such as `Bus 001 Device 013: ID 0c45:652f Microdia` should be present

Set udev to permit USB access, add a udev rule for like the following:
```
# /etc/udev/rules.d/99-usb.rules
SUBSYSTEM=="usb", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="652f" MODE="0666"
```
and then reboot or reload the configuration with udevadm.
