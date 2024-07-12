from datetime import timedelta

DOMAIN = "dbs2300"
SCAN_INTERVAL = timedelta(seconds=10)


SENSOR_TYPES = {
    "ac_input_power": "AC Input Power",
    "ac_output_power": "AC Output Power",
    "dc_output_power": "DC Output Power",
    "battery_capacity": "Battery Capacity",
}

SWITCH_TYPES = {
    "ac_output_control": "AC Output Control"
}
