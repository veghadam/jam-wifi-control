#!/usr/bin/env python3
"""Network diagnostics for JAM WiFi speaker connectivity"""

import socket
import requests
import subprocess
import json

def get_network_info():
    """Get current network configuration"""
    print("🌐 Network Configuration")
    print("=" * 60)

    try:
        # Get primary IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"Your IP: {local_ip}")

        # Get all network interfaces
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        print("\nActive network interfaces:")
        for line in result.stdout.split('\n'):
            if 'inet ' in line and '127.0.0.1' not in line:
                print(f"  {line.strip()}")

    except Exception as e:
        print(f"Error: {e}")

def test_linkplay_api(ip):
    """Test LinkPlay API endpoints on a specific IP"""
    print(f"\n🧪 Testing LinkPlay API on {ip}")
    print("=" * 60)

    endpoints = {
        "Port 8080 (HTTP)": 8080,
        "Port 80 (HTTP)": 80,
        "Port 49152 (UPnP)": 49152,
    }

    for name, port in endpoints.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            sock.close()

            if result == 0:
                print(f"✅ {name}: OPEN")

                # Try HTTP request if port 80 or 8080
                if port in [80, 8080]:
                    try:
                        url = f"http://{ip}:{port}/httpapi.asp?command=getStatus"
                        response = requests.get(url, timeout=2)
                        if response.status_code == 200:
                            print(f"   LinkPlay API response: {response.text[:100]}")
                    except Exception as e:
                        print(f"   HTTP request failed: {e}")
            else:
                print(f"❌ {name}: CLOSED")
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")

def scan_custom_ip():
    """Allow user to manually enter IP to test"""
    print("\n📝 Manual IP Test")
    print("=" * 60)
    ip = input("Enter speaker IP address (or press Enter to skip): ").strip()

    if ip:
        test_linkplay_api(ip)
        return ip
    return None

def main():
    print("JAM WiFi Speaker Diagnostics")
    print("=" * 60)
    print()

    # Show network info
    get_network_info()

    print("\n" + "=" * 60)
    print("Possible Issues:")
    print("=" * 60)
    print("1. Speaker not powered on")
    print("2. Speaker in Bluetooth mode (switch to WiFi mode)")
    print("3. Speaker on different WiFi network")
    print("4. Computer connected via VPN (disconnect VPN)")
    print("5. Network isolation/firewall blocking communication")
    print("6. Speaker needs factory reset")

    print("\n" + "=" * 60)
    print("To connect speaker to WiFi:")
    print("=" * 60)
    print("1. Use the JAM WiFi app to set up WiFi")
    print("2. Or press and hold the WiFi button on speaker")
    print("3. Look for device name in your WiFi settings")
    print("4. Connect to speaker's WiFi hotspot")
    print("5. Configure your home WiFi through browser at 10.10.10.254")

    # Manual test option
    print()
    tested_ip = scan_custom_ip()

    if tested_ip:
        print(f"\n💡 To test this IP later, run:")
        print(f"   ./venv/bin/python3 test_speaker.py {tested_ip}")

if __name__ == "__main__":
    main()
