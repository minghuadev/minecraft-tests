

wiring: 

    rfm95 pin    wire to    feather m0 express pin
          SCK    yellow    SCK
          MISO   green     MI
          MOSI   orange    MO
          CS     purple    5
          RST    brown     6
          GND    black     GND
          VIN    red       3V


download adafruit-circuitpython-feather_m0_express-en_US-8.2.0.uf2
install to feather m0 express:

    double-click the reset button on feather m0 express
    drop the file to its flash drive showing up on a windows pc

  or feather rp2040 adafruit-circuitpython-adafruit_feather_rp2040-en_US-8.2.2.uf2

    hold bootsel button, click reset button, release bootsel after RPI-RP2 drive appears
    drop the file to the flash drive


download adafruit-circuitpython-bundle-8.x-mpy-20230711.zip
extract and install: 

  copy the two items to the board, in the root directory or to the lib/ directory: 

    the "adafruit_bus_device/" directory, 
    the "adafruit_rfm9x.mpy" file.

  assuming the board runs circuitpython 8.2.0, the board is feather m0 express samd21g18

  copy in the neopixel.mpy

 
