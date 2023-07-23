'''
2023-06-07 Taejune Park - v2.1
Added if statement to check if the first lot of power IC data is overwrritten

2023-06-06 Taejune Park - v2.0
DRAFT for 'New Data Logger Design'

2023-04-29 Taejune Park - v1.3
Added support for .txt

2023-04-28 Taejune Park - v1.2
Added support for .s19

2023-04-07 Taejune Park - v1.1
Edited print data format

2023-04-06 Taejune Park - v1.0
Edited for you to get data esaility by enterting whole file path as an input.
If source data dosen't have correct format to parse, it will print an error

2022-06-16 Taejune Park - v0.1
This python script will provide you with intutive visual data from Datalogger.
You need to put this script into the folder that has img.asc data file.
The number of sessions is three at the moment.
Each session has 32kb data and total hence is 96kb.
'''

from pprint import pprint
import bincopy

LOG_CATEGORY = {
    "DATALOG_CAT_SW_VERSION": 1,  # 16bytes
    "DATALOG_CAT_POWER_NETWORK_STATUS": 100,  # 1600bytes
    "DATALOG_CAT_A2B_COMM": 100,
    "DATALOG_CAT_OTHER_COMM": 30,  # 480bytes
    "DATALOG_CAT_ADC_TEMP": 30,
    "DATALOG_CAT_POWER_IC": 80,
    "DATALOG_CAT_DTC": 80,
    "DATALOG_CAT_OTA": 100,
    "DATALOG_CAT_IFC": 100,
    "DATALOG_CAT_CAN_RX": 750,
    "DATALOG_CAT_CAN_TX": 675,
    "DATALOG_CAT_CRC": 2,
}

