#!/usr/bin/env python3
"""
ESP32 Radio Server
Serves song data to ESP32 clients via HTTP GET requests.
Songs are returned as JSON with frequencies and durations.
"""

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Define 10 songs (one per station)
# Each song is a list of (frequency, duration) tuples
# Frequencies in Hz, durations in milliseconds

SONGS = {
    0: {
        "name": "C Major Scale",
        "frequencies": [262, 294, 330, 349, 392, 440, 494, 523],
        "durations": [500, 500, 500, 500, 500, 500, 500, 500]
    },
    1: {
        "name": "Twinkle Twinkle Little Star",
        "frequencies": [262, 262, 392, 392, 440, 440, 392, 349, 349, 330, 330, 294, 294, 262],
        "durations": [500, 500, 500, 500, 500, 500, 1000, 500, 500, 500, 500, 500, 500, 1000]
    },
    2: {
        "name": "Happy Birthday",
        "frequencies": [262, 262, 294, 262, 349, 330, 262, 262, 294, 262, 392, 349, 262, 262, 523, 440, 349, 330, 294],
        "durations": [250, 250, 500, 500, 500, 1000, 250, 250, 500, 500, 500, 1000, 250, 250, 500, 500, 500, 500, 1000]
    },
    3: {
        "name": "Jingle Bells",
        "frequencies": [330, 330, 330, 330, 330, 330, 330, 392, 262, 294, 330, 349, 349, 349, 349, 349, 330, 330, 330, 294, 294, 330, 294, 392],
        "durations": [500, 500, 1000, 500, 500, 1000, 500, 500, 500, 500, 2000, 500, 500, 500, 500, 500, 500, 500, 250, 250, 500, 500, 500, 500]
    },
    4: {
        "name": "Mario Theme",
        "frequencies": [659, 659, 0, 659, 0, 523, 659, 0, 784, 0, 392, 0, 523, 0, 392, 0, 330, 0, 440, 0, 494, 0, 466, 0, 392, 0, 659, 0, 784, 0, 880, 0, 698, 0, 784, 0, 659, 0, 523, 0, 587, 0, 494],
        "durations": [150, 300, 150, 300, 300, 300, 300, 300, 300, 300, 300, 150, 300, 150, 300, 300, 300, 300, 300, 150, 300, 150, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 150, 300, 150, 300, 300, 300, 300, 300, 300, 300]
    },
    5: {
        "name": "Star Wars Theme",
        "frequencies": [440, 440, 440, 349, 523, 440, 349, 523, 440, 659, 659, 659, 698, 523, 415, 349, 523, 440],
        "durations": [500, 500, 500, 350, 150, 500, 350, 150, 650, 500, 500, 500, 350, 150, 500, 350, 150, 650]
    },
    6: {
        "name": "Fur Elise",
        "frequencies": [659, 622, 659, 622, 659, 494, 587, 523, 440, 0, 262, 330, 440, 494, 0, 330, 415, 494, 523, 0, 330, 440, 523, 587],
        "durations": [200, 200, 200, 200, 200, 200, 200, 200, 400, 200, 200, 200, 200, 400, 200, 200, 200, 200, 400, 200, 200, 200, 200, 400]
    },
    7: {
        "name": "Ode to Joy",
        "frequencies": [392, 392, 440, 392, 523, 494, 392, 392, 440, 392, 349, 330, 392, 392, 440, 392, 523, 494, 440, 349, 349, 330, 294, 262],
        "durations": [500, 500, 500, 500, 500, 1000, 500, 500, 500, 500, 500, 1000, 500, 500, 500, 500, 500, 1000, 500, 500, 500, 500, 500, 1000]
    },
    8: {
        "name": "Canon in D",
        "frequencies": [294, 330, 349, 392, 440, 392, 349, 330, 294, 330, 349, 392, 440, 494, 523, 494, 440, 392],
        "durations": [600, 600, 600, 600, 600, 600, 600, 600, 1200, 600, 600, 600, 600, 600, 600, 600, 600, 1200]
    },
    9: {
        "name": "Chromatic Scale",
        "frequencies": [262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494, 523],
        "durations": [400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]
    }
}


@app.route('/song', methods=['GET'])
def get_song():
    """
    Endpoint to get song data for a specific station.
    Query parameter: station (0-9)
    Returns JSON with frequencies and durations arrays.
    """
    try:
        station = request.args.get('station', type=int)
        
        if station is None:
            return jsonify({"error": "Missing station parameter"}), 400
        
        if station < 0 or station > 9:
            return jsonify({"error": "Station must be between 0 and 9"}), 400
        
        song_data = SONGS.get(station)
        if song_data is None:
            return jsonify({"error": f"Station {station} not found"}), 404
        
        # Return only frequencies and durations (not the name)
        response = {
            "frequencies": song_data["frequencies"],
            "durations": song_data["durations"]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/stations', methods=['GET'])
def list_stations():
    """
    Optional endpoint to list all available stations and their song names.
    """
    stations_info = {
        station: {"name": song["name"]} 
        for station, song in SONGS.items()
    }
    return jsonify(stations_info)


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({"status": "ok", "stations": len(SONGS)})


if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) so ESP32 can connect
    # Default port 5000
    print("Starting ESP32 Radio Server...")
    print(f"Server will be available at http://<your-ip>:5000")
    print(f"Example: http://192.168.1.100:5000/song?station=0")
    app.run(host='0.0.0.0', port=5000, debug=True)
