# import necessary packages
import time
import pytz
from datetime import datetime
import pymodbus
from pymodbus.client import ModbusSerialClient

#    choices:
def write():
    print(" ")
    print("### Modbus writing operation ###")
    print(" ")
    slv = int(input("Enter the slave id: "))
    baud = int(input("Enter the baudrate: "))
    com = str(input("Enter the com port: "))
    add = int(input("Enter the register address: "))
    val = int(input("Enter the value to write: "))

    # establish connection
    client = ModbusSerialClient(port=com, baudrate=baud, timeout=1, stopbits=1, bytesize=8, parity='N')

    if client.connect():
        print(" ")
        print("Device is connected!")
        write = client.write_registers(add, val, slv)
        if write.isError():
            print("Error")
        else:
            print(f"### Value {val} is written to register {add} ###")
    else:
        print("Failed to connect to device!")
    
    client.close()
    input()

def read():
    print(" ")
    print("### Modbus reading operation ###")
    print(" ")
    slv = int(input("Enter the slave id: "))
    baud = int(input("Enter the baudrate: "))
    com = str(input("Enter the com port: "))
    add = int(input("Enter the register address: "))
    
    client = ModbusSerialClient(port=com, baudrate=baud, timeout=1, stopbits=1, bytesize=8, parity='N')

    if client.connect():
        print(" ")
        print("Device is connected!")
        count = int(input("Enter count: "))
        read = client.read_holding_registers(add, count, slv)
        if read.isError():
            print("Error while reading")
        else:
            print(read.registers)
    else:
        print("Failed to connect to device!")
    
    client.close()
    input()

def monitor():
    print(" ")
    print("### Modbus reading monitor ###")
    print(" ")
    slv = int(input("Enter the slave id: "))
    baud = int(input("Enter the baudrate: "))
    com = str(input("Enter the com port: "))
    add = int(input("Enter the register address: "))

    # TIMEZONE OF LUDHIANA
    timezone = pytz.timezone("Asia/Kolkata")

    client = ModbusSerialClient(port=com, baudrate=baud, timeout=1, stopbits=1, bytesize=8, parity='N')

    if client.connect():
        print(" ")
        print("Device is connected!")
        count = int(input("Enter count: "))
        try:
            while True:
                # Read registers
                result = client.read_holding_registers(add, 10, slv)

                if result.isError():
                    print("Failed to read the values.")
                else:
                    # Get the time in GMT+5:30
                    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Display the value with the current date and time
                    print(f"{current_time} - Values read from address {add}: {result.registers}")
                
                # DELAY BEFORE LOOPING AGIAN
                time.sleep(1)

        except KeyboardInterrupt:
            print("Reading operation stopped by user.")
            client.close()
    else:
        print("Failed to connect to the server.")

def menu():
    print("### Modbus Menu ###")
    print("1. Write")
    print("2. Read")
    print("3. Monitor")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        write()
    elif choice == 2:
        read()
    elif choice == 3:
        monitor()
    else:
        print("Exiting...")
        
menu()
input()