LOG_DATA_ID = [
    "DATALOG_AMP_SW_VER",
    "DATALOG_POW_NETWORK",
    "DATALOG_A2B_COMM_MASTER",
    "DATALOG_A2B_COMM_INT",
    "DATALOG_A2B_COMM_RESERVED_2",
    "DATALOG_A2B_COMM_RESERVED_3",
    "DATALOG_A2B_COMM_RESERVED_4",
    "DATALOG_OTHER_COMM",
    "DATALOG_ADC_TEMP",
    "DATALOG_POWER_IC_STATE",
    "DATALOG_POWER_IC_IB",
    "DATALOG_POWER_IC_DB",
    "DATALOG_POWER_IC_4",
    "DATALOG_POWER_IC_5",
    "DATALOG_DTC_1",
    "DATALOG_DTC_2",
    "DATALOG_DTC_3",
    "DATALOG_DTC_4",
    "DATALOG_DTC_5",
    "DATALOG_DTC_6",
    "DATALOG_DTC_7",
    "DATALOG_DTC_8",
    "DATALOG_OTA_LOG_1",
    "DATALOG_OTA_LOG_2",
    "DATALOG_IFC_LOG_1",
    "DATALOG_IFC_LOG_2",
    "DATALOG_IFC_LOG_3",
    "DATALOG_IFC_LOG_4",
    "DATALOG_IFC_LOG_5",
    "DATALOG_IFC_LOG_6",
    "DATALOG_IFC_LOG_7",
    "DATALOG_IFC_LOG_8",
    "DATALOG_IFC_LOG_9",
    "DATALOG_IFC_LOG_10",
    "DATALOG_IFC_LOG_11",
    "DATALOG_IFC_LOG_12",
    "DATALOG_IFC_LOG_13",
    "DATALOG_IFC_LOG_14",
    "DATALOG_IFC_LOG_15",
    "DATALOG_IFC_LOG_16",
    "DATALOG_IFC_LOG_17",
    "DATALOG_IFC_LOG_18",
    "DATALOG_IFC_LOG_19",
    "DATALOG_IFC_LOG_20",
    "DATALOG_CAN_RX_HU_AMP_E_01",
    "DATALOG_CAN_RX_HU_AMP_E_02",
    "DATALOG_CAN_RX_HU_AMP_E_03",
    "DATALOG_CAN_RX_HU_AMP_E_04",
    "DATALOG_CAN_RX_HU_AMP_E_05",
    "DATALOG_CAN_RX_HU_AMP_E_06",
    "DATALOG_CAN_RX_HU_AMP_E_07",
    "DATALOG_CAN_RX_HU_AMP_E_08",
    "DATALOG_CAN_RX_HU_AMP_E_09",
    "DATALOG_CAN_RX_HU_AMP_E_10",
    "DATALOG_CAN_RX_HU_AMP_E_11",
    "DATALOG_CAN_RX_HU_AMP_E_12",
    "DATALOG_CAN_RX_HU_AMP_E_13",
    "DATALOG_CAN_RX_HU_AMP_PE_01",
    "DATALOG_CAN_RX_HU_AMP_P_01",
    "DATALOG_CAN_RX_HU_CAR_PE_01",
    "DATALOG_CAN_RX_HU_MON_PE_01",
    "DATALOG_CAN_RX_CLU_AMP_PE_01",
    "DATALOG_CAN_RX_ADAS_PRK_20_20_2",
    "DATALOG_CAN_RX_ADAS_UX_01_50_3",
    "DATALOG_CAN_RX_DATC_14_00",
    "DATALOG_CAN_RX_DVRS_HU_PE_00",
    "DATALOG_CAN_RX_ATS_00_00",
    "DATALOG_CAN_RX_ICU_01_00",
    "DATALOG_CAN_RX_DRV_SHVU_02_00",
    "DATALOG_CAN_RX_AST_SHVU_02_00",
    "DATALOG_CAN_RX_MKBD_HU_PE_03",
    "DATALOG_CAN_RX_FCS_01_200",
    "DATALOG_CAN_RX_BCM_01_00",
    "DATALOG_CAN_RX_NM_AMP",
    "DATALOG_CAN_RX_BCM_05_200",
    "DATALOG_CAN_RX_BCM_10_200",
    "DATALOG_CAN_RX_BCM_12_200",
    "DATALOG_CAN_RX_CDU_01_PE_200",
    "DATALOG_CAN_RX_CDU_14_200_1",
    "DATALOG_CAN_RX_DATC_14_00_1",
    "DATALOG_CAN_RX_HCU_03_10_2",
    "DATALOG_CAN_RX_ICSC_02_100_1",
    "DATALOG_CAN_RX_NM_ADP",
    "DATALOG_CAN_RX_NM_CDU",
    "DATALOG_CAN_RX_NM_CGW_CCU",
    "DATALOG_CAN_RX_NM_CLU_MM",
    "DATALOG_CAN_RX_NM_ETCS",
    "DATALOG_CAN_RX_NM_H_U_MM",
    "DATALOG_CAN_RX_NM_ICC",
    "DATALOG_CAN_RX_NM_MKBD",
    "DATALOG_CAN_RX_NM_RRC",
    "DATALOG_CAN_RX_NM_VESS",
    "DATALOG_CAN_RX_GST_ALL",
    "DATALOG_CAN_RX_GST_AMP",
    "DATALOG_CAN_RX_ICU_02_200",
    "DATALOG_CAN_RX_ICU_05_200",
    "DATALOG_CAN_RX_RESERVE_00",
    "DATALOG_CAN_RX_RESERVE_01",
    "DATALOG_CAN_RX_RESERVE_02",
    "DATALOG_CAN_RX_RESERVE_03",
    "DATALOG_CAN_RX_RESERVE_04",
    "DATALOG_CAN_RX_RESERVE_05",
    "DATALOG_CAN_RX_RESERVE_06",
    "DATALOG_CAN_RX_RESERVE_07",
    "DATALOG_CAN_RX_RESERVE_08",
    "DATALOG_CAN_RX_RESERVE_09",
    "DATALOG_CAN_RX_RESERVE_10",
    "DATALOG_CAN_RX_RESERVE_11",
    "DATALOG_CAN_RX_RESERVE_12",
    "DATALOG_CAN_RX_RESERVE_13",
    "DATALOG_CAN_RX_RESERVE_14",
    "DATALOG_CAN_RX_RESERVE_15",
    "DATALOG_CAN_RX_RESERVE_16",
    "DATALOG_CAN_RX_RESERVE_17",
    "DATALOG_CAN_RX_RESERVE_18",
    "DATALOG_CAN_RX_RESERVE_19",
    "DATALOG_CAN_RX_RESERVE_20",
    "DATALOG_CAN_RX_RESERVE_21",
    "DATALOG_CAN_RX_RESERVE_22",
    "DATALOG_CAN_RX_RESERVE_23",
    "DATALOG_CAN_RX_RESERVE_24",
    "DATALOG_CAN_RX_RESERVE_25",
    "DATALOG_CAN_RX_RESERVE_26",
    "DATALOG_CAN_RX_RESERVE_27",
    "DATALOG_CAN_RX_RESERVE_28",
    "DATALOG_CAN_RX_RESERVE_29",
    "DATALOG_CAN_RX_RESERVE_30",
    "DATALOG_CAN_RX_RESERVE_31",
    "DATALOG_CAN_RX_RESERVE_32",
    "DATALOG_CAN_RX_RESERVE_33",
    "DATALOG_CAN_RX_RESERVE_34",
    "DATALOG_CAN_RX_RESERVE_35",
    "DATALOG_CAN_RX_RESERVE_36",
    "DATALOG_CAN_RX_RESERVE_37",
    "DATALOG_CAN_RX_RESERVE_38",
    "DATALOG_CAN_RX_RESERVE_39",
    "DATALOG_CAN_RX_RESERVE_40",
    "DATALOG_CAN_RX_RESERVE_41",
    "DATALOG_CAN_RX_RESERVE_42",
    "DATALOG_CAN_RX_RESERVE_43",
    "DATALOG_CAN_RX_RESERVE_44",
    "DATALOG_CAN_RX_RESERVE_45",
    "DATALOG_CAN_RX_RESERVE_46",
    "DATALOG_CAN_RX_RESERVE_47",
    "DATALOG_CAN_RX_RESERVE_48",
    "DATALOG_CAN_RX_RESERVE_49",
    "DATALOG_CAN_RX_RESERVE_50",
    "DATALOG_CAN_RX_RESERVE_51",
    "DATALOG_CAN_RX_RESERVE_52",
    "DATALOG_CAN_RX_RESERVE_53",
    "DATALOG_CAN_RX_RESERVE_54",
    "DATALOG_CAN_RX_RESERVE_55",
    "DATALOG_CAN_RX_RESERVE_56",
    "DATALOG_CAN_RX_RESERVE_57",
    "DATALOG_CAN_RX_RESERVE_58",
    "DATALOG_CAN_RX_RESERVE_59",
    "DATALOG_CAN_RX_RESERVE_60",
    "DATALOG_CAN_RX_RESERVE_61",
    "DATALOG_CAN_RX_RESERVE_62",
    "DATALOG_CAN_RX_RESERVE_63",
    "DATALOG_CAN_RX_RESERVE_64",
    "DATALOG_CAN_RX_RESERVE_65",
    "DATALOG_CAN_RX_RESERVE_66",
    "DATALOG_CAN_RX_RESERVE_67",
    "DATALOG_CAN_RX_RESERVE_68",
    "DATALOG_CAN_RX_RESERVE_69",
    "DATALOG_CAN_RX_RESERVE_70",
    "DATALOG_CAN_RX_RESERVE_71",
    "DATALOG_CAN_RX_RESERVE_72",
    "DATALOG_CAN_RX_RESERVE_73",
    "DATALOG_CAN_RX_RESERVE_74",
    "DATALOG_CAN_RX_RESERVE_75",
    "DATALOG_CAN_RX_RESERVE_76",
    "DATALOG_CAN_RX_RESERVE_77",
    "DATALOG_CAN_RX_RESERVE_78",
    "DATALOG_CAN_RX_RESERVE_79",
    "DATALOG_CAN_RX_RESERVE_80",
    "DATALOG_CAN_RX_RESERVE_81",
    "DATALOG_CAN_RX_RESERVE_82",
    "DATALOG_CAN_RX_RESERVE_83",
    "DATALOG_CAN_TX_AMP_HU_E_01",
    "DATALOG_CAN_TX_AMP_HU_E_03",
    "DATALOG_CAN_TX_AMP_HU_E_04",
    "DATALOG_CAN_TX_AMP_HU_E_05",
    "DATALOG_CAN_TX_AMP_HU_E_06",
    "DATALOG_CAN_TX_AMP_HU_E_07",
    "DATALOG_CAN_TX_AMP_HU_E_08",
    "DATALOG_CAN_TX_AMP_HU_E_11",
    "DATALOG_CAN_TX_AMP_HU_PE_01",
    "DATALOG_CAN_TX_AMP_HU_PE_02",
    "DATALOG_CAN_TX_AMP_HU_PE_03",
    "DATALOG_CAN_TX_AMP_HU_PE_04",
    "DATALOG_CAN_TX_AMP_HU_PE_05",
    "DATALOG_CAN_TX_AMP_HU_PE_07",
    "DATALOG_CAN_TX_AMP_HU_P_01",
    "DATALOG_CAN_TX_AMP_HU_P_02",
    "DATALOG_CAN_TX_AMP_HU_P_03",
    "DATALOG_CAN_TX_RESERVE_01",
    "DATALOG_CAN_TX_RESERVE_02",
    "DATALOG_CAN_TX_RESERVE_03",
    "DATALOG_CAN_TX_RESERVE_04",
    "DATALOG_CAN_TX_RESERVE_05",
    "DATALOG_CAN_TX_RESERVE_06",
    "DATALOG_CAN_TX_RESERVE_07",
    "DATALOG_CAN_TX_RESERVE_08",
    "DATALOG_CAN_TX_RESERVE_09",
    "DATALOG_CAN_TX_RESERVE_10",
    "DATALOG_CAN_TX_RESERVE_11",
    "DATALOG_CAN_TX_RESERVE_12",
    "DATALOG_CAN_TX_RESERVE_13",
    "DATALOG_CAN_TX_RESERVE_14",
    "DATALOG_CAN_TX_RESERVE_15",
    "DATALOG_CAN_TX_RESERVE_16",
    "DATALOG_CAN_TX_RESERVE_17",
    "DATALOG_CAN_TX_RESERVE_18",
    "DATALOG_CAN_TX_RESERVE_19",
    "DATALOG_CAN_TX_RESERVE_20",
    "DATALOG_CAN_TX_RESERVE_21",
    "DATALOG_CAN_TX_RESERVE_22",
    "DATALOG_CAN_TX_RESERVE_23",
    "DATALOG_RESERVE_01",
    "DATALOG_RESERVE_02",
    "DATALOG_RESERVE_03",
    "DATALOG_RESERVE_04",
    "DATALOG_RESERVE_05",
    "DATALOG_RESERVE_06",
    "DATALOG_RESERVE_07",
    "DATALOG_RESERVE_08",
    "DATALOG_RESERVE_09",
    "DATALOG_RESERVE_10",
    "DATALOG_RESERVE_11",
    "DATALOG_RESERVE_12",
    "DATALOG_RESERVE_13",
    "DATALOG_RESERVE_14",
    "DATALOG_RESERVE_15",
    "DATALOG_RESERVE_16",
    "DATALOG_RESERVE_17",
    "DATALOG_RESERVE_18",
    "DATALOG_RESERVE_19",
    "DATALOG_RESERVE_20",
    "DATALOG_RESERVE_21",
    "DATALOG_RESERVE_22",
    "DATALOG_RESERVE_23",
    "DATALOG_RESERVE_24",
    "DATALOG_RESERVE_25",
    "DATALOG_RESERVE_26",
    "DATALOG_RESERVE_27",
    "DATALOG_RESERVE_28",
    "DATALOG_RESERVE_29",
    "DATALOG_RESERVE_30",
    "DATALOG_RESERVE_31",
    "DATALOG_RESERVE_32",
    "DATALOG_RESERVE_33",
    "DATALOG_RESERVE_34",
    "DATALOG_RESERVE_35",
    "DATALOG_RESERVE_36",
]
D_LOG_DATA_ID = {'%02X' % i: elem for i, elem in enumerate(LOG_DATA_ID)}

