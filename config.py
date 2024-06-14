def tablist():
    return ['ACTW','ACLW','AROW']

def unit_dict():
    return {'WaterTemp_ACTW':'°C',
 'Conductivity':None,
 'Salinity':'psu',
 'ACTWVoltage':None,
 'WaterTemp_ACLW':'°C',
 'Chlorophyll':'mg/m3',
 'Turbidity':None,
 'ACLWVoltage':None,
 'LoggerVoltage_Min':None,
 'LoggerTemp':'°C',
 'WaterTemp_AROW':'°C',
 'DO_AROW':'%',
 'AROWVoltage':None,
 'DO_mgL':'mg/L'
 }

## Line notification config

url = "https://api.line.me/v2/bot/message/broadcast"

# UID = 'Udd56a9c385ee19463fa51ff1e388c727'

token = 'nTzbrOCTsKEgNtRadgEeLCjQZ4zRdsFgJGi4PBQ6kTopoyh3WsC172Y3o+7XdVNivsry5kEVdMwG5S2l+cW2zpaC2Wku7ovFU9P/UNioiKUi3akimhUivEvzvndnkoIXKtBIOa1uS1hZyUQadBCI4QdB04t89/1O/w1cDnyilFU='

def npoints():
    return 60*3