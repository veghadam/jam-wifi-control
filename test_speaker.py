#!/usr/bin/env python3
"""Quick test of a JAM WiFi speaker at a specific IP"""

import requests
import json
import sys

def test_speaker(ip):
    """Test LinkPlay API commands on a speaker"""
    base_url = f"http://{ip}/httpapi.asp"

    print(f"Testing speaker at {ip}")
    print("=" * 60)

    # Test commands
    commands = {
        "Device Status": "getStatus",
        "Extended Status": "getStatusEx",
        "Player Status": "getPlayerStatus",
    }

    for name, cmd in commands.items():
        print(f"\n{name} ({cmd}):")
        try:
            response = requests.get(f"{base_url}?command={cmd}", timeout=3)
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(json.dumps(data, indent=2))
                except:
                    print(response.text)
            else:
                print(f"HTTP {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_speaker.py <speaker-ip>")
        print("Example: python test_speaker.py 192.168.1.100")
        sys.exit(1)

    test_speaker(sys.argv[1])
