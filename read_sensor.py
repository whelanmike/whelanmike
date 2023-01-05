#!/usr/bin/python
import datetime 
import random
from google.cloud import datastore

datastore_client = datastore.Client()

def read_sensor():
    sensor_dict = {}
    read_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_id = str(abs(hash(read_time))) # Generate a positive random int as the Name/ID in Google Datastore.
    external_temp = round (random.uniform(-3, 21), 2)
    greenhouse_temp = round (random.uniform(5, 35), 2)
    filename = '/home/whelanmike/sensor_data/temperature_log_' + read_time.replace('-', '_').replace(' ', '_').replace(':', '_')
    sensor_dict = {'DBID': db_id, 'READ_TIME': read_time, 'EXTERNAL_TEMP': external_temp, 'GREENHOUSE_TEMP': greenhouse_temp, 'FILENAME': filename}
    return  sensor_dict

sensor_readings = read_sensor()
fil_nam =  sensor_readings['FILENAME']
with open(fil_nam, 'w') as log_file:
    log_file.write( str(sensor_readings) + "\n" )

# ----------------- Part(2) of process --------------
DBID = sensor_readings['DBID']
kind = "TemperatureLog"
# The Cloud Datastore key for the new entity
task_key = datastore_client.key(kind, DBID)
task = datastore.Entity(key=task_key)

task["externalCelcius"] = sensor_readings['EXTERNAL_TEMP']
task["greenhouseCelcius"] = sensor_readings['GREENHOUSE_TEMP']
task["logDate"] = datetime.datetime.strptime(sensor_readings['READ_TIME'][:10] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
task["logTime"] = datetime.datetime.strptime('1970-01-01 ' + sensor_readings['READ_TIME'][-8:], '%Y-%m-%d %H:%M:%S')

datastore_client.put(task)

print(f"Saved {task.key.name}: {task['logDate']}: {task['externalCelcius']}: {task['greenhouseCelcius']}")
