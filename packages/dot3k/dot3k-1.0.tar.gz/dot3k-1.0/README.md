dot3k
=====

Requirements
------------

You should install python-smbus first via apt:

    sudo apt-get install python-smbus

And pip, if you don't have it:

    sudo apt-get install python-pip

Then install st7036 and sn3218 using pip:

    sudo pip install st7036 sn3218

Usage
=====

LCD
---

    import dot3k.lcd as lcd
    lcd.write('Hello World!')


Backlight
---------

    import dot3k.backlight as backlight
    backlight.sweep(0.5)
    backlight.update()

Joystick
--------

    import dot3k.joystick as joystick
    @joystick.on(joystick.UP)
    def handle_joystick_up(pin):
        print("Joystick up!")
