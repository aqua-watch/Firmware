#!/bin/bash
rm -r /home/$USER/Arduino/libraries/sensor_readings
cp -r sensor_readings/ /home/$USER/Arduino/libraries/
#zip -r includes/sensor_readings.zip sensor_readings/