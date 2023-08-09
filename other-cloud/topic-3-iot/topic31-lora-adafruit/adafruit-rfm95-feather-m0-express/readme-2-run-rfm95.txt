

on a stationing unit, 

  copy code-2-snd-rcv-txpwr.txt into code.txt
  it runs by itself


on a mobile unit, 

  copy code-3-6-rcv-rpy-more-mem.txt into code.txt
  it runs by itself. when it receives, it replies and blinks neopixel

  after a while its pritned free memory are : 
        1696 and 2032 in two lines.
        the two numbers may fluctuate a bit, the 1696 may change to 1680 or 1728, 
        the 2032 may become 2016.

  hit control-C to break, then control-D to reload, its initial free mem is 2928. then 
  showing 1664, then pairs: 
        1216, 1904, 
        1568, 1904, 
        1600, 1904, 
        1568, 1904, 
        1552, 1888, 
        1392, 1904, 
        ... 

  copy the code.txt into its flash drive, it reloads, with first two free memory showing 
  as 3088, and then 1824. then in pairs: 
        1360, 2016, 
        1488, 2016, 
        1728, 2032
        1504, 2016, 
        1696, 2032, 
        ...


