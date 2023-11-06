from flask import Flask, request, jsonify
from flask_cors import CORS

class Microservice:
    id_counter = 0;
    def __init__(self, service_name, port):
        self.app = Flask(service_name)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.port = port

    def build_response(self, data, status=200):
        response = jsonify(data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, status
    
    def check_status(self):
        return self.build_response({"status": f"{self.service_name} is online"})

    def run(self):
        self.app.add_url_rule('/check_status', 'check_status', self.check_status)
        self.app.run(debug=True, host="0.0.0.0", port=self.port)