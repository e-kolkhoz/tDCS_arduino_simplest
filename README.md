# tDCS_arduino_simplest
to make this tDCS you need only arduino, resistor, capasitor and crocodile connectors
![Assembled](/imgs/wtf.jpg?raw=true "Assembled")

# Schematic
![Schematic](/imgs/connections.jpg?raw=true "Schematic")
1) Arduino (I have the chineese clone of Nano) 
   - D9 pin as PWM output
   - A0 pin as analog input (for current feedback)
   - GND pin just for GND.
2) R - resistor for current measurement (I have 470 Ohm, I think 300-1000 Ohm would be ok, you need to write correct value to arduino code)
3) C - capasitor (I have electrolytic one, with 220 uF, electrolytic must be connected with "-" pin to ground).  Capasitor smoothes PWM pulsations.
4) Sponge electrodes (use saline water to wet it) attached to your head.

# How it works
Arduino is trying to set target value of current (up to 1 mA) passed through your brain by changing output voltage. You can set target_mA value by serial CLI.

# If I want to try this
0) You must read what is tDCS first. Yes, it's not approved by FDA and can be harmful. 
1) Assemble schematic.
2) Download firmware and set params in //HARDWARE PARAMS section
3) Upload firmware to your arduino. Open Tools > Serial Plotter and look to fancy lines. 
   - First (blue?) - voltage on PWM (0-5 Volts)
   - Second (red?) - current passed through your brain (mA)
   - Third (green?) - same as the Second one just smoothed (mA)
   - Fourth (orange?) - debounced status (-1 - electrodes are not connected, 0 - trying to set target current, 1 - current has target value)

# Tweakings
![Serial Plotter](/imgs/pulsations.png?raw=true "Serial Plotter")
Here you can see that output voltage is small, and pulsations of current are significant. You can try to add some resistors (100 - 700 Ohms or variable resistor/potentiometer) in series with cathode or anode to make resistance of whole circuit bigger and have more stable parameters.
![Additional resistance](/imgs/additionalRa.jpg?raw=true "Additional resistance")
With this resistors output voltage with same target_ma would be bigger, and pulsations are smaller.
![With additional 500 Ohms](/imgs/Screenshot%20from%202017-06-26%2017:50:52.png?raw=true "With additional 500 Ohms")

# UI
For comfortable and safe using it needs UI (python pyside, or something like this).
It has Serial CLI 115200 (you can check it out with putty, or Arduino IDE > Tools > Serial Monitor (some ugly artifacts when trying to clear screen and needs to set "Carriage return"))

![CLI](/imgs/cli_menu.png?raw=true "CLI")


