from django.shortcuts import render
import csv
import json
import time
import pickle
from hashlib import sha256
from datetime import datetime
import serial
import time
import pandas as pd
# Create your views here.

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash()

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def save_object(self, obj, filename):
        with open(filename, 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


class CarbonCreditSystem:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def read_data_from_csv(self, filename):
        industries = []
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                industries.append(row)
        return industries

    def write_data_to_csv(self, data, filename):
        fieldnames = ['Year', 'Industry Name', 'Sector', 'Emissions', 'Production Output',
                      'Emission Reduction Measures', 'Future Expansion Plans',
                      'Technological Infrastructure', 'Carbon Intensity', 'Compliance History',
                      'Emission Limit']  # Adjusted field names to match CSV
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def add_blockchain_data(self, data):
        for industry_data in data:
            block = Block(index=len(self.blockchain.chain) + 1,
                          transactions=[industry_data],
                          timestamp=time.time(),
                          previous_hash=self.blockchain.last_block.hash)
            proof = self.blockchain.proof_of_work(block)
            self.blockchain.add_block(block, proof)

    def add_new_industry(self, industry):
        data = {
            "name": industry.name,
            "sector": industry.sector,
            "historical_emissions": industry.historical_emissions,
            "production_output": industry.production_output,
            "emission_reduction_measures": industry.emission_reduction_measures,
            "future_expansion_plans": industry.future_expansion_plans,
            "technological_infrastructure": industry.technological_infrastructure,
            "carbon_intensity": industry.carbon_intensity,
            "compliance_history": industry.compliance_history,
            "Limit": industry.Limit
        }
        block = Block(index=len(self.blockchain.chain) + 1,
                      transactions=[data],
                      timestamp=time.time(),
                      previous_hash=self.blockchain.last_block.hash)
        proof = self.blockchain.proof_of_work(block)
        self.blockchain.add_block(block, proof)

    # def view_blockchain(self):
    #     for block in self.blockchain.chain:
    #         print(f"Block Index: {block.index}")
    #         print(f"Timestamp: {datetime.fromtimestamp(block.timestamp)}")
    #         print(f"Previous Hash: {block.previous_hash}")
    #         print(f"Hash: {block.hash}")
    #         print("Transactions:")
    #         for transaction in block.transactions:
    #             print(json.dumps(transaction, indent=4))
    #         print()

    def view_entry(self, index):
        if 0 < index < len(self.blockchain.chain):
            block = self.blockchain.chain[index]
            print(f"Block Index: {block.index}")
            print(f"Timestamp: {datetime.fromtimestamp(block.timestamp)}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print("Transactions:")
            for transaction in block.transactions:
                print(json.dumps(transaction, indent=4))
            print()
        else:
            print("Invalid block index.")

    def check_violations(self):
        violations = []
        for block in self.blockchain.chain:
            for transaction in block.transactions:
                production_output = float(transaction.get('Production Output', 0))
                emission_limit = float(transaction.get('Emission Limit', 0))
                if production_output > emission_limit:
                    violation_info = {
                        "Block Index": block.index,
                        "Timestamp": datetime.fromtimestamp(block.timestamp).isoformat(),  # Convert to string
                        "Block Hash": block.hash,
                        "Transaction": transaction
                    }
                    violations.append(violation_info)
        return violations


class Industry:
    def __init__(self, year, name, sector, historical_emissions, production_output, emission_reduction_measures,
                 future_expansion_plans, technological_infrastructure, carbon_intensity, compliance_history, Limit):
        self.year = year  # Add year argument
        self.name = name
        self.sector = sector
        self.historical_emissions = historical_emissions
        self.production_output = production_output
        self.emission_reduction_measures = emission_reduction_measures
        self.future_expansion_plans = future_expansion_plans
        self.technological_infrastructure = technological_infrastructure
        self.carbon_intensity = carbon_intensity
        self.compliance_history = compliance_history
        self.Limit = Limit




def index(request):
    return render(request,'myapp/index.html')

def userhomepage(request):
    return render(request,'myapp/userhomepage.html')

def login(request):
    if request.method=="POST":
        username = request.POST['uname']
        password = request.POST['pwd']
        print(username,password)
        if username == 'admin' and password == 'admin':
            return render(request, 'myapp/adminhomepage.html')
        elif username == 'abc' and password == 'abc':
            return render(request, 'myapp/userhomepage.html')
        else:
            return render(request,'myapp/login.html')
    return render(request,'myapp/login.html')

def adminhomepage(request):

    return render(request,'myapp/adminhomepage.html')

def viewBlockchain(request):
    print("Blockchain-enabled Carbon Credits\nIoT Sensors for Monitoring Emissions and Credit Accumulation.")

    print("Welcome to Ministry of Power & Ministry of Environment, Forests & Climate Change Manager Portal")

    blockchain = Blockchain()
    carbon_credit_system = CarbonCreditSystem(blockchain)

    data = carbon_credit_system.read_data_from_csv('carbon_credits_data.csv')
    carbon_credit_system.add_blockchain_data(data)
    blockchain.mine()
    blockchain.save_object(blockchain, 'blockchain_data.pkl')
    # carbon_credit_system.view_blockchain()
    blockchain_data = []
    for block in blockchain.chain:
        block_data = {
            'index': block.index,
            'timestamp': datetime.fromtimestamp(block.timestamp),
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'transactions': block.transactions
        }
        blockchain_data.append(block_data)

    return render(request, 'myapp/viewBlockchain.html', {'blockchain_data': blockchain_data})

def indivbc(request):
    if request.method=='POST':
        bcindex=request.POST.get('blockindex')
        print(bcindex)
        index=int(bcindex)-1
        blockchain = Blockchain()
        carbon_credit_system = CarbonCreditSystem(blockchain)

        data = carbon_credit_system.read_data_from_csv('carbon_credits_data.csv')
        carbon_credit_system.add_blockchain_data(data)
        blockchain.mine()
        blockchain.save_object(blockchain, 'blockchain_data.pkl')
        if 0 < index < len(blockchain.chain):
            block = blockchain.chain[index]
            block_data = {
                'index': block.index,
                'timestamp': datetime.fromtimestamp(block.timestamp),
                'previous_hash': block.previous_hash,
                'hash': block.hash,
                'transactions': block.transactions
            }
            return render(request, 'myapp/indivbc.html', {'block_data': block_data})
        else:
            error_message = "Invalid block index."
            # return render(request, 'error_template.html', {'error_message': error_message})

    return render(request,'myapp/indivbc.html')

def checkviolate(request):
    violations = []
    blockchain = Blockchain()
    carbon_credit_system = CarbonCreditSystem(blockchain)

    data = carbon_credit_system.read_data_from_csv('carbon_credits_data.csv')
    carbon_credit_system.add_blockchain_data(data)
    blockchain.mine()
    blockchain.save_object(blockchain, 'blockchain_data.pkl')

    for block in blockchain.chain:
        for transaction in block.transactions:
            production_output = float(transaction.get('Production Output', 0))
            emission_limit = float(transaction.get('Emission Limit', 0))
            if production_output > emission_limit:
                violations.append({
                    "block_index": block.index,
                    "timestamp": datetime.fromtimestamp(block.timestamp).isoformat(),
                    "transaction": transaction
                })

    context = {
        'violations': violations,
    }

    return render(request, 'myapp/checkviolate.html', context)


# ######################User Details###############################

def addcompany(request):
    if request.method=='POST':
        blockchain = Blockchain()
        carbon_credit_system = CarbonCreditSystem(blockchain)

        data = carbon_credit_system.read_data_from_csv('carbon_credits_data.csv')
        carbon_credit_system.add_blockchain_data(data)
        blockchain.mine()
        blockchain.save_object(blockchain, 'blockchain_data.pkl')

        year = request.POST.get('txtyear') # Add year input
        name = request.POST.get('txtcname')
        sector = request.POST.get('txtsector')
        historical_emissions = float(request.POST.get('txthemission') )
        production_output = float(request.POST.get('txtpoutput') )
        emission_reduction_measures = request.POST.get('txtrmeasure')
        future_expansion_plans = request.POST.get('txteplan')
        technological_infrastructure = request.POST.get('txtinfra')
        carbon_intensity = request.POST.get('txtintensity')
        compliance_history = request.POST.get('txtchistory')
        Limit = float(request.POST.get('txtlimit') )
        new_industry = Industry(year, name, sector, historical_emissions, production_output,
                                emission_reduction_measures, future_expansion_plans,
                                technological_infrastructure, carbon_intensity,
                                compliance_history, Limit)

        # carbon_credit_system.add_new_industry(new_industry)
        data = {
            "name": new_industry.name,
            "sector": new_industry.sector,
            "historical_emissions": new_industry.historical_emissions,
            "production_output": new_industry.production_output,
            "emission_reduction_measures": new_industry.emission_reduction_measures,
            "future_expansion_plans": new_industry.future_expansion_plans,
            "technological_infrastructure": new_industry.technological_infrastructure,
            "carbon_intensity": new_industry.carbon_intensity,
            "compliance_history": new_industry.compliance_history,
            "Limit": new_industry.Limit
        }
        block = Block(index=len(blockchain.chain) + 1,
                      transactions=[data],
                      timestamp=time.time(),
                      previous_hash=blockchain.last_block.hash)
        proof = blockchain.proof_of_work(block)
        blockchain.add_block(block, proof)
        print('hi')
        # Update CSV
        new_data = carbon_credit_system.read_data_from_csv('carbon_credits_data.csv')
        new_data.append({
            "Year": new_industry.year,  # Add year
            "Industry Name": new_industry.name,
            "Sector": new_industry.sector,
            "Emissions": new_industry.historical_emissions,
            "Production Output": new_industry.production_output,
            "Emission Reduction Measures": new_industry.emission_reduction_measures,
            "Future Expansion Plans": new_industry.future_expansion_plans,
            "Technological Infrastructure": new_industry.technological_infrastructure,
            "Carbon Intensity": new_industry.carbon_intensity,
            "Compliance History": new_industry.compliance_history,
            "Emission Limit": new_industry.Limit
        })
        fieldnames = ['Year', 'Industry Name', 'Sector', 'Emissions', 'Production Output',
                      'Emission Reduction Measures', 'Future Expansion Plans',
                      'Technological Infrastructure', 'Carbon Intensity', 'Compliance History',
                      'Emission Limit']  # Adjusted field names to match CSV
        filename='carbon_credits_data.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_data)
        # carbon_credit_system.write_data_to_csv(new_data, 'carbon_credits_data.csv')
        print( "Register New Industry to Ministry of Power & Ministry of Environment, Forests & Climate Change Manager Portal")
        res="Register New Industry to Ministry of Power & Ministry of Environment, Forests & Climate Change Manager Portal"
        content={
            'data':res,
        }
        return render(request, 'myapp/addcompany.html',content)
    return render(request,'myapp/addcompany.html')

def read_and_sum(num_readings):
    total = 0
    readings = []
    serial_port = 'COM4'  # Change this to match your serial port
    baud_rate = 9600

    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate)
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


def sensorentry(request):
    if request.method=='POST':
        serial_port = 'COM4'  # Change this to match your serial port
        baud_rate = 9600

        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate)
        ser.close()

        # Wait for the serial connection to be established
        time.sleep(2)

        # Prompt the user to enter the Year
        industry_name = request.POST.get('txtcname')
        year = int(request.POST.get('txtpyear'))
        new_year = int(request.POST.get('txtnyear'))

        print("Fetching live Sensor values from", industry_name,
              "for New Industry to Ministry of Power & Ministry of Environment,\nIoT Sensors for Monitoring Emissions and Credit Accumulation.")
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
        data="Fetching live Sensor values from"+industry_name+"for New Industry to Ministry of Power & Ministry of Environment,\nIoT Sensors for Monitoring Emissions and Credit Accumulation."

        co2 = pd.read_csv('carbon_credits_data.csv')

        # Fetch the record based on the provided Industry Name and Year
        record = co2[(co2['Industry Name'] == industry_name) & (co2['Year'] == int(year))]

        if len(record) == 0:
            print("No record found for the provided Industry Name and Year.")
            content={
                'data1':"No record found for the provided Industry Name and Year."

            }
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

            print("Overall", new_year, "Carbon Credits Data of", industry_name, "of all month is", total)
            res="Overall"+ str(new_year)+ "Carbon Credits Data of"+ str(industry_name)+ "of all month is"+ str(total)
            time.sleep(3)
            print("New record appended successfully.")
            content = {
                'data1': data,
                'data2': 'Loading.........................',
                'data3':res,
                'data4':"New record appended successfully."
            }
        # Close the serial port

        ser.close()
        return render(request, 'myapp/sensorentry.html',content)
    return render(request,'myapp/sensorentry.html')


def manualentry(request):
    return render(request,'myapp/manualentry.html')