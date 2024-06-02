import serial
import time
import pandas as pd

# Define the serial port and baud rate
serial_port = "COM4"  # Change this to match your serial port
baud_rate = 9600

# Function to read sensor values and calculate the sum
def read_and_sum(num_readings):
    total = 0
    readings = []
    for _ in range(num_readings):
        # Read the line from the serial port
        line = ser.readline().decode().strip()

        # Extract the numeric value from the line
        sensor_value = line.split(":")[-1].strip()

        try:
            # Convert the sensor value to an integer and add it to the list of readings
            reading = int(sensor_value)
            readings.append(reading)

            # Add the reading to the total
            total += reading

        except ValueError:
            print("Invalid sensor value:", sensor_value)

        # Wait for a short time before reading again
        time.sleep(1)

    # Map each reading to each month of the year
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    readings_by_month = {month: reading for month, reading in zip(months, readings)}

    # Print the readings mapped to each month
    print("\n2024 each month:")
    for month, reading in readings_by_month.items():
        print(f"{month}: {reading}")

    return readings, total

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)

# Wait for the serial connection to be established
time.sleep(2)

# Prompt the user to enter the Year
industry_name = input("Enter the Industry Name: ")
year = input("Enter the previous Year: ")




new_year = int(input("Enter the new Year for the new record: "))

print("Fetching live Sensor values from",industry_name,"for New Industry to Ministry of Power & Ministry of Environment,\nIoT Sensors for Monitoring Emissions and Credit Accumulation.")
print("Loading.")
time.sleep(3)
print("Loading..")
time.sleep(3)
print("Loading...")
time.sleep(3)
print("Loading....")
time.sleep(3)
print("Loading......")
time.sleep(3)
print("Loading........")
time.sleep(3)
print("Loading........")

co2 = pd.read_csv('carbon_credits_data.csv')

# Fetch the record based on the provided Industry Name and Year
record = co2[(co2['Industry Name'] == industry_name) & (co2['Year'] == int(year))]

if len(record) == 0:
    print("No record found for the provided Industry Name and Year.")
else:
    copy_record = record.copy()

    # Take 30 readings from the CO2 sensor and calculate the sum
    num_readings = 12
    readings, total = read_and_sum(num_readings)

    # Update the Production Output field with the calculated total value
    record_index = record.index[0]
    co2.at[record_index, 'Production Output'] += total

    # Create a new record with updated year and production output
    new_record = record.copy()
    new_record.at[record_index, 'Year'] = new_year
    new_record.at[record_index, 'Production Output'] = total

    # Append the new record to the DataFrame
    co2 = pd.concat([co2, new_record], ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    co2.to_csv('carbon_credits_data.csv', index=False)

    print("Overall", new_year, "Carbon Credits Data of",industry_name,"of all month is", total)

    print("New record appended successfully.")

# Close the serial port
ser.close()
