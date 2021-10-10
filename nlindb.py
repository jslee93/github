from influxdb import InfluxDBClient

_host = '127.0.0.1'
_port = "8086"
_user = "None"
_pass = "None"

def connectInflux(name):
  indb = InfluxDBClient(_host, _port, _user, _pass, name)
  indb.switch_database(name)
  return indb