SIZE_OF_SESSION = 32768  # 32kb


def log_to_list(log):
    '''Supported log extension: s19, asc, txt
    This will have format of ['06', '00', '00', '0A'...]
    '''
    log_list = []

    if log.endswith(".s19"):
        f = bincopy.BinFile(log)
        log_list = f.as_ti_txt()
        log_list = log_list.split()[1:-1]
    elif log.endswith(".asc") or log.endswith(".txt"):
        with open(log, "r") as f:
            for line in f:
                line = line[:-1].replace(" ", "")
                line = [line[i:i+2] for i in range(0, len(line), 2)]
                log_list.extend(line)
    else:
        print("Error: unsupported extension")
        exit()

    return log_list


def session_to_dict(session):
    d_session = {}
    start_index = 0

    for category, length in LOG_CATEGORY.items():
        end_index = start_index + length * 16
        d_session[category] = session[start_index:end_index]
        start_index = end_index

    return d_session


def parse(d_session):
    d_parsed = {}

    for _category, _data in d_session.items():
        # breakpoint()
        if _category == "DATALOG_CAT_CRC":
            d_parsed[_category] = {
                "CRC": _data[-4:],
                "TIME_STAMP": str(int("0x"+"".join(_data[-8:-4]), 16)) + "ms"}
        else:
            if _category == "DATALOG_CAT_POWER_IC":
                '''Check if first lot is overwritten.   
                If so, the lot will be moved to the end of data
                '''
                if _data[6] != 'BB' or (_data[5] not in ['09', '0A', '0B']):
                    _data.extend(_data[:16])
                    _data = _data[16:]

            d_parsed[_category] = {}
            num = 1
            while _data and _data[0] != '00':
                data_length = _data[0]  # data length
                # four bytes time stamp to indicate number of ms since power on
                time_stamp = _data[1:5]
                data_id = _data[5]  # logging data ID
                # additional data ID reserved for CAN FD usage. For other types of event, it uses 0xBB as padding
                reserved = _data[6]

                if reserved != "BB":
                    data_id = "".join(_data[5:6])
                    reserved = ""

                # actual data payload (length indicated in byte 1)
                data = _data[7:7+int("0x"+data_length, 16)]

                total_length = len(data_length) + len(time_stamp) + \
                    len(data_id) + len(reserved) + len(data)
                lot_length = total_length + (16-total_length % 16)

                d_data = {
                    "DATA_ID": data_id,
                    "DATA_NAME": D_LOG_DATA_ID[data_id],
                    "DATA_LENGTH": str(int("0x"+data_length, 16))+"bytes",
                    "DATA": " ".join(data),
                    "TIME_STAMP": str(int("0x"+"".join(time_stamp), 16)) + "ms",
                }

                d_parsed[_category][f"data_{num:04}"] = d_data
                num += 1

                _data = _data[lot_length:]

    return d_parsed


def main():
    log = input("Input the full path of source file to parse:\n")
    sessions = log_to_list(log)
    session1 = sessions[:SIZE_OF_SESSION]
    session2 = sessions[SIZE_OF_SESSION:SIZE_OF_SESSION*2]
    session3 = sessions[SIZE_OF_SESSION*2:SIZE_OF_SESSION*3]

    for i, session in enumerate([session1, session2, session3], 1):
        try:
            print(
                f"==========================Session {i} Start============================")
            d_session = session_to_dict(session)
            d_parsed = parse(d_session)
            pprint(d_parsed, sort_dicts=False)
        except:
            print(f"Error: Session {i} data is not good to parse")
        finally:
            print(
                f"==========================Session {i} End==============================\n")


if __name__ == "__main__":
    main()
