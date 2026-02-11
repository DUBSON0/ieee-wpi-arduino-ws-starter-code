#!/usr/bin/env python3
"""
Test client for the ESP32 Radio Server.
Makes GET requests to the server endpoints and prints responses.

Usage:
    python test_server.py                    # Show all stations
    python test_server.py --station 0        # Get song data for station 0
    python test_server.py --health           # Health check
    python test_server.py --all              # Fetch all songs from all stations
    python test_server.py --host 10.0.0.5    # Use a custom server IP
    python test_server.py --port 8080        # Use a custom port
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def make_request(url):
    """Make a GET request and return the parsed JSON response."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return response.status, data
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode()) if e.fp else {}
        return e.code, body
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to server at {url}")
        print(f"  Reason: {e.reason}")
        sys.exit(1)


def print_json(data):
    """Pretty-print a JSON object."""
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Test client for the ESP32 Radio Server")
    parser.add_argument("--host", default="192.168.0.100", help="Server IP address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Server port (default: 5000)")
    parser.add_argument("--station", type=int, metavar="N", help="Get song data for station N (0-9)")
    parser.add_argument("--health", action="store_true", help="Run health check")
    parser.add_argument("--all", action="store_true", help="Fetch song data for all stations")

    args = parser.parse_args()
    base_url = f"http://{args.host}:{args.port}"

    if args.health:
        print(f"GET {base_url}/health")
        status, data = make_request(f"{base_url}/health")
        print(f"Status: {status}")
        print_json(data)

    elif args.station is not None:
        url = f"{base_url}/song?station={args.station}"
        print(f"GET {url}")
        status, data = make_request(url)
        print(f"Status: {status}")
        print_json(data)

    elif args.all:
        # First list all stations
        print(f"GET {base_url}/stations")
        status, stations = make_request(f"{base_url}/stations")
        print(f"Status: {status}")
        print_json(stations)
        print()

        # Then fetch each station's song data
        for i in range(10):
            url = f"{base_url}/song?station={i}"
            print(f"GET {url}")
            status, data = make_request(url)
            name = stations.get(str(i), {}).get("name", "Unknown")
            print(f"  Station {i} ({name}): {len(data.get('frequencies', []))} notes")
        print("\nAll stations fetched successfully.")

    else:
        # Default: list stations
        print(f"GET {base_url}/stations")
        status, data = make_request(f"{base_url}/stations")
        print(f"Status: {status}")
        print()
        for station_id in sorted(data.keys(), key=int):
            info = data[station_id]
            print(f"  Station {station_id}: {info['name']}")


if __name__ == "__main__":
    main()
