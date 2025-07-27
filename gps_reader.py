import serial
import pynmea2
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='gps_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def setup_serial(port="/dev/ttyAMA0", baudrate=9600, timeout=1):
    """Initialize serial connection with error handling."""
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        logging.info("Serial port opened successfully")
        return ser
    except serial.SerialException as e:
        logging.error(f"Failed to open serial port: {e}")
        print(f"Error: Could not open serial port {port}. Check connections and permissions.")
        return None

def parse_gps_data(data):
    """Parse NMEA data and extract relevant fields."""
    try:
        # Decode bytes to string, handling potential errors
        data = data.decode('utf-8', errors='ignore').strip()
        if data.startswith('$GPGGA'):
            msg = pynmea2.parse(data)
            return {
                'timestamp': msg.timestamp,
                'latitude': msg.latitude,
                'longitude': msg.longitude,
                'altitude': msg.altitude,
                'satellites': msg.num_satellites,
                'fix_quality': msg.gps_qual
            }
        return None
    except pynmea2.ParseError:
        logging.warning(f"Failed to parse NMEA sentence: {data}")
        return None
    except UnicodeDecodeError:
        logging.warning("Failed to decode data")
        return None

def main():
    # Initialize serial port
    ser = setup_serial()
    if not ser:
        return

    print("Starting GPS data collection... Press Ctrl+C to stop.")
    try:
        while True:
            try:
                # Read a line from the serial port
                data = ser.readline()
                if data:
                    gps_info = parse_gps_data(data)
                    if gps_info and gps_info['fix_quality'] > 0:  # Ensure valid GPS fix
                        log_message = (
                            f"Time: {gps_info['timestamp']}, "
                            f"Lat: {gps_info['latitude']:.6f}, "
                            f"Lon: {gps_info['longitude']:.6f}, "
                            f"Alt: {gps_info['altitude']} m, "
                            f"Satellites: {gps_info['satellites']}"
                        )
                        print(log_message)
                        logging.info(log_message)
                    else:
                        print("Waiting for GPS fix...")
                else:
                    print("No data received. Checking connection...")
            except serial.SerialException as e:
                logging.error(f"Serial error: {e}")
                print("Serial error occurred. Reconnecting...")
                ser.close()
                ser = setup_serial()
                if not ser:
                    break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                print(f"Error: {e}")
            time.sleep(1)  # Avoid overwhelming the CPU
    except KeyboardInterrupt:
        print("\nStopping GPS data collection...")
    finally:
        if ser and ser.is_open:
            ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
