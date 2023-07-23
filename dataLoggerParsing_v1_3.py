# 2023-04-29 Taejune Park -  v1.3
# add support for .txt

# 2023-04-28 Taejune Park -  v1.2
# add support for .s19

# 2023-04-07 Taejune Park - v1.1
# Edited print data format

# 2023-04-06 Taejune Park - v1.0
# Edited for you to get data esaility by enterting whole file path as an input.
# If source data dosen't have correct format to parse, it will print an error

# 2022-06-16 Taejune Park - v0.1
# This python script will provide you with intutive visual data from Datalogger.
# You need to put this script into the folder that has img.asc data file.
# The number of sessions is three at the moment.
# Each session has 32kb data and total hence is 96kb.

from pprint import pprint
import bincopy

# Input to parse
filename = input("Input the full path of source file to parse\n")

# Identifier (configured in Pearl GN7 as of 16th June 2022)
identifier = {
    "00": "DATALOG_ID_POWER_ACC_ST",       # On status change, log ACC status
    "01": "DATALOG_ID_POWER_IGN_ST",       # On status change, log IGN status
    # On CAN error pin change, log CAN bus off status
    "02": "DATALOG_ID_CAN_BUS_OFF",
    # On CAN error, log Network Management status
    "03": "DATALOG_ID_CAN_NET_MGMT_ST",
    # At each boot or Discovery fail, log A2B Discovery info
    "04": "DATALOG_ID_A2B_DISCV_INF",
    # Master a2b tries post discover of ADP node soon after fault or HU re-discovery
    "05": "DATALOG_ID_A2B_ADP_INF",
    "06": "DATALOG_ID_A2B_DIAG_INFO",      # A2B diag info, bit field for err status
    # On error INT or error count max, log I2C error status + Add
    "07": "DATALOG_ID_I2C_ERR",
    # On error INT or error count max, log SPI error status + Add
    "08": "DATALOG_ID_SPI_ERR",
    # On low, high, normal change, log AD voltage status
    "09": "DATALOG_ID_ADC_VOLT_ST",
    # On exceeding Temp threshold for Audio foldback, log temp
    "0A": "DATALOG_ID_TEMP_SENSOR_ST",
    "0B": "DATALOG_ID_TEMP_ERR_ST",        # when temp err status changes, log temp
    # When DTC occurs or clears, log all DTC list
    "0C": "DATALOG_ID_DTC_OCCUR",
    "0D": "DATALOG_ID_POWER_IC_ST",        # On On/Off status change, log last state
    # Last state values of Instruction bytes Power IC
    "0E": "DATALOG_ID_POWER_IC_IB",
    "0F": "DATALOG_ID_POWER_IC_DB",        # Last state values of Data bytes Power IC
    "10": "DATALOG_ID_POWER_IC_MUTE_PIN",  # Last state value of Power ICs Mute pin
    "11": "DATALOG_ID_POWER_IC_STATE_CHG",  # Power IC state change
    "12": "DATALOG_ID_OTA",                # track ota status
    # On end of session, log SW version Boot+App+FFDB+RNDB+DSP+Chimes
    "13": "DATALOG_ID_AMP_SW_VER",
    "14": "DATALOG_ID_IFC",                # On end of session, log IFCs
    "15": "DATALOG_ID_CLOCK_TIME",         # On end of session, log time
    "16": "DATALOG_ID_INTERNAL_DATA",      # Log various internal Bose data as needed
}

# Import log file and save into list
img = []

if filename.endswith(".s19"):
    f = bincopy.BinFile(filename)
    img = f.as_ti_txt()
    img = img.split()[1:-1]

elif filename.endswith(".asc") or filename.endswith(".txt"):
    with open(filename, "r") as f:
        for line in f:
            line = line[:-1].replace(" ", "")
            line = [line[i:i+2] for i in range(0, len(line), 2)]
            img.extend(line)

else:
    print("Error: unsupported extension")
    exit()

# Divide sections (each one has 32kb and total is 96kb)
session1 = img[0:32768]
session2 = img[32768:65536]
session3 = img[65536:98304]

# Get parsing data


def dataLoggerParsing(session):
    # get header(first 16 bytes)
    CRC = " ".join(session[:4])
    Ver = session[4]
    NSO = " ".join(session[6:8])
    NSO_idx = int("0x" + NSO.replace(" ", ""), 16)

    # trim data(from after header to before NSO)
    trimmedData = session[32:NSO_idx]  # eliminate byte 16~31 filled with 00
    # trimmedData = session[32:32768] # eliminate byte 16~31 filled with 00

    # parsing
    header = [{"CRC": CRC, "VER": Ver, "NSO": NSO}]
    try:
        while trimmedData and trimmedData[0] != '00':
            data_length = int("0x"+trimmedData[0], 16)
            time_stamp = int("0x"+"".join(trimmedData[1:5]), 16)
            id = str(trimmedData[5])
            data = trimmedData[6:data_length]
            data_dic = {
                "id": id + ": "+identifier[id],
                "time_stamp": str(time_stamp) + "ms",
                "data": " ".join(data).strip(),
                "data_length": str(data_length)+"bytes",
            }
            header.append(data_dic)

            # take next block by removing fill-in 'AA'
            if data_length % 4 == 0:
                trimmedData = trimmedData[data_length:]
            else:
                trimmedData = trimmedData[data_length + (4-data_length % 4):]
    except:
        print(f"Error: session {i} data is not good to parse")

    pprint(header)


# Print data
sessions = [session1, session2, session3]
for i, session in enumerate(sessions, 1):
    try:
        print(
            f"==========================Session {i} Start============================")
        dataLoggerParsing(session)
    except:
        print(f"Error: session {i} data is not good to parse")
    finally:
        print(
            f"==========================Session {i} End==============================\n")
