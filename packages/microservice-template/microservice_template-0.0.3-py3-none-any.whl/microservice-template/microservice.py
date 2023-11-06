from flask import Flask, request, jsonify
from flask_cors import CORS

class Microservice:
    id_counter = 0;
    def __init__(self, service_name, port):
        self.app = Flask(service_name)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.port = port

    def buildResponse(self, data, status=200):
        response = jsonify(data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, status
    
    @self.app.route("/check_status", methods=["GET"])
    def check_status(self):
        return self.buildResponse({"status": f"{self.service_name} is online"})

    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=self.port)