import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import wmi

class JSONRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':

            w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
            sensor_info = w.Sensor()

            list_of_sensors = []

            for sensor in sensor_info:
                if sensor.SensorType==u'Temperature' or sensor.SensorType==u'Fan':
                    elem = {
                        "identifier": sensor.Identifier,
                        "name": sensor.Name,
                        "value": sensor.Value
                    }
                    list_of_sensors.append(elem)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(list_of_sensors).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_POST(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write("API doesn't support POST")

def run(server_class=HTTPServer, handler_class=JSONRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

# import wmi, json

# w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
# sensor_info = w.Sensor()

# list_of_sensors = []

# for sensor in sensor_info:
#     if sensor.SensorType==u'Temperature' or sensor.SensorType==u'Fan':
#         elem = {
#             "identifier": sensor.Identifier,
#             "name": sensor.Name,
#             "value": sensor.Value
#         }
#         list_of_sensors.append(elem)

# json_str = json.dumps(list_of_sensors)

# with open("data.json", "w") as f:
#     print(json_str, file=f)