# RaspberryPi-GPS-Interfacing

# Raspberry Pi GPS Module Interfacing

This project demonstrates how to interface a GPS module (e.g., NEO-6M) with a Raspberry Pi using Python. The code reads NMEA sentences from the GPS module via UART, parses `$GPGGA` sentences, and extracts latitude, longitude, altitude, and satellite information. Data is logged to a file (`gps_data.log`) for further analysis.

## Requirements
- Raspberry Pi (any model with GPIO pins)
- GPS module (e.g., NEO-6M)
- Python 3
- Libraries: `pyserial`, `pynmea2` (install with `pip install pyserial pynmea2`)
- UART enabled on Raspberry Pi

## Setup
1. Connect the GPS module:
   - VCC → 3.3V or 5V (check module specs)
   - GND → GND
   - TX → GPIO15 (RXD, Pin 10)
   - RX → GPIO14 (TXD, Pin 8)
2. Enable UART:
   - Edit `/boot/config.txt` to include:
  
 ## Code Explanation
Imports:
serial: For serial communication with the GPS module.
pynmea2: To parse NMEA sentences.
time: For adding delays.
logging: To log GPS data to a file (gps_data.log).
datetime: To handle timestamps.
Functions:
setup_serial: Initializes the serial port with error handling.
parse_gps_data: Parses $GPGGA sentences and extracts timestamp, latitude, longitude, altitude, satellites, and fix quality.
main: Reads data in a loop, processes valid GPS fixes, logs them, and handles errors.
Features:
Decodes byte data to strings, handling encoding errors.
Checks for valid GPS fixes (fix_quality > 0).
Logs data to gps_data.log with timestamps.
Reconnects on serial errors and cleans up on exit.
Output: Prints GPS data (e.g., Time: 12:34:56, Lat: 12.345678, Lon: 78.901234, Alt: 100.0 m, Satellites: 8) and logs it to a file.
