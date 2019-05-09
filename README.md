# Sensors

# Arduino
<h4> Dependencies </h4>
Only have one so far <a href="http://www.pjrc.com/teensy/arduino_libraries/OneWire.zip"> OneWire </a>
And how to install dependencies on libraries on Arduino IDE :https://www.arduino.cc/en/Guide/Libraries#toc4
<h4> PH docs: </h4>
https://www.dfrobot.com/wiki/index.php/Analog_pH_Meter_Pro_SKU:SEN0169

<h4> Conductivity docs: </h4>
https://www.dfrobot.com/wiki/index.php/Analog_EC_Meter_SKU:DFR0300

<h4> Turpidity docs: </h4>
https://www.dfrobot.com/wiki/index.php/Turbidity_sensor_SKU:_SEN0189

<h4> TDS docs: </h4>
https://www.dfrobot.com/wiki/index.php/Gravity:_Analog_TDS_Sensor_/_Meter_For_Arduino_SKU:_SEN0244

<h4> ORP docs: </h4>
https://www.dfrobot.com/wiki/index.php/Analog_ORP_Meter(SKU:SEN0165)

# Quickstart Guide:
<h4> AquaWatch device </h4>
TODO: list out what each of the arduino projects does and their input/output formats/baudrate configuration, etc

<h4> Table </h4>
The `listening.py` script continuously runs experiments using the table, and writes the sample outputs to the model specified as the MODEL_PATH in the code, with the description specified in the MODEL_DESCRIPTION variable.

To run the experiment logic without actually sampling (i.e. just moving the sensors back and forth between the sample and the cleaning solution), run `listening.py` with the `--no_dween` flag. The script should be started with the sensors fully lowered into the sample, as it will immediately begin sampling when run.

<h4> Web interface </h4>
The web interface requires `virtualenv` to be installed. Python dependencies can be found in requirements.txt.

To run the code:
~~~
source dev.sh # Sets up virtual env, installs requirements, activates virtual environment.
./web_interface/app.py
~~~

The web interface will run on port 5000.


