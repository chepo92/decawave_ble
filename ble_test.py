import bluepy.btle
import pprint

# Path for saving results
output_path = 'scan_results.txt'

# BLE advertising data type codes
SHORT_LOCAL_NAME_AD_CODE = 8

# Known Decawave services (from documentation)
NETWORK_NODE_SERVICE_UUID = '680c21d9-c946-4c1f-9c11-baa1c21329e7'

# Uknown Decawave services (found in scan)
UNKNOWN_01_SERVICE_UUID = '00001801-0000-1000-8000-00805f9b34fb'
UNKNOWN_02_SERVICE_UUID = '00001800-0000-1000-8000-00805f9b34fb'

# Known Decawave characteristics for network node service (from documentation)
OPERATION_MODE_CHARACTERISTIC_UUID = '3f0afd88-7770-46b0-b5e7-9fc099598964'
NETWORK_ID_CHARACTERISTIC_UUID = '80f9d8bc-3bff-45bb-a181-2d6a37991208'
LOCATION_DATA_MODE_CHARACTERISTIC_UUID = 'a02b947e-df97-4516-996a-1882521e0ead'
LOCATION_DATA_CHARACTERISTIC_UUID = '003bbdf2-c634-4b3d-ab56-7ec889b89a37'
PROXY_POSITION_CHARACTERISTIC_UUID = 'f4a67d7d-379d-4183-9c03-4b6ea5103291'
DEVICE_INFO_CHARACTERISTIC_UUID = '1e63b1eb-d4ed-444e-af54-c1e965192501'
STATISTICS_CHARACTERISTIC_UUID = '0eb2bc59-baf1-4c1c-8535-8a0204c69de5'
FW_UPDATE_PUSH_CHARACTERISTIC_UUID = '5955aa10-e085-4030-8aa6-bdfac89ac32b'
FW_UPDATE_POLL_CHARACTERISIC_UUID = '9eed0e27-09c0-4d1c-bd92-7c441daba850'
DISCONNECT_CHARACTERISTIC_UUID = 'ed83b848-da03-4a0a-a2dc-8b401080e473'

# Unknown Decawave characteristics for network node service (found in scan)
UNKNOWN_01_CHARACTERISTIC_UUID = 'f0f26c9b-2c8c-49ac-ab60-fe03def1b40c'
UNKNOWN_02_CHARACTERISTIC_UUID = '7bd47f30-5602-4389-b069-8305731308b6'
UNKNOWN_03_CHARACTERISTIC_UUID = '17b1613e-98f2-4436-bcde-23af17a10c72'
UNKNOWN_04_CHARACTERISTIC_UUID = '28d01d60-89de-4bfa-b6e9-651ba596232c'
UNKNOWN_05_CHARACTERISTIC_UUID = '5b10c428-af2f-486f-aee1-9dbd79b6bccb'

# Function for identifying Decawave devices
def is_decawave_scan_entry(scan_entry):
	short_local_name = scan_entry.getValueText(SHORT_LOCAL_NAME_AD_CODE)
	return (short_local_name is not None and short_local_name.startswith('DW'))

# Create scanner object
scanner = bluepy.btle.Scanner()

# Scan for BLE devices
print('Scanning for BLE devices.')
scan_entries = scanner.scan()
print('Finished scanning for BLE devices.')

# Filter for Decawave devices
decawave_scan_entries = list(filter(is_decawave_scan_entry, scan_entries))
num_decawave_devices = len(decawave_scan_entries)
print('Found {} Decawave devices.'.format(num_decawave_devices))

# Get services and characteristics for Decawave devices
print('Getting services and characteristics for Decawave devices.')
decawave_devices = []
for decawave_scan_entry in decawave_scan_entries:
	mac_address = decawave_scan_entry.addr
	addrType = decawave_scan_entry.addrType
	iface = decawave_scan_entry.iface
	rssi = decawave_scan_entry.rssi
	connectable = decawave_scan_entry.connectable
	print('Getting scan data for Decawave device {}'.format(mac_address))
	scan_data = decawave_scan_entry.getScanData()
	scan_data_information = []
	for scan_data_tuple in scan_data:
		type_code = scan_data_tuple[0]
		description = scan_data_tuple[1]
		value = scan_data_tuple[2]
		scan_data_information.append({
			'type_code': type_code,
			'description': description,
			'value': value})
	peripheral = bluepy.btle.Peripheral()
	print('\nConnecting to Decawave device {}'.format(mac_address))
	peripheral.connect(mac_address)
	print('Getting services for Decawave device {}'.format(mac_address))
	services = list(peripheral.getServices())
	services_information = []
	for service in services:
		service_uuid = service.uuid
		print('Getting characteristics for service UUID: {}'.format(service_uuid))
		characteristics = service.getCharacteristics()
		characteristics_information = []
		for characteristic in characteristics:
			characteristic_uuid = characteristic.uuid
			print('\tCharacteristic UUID: {}'.format(characteristic_uuid))
			characteristics_information.append({
				'characteristic_uuid': characteristic_uuid})
		services_information.append({
			'service_uuid': service_uuid,
			'characteristics': characteristics_information})
	peripheral.disconnect()
	decawave_devices.append({
		'mac_address': mac_address,
		'addrType': addrType,
		'iface': iface,
		'rssi': rssi,
		'connectable': connectable,
		'scan_data': scan_data_information,
		'services': services_information})

# Write results to file
print('Saving results in {}'.format(output_path))
with open(output_path, 'w') as file:
	file.write('\nDecawave devices found:\n')
	for decawave_device in decawave_devices:
		print(decawave_device.keys())
		file.write('\nDevice MAC address: {}\n'.format(decawave_device['mac_address']))
		file.write('Address type: {}\n'.format(decawave_device['addrType']))
		file.write('Interface number: {}\n'.format(decawave_device['iface']))
		file.write('RSSI (dB): {}\n'.format(decawave_device['rssi']))
		file.write('Connectable: {}\n'.format(decawave_device['connectable']))
		for scan_data_item in decawave_device['scan_data']:
			file.write('\n\tType code: {}\n\tDesc: {}\n\tValue: {}\n '.format(
				scan_data_item['type_code'],
				scan_data_item['description'],
				scan_data_item['value']))
