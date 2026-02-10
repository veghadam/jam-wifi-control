#!/usr/bin/env python3
"""
Universal network scanner for JAM WiFi speakers
Scans any network range you specify
"""

import requests
import socket
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_speaker(ip):
    """Check if an IP is a LinkPlay speaker"""
    try:
        # Check if port 8080 is open
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, 8080))
        sock.close()

        if result == 0:
            # Port is open, try LinkPlay API
            try:
                response = requests.get(f"http://{ip}/httpapi.asp?command=getStatus", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    return (ip, True, data)
            except:
                pass

        return (ip, False, None)
    except Exception as e:
        return (ip, False, None)

def get_local_network():
    """Detect local network range"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()

        # Get network prefix (e.g., 192.168.1)
        network_prefix = '.'.join(local_ip.split('.')[:-1])
        return network_prefix
    except:
        return None

def scan_network(network_prefix):
    """Scan a network for JAM speakers"""
    print(f"🔍 Scanning {network_prefix}.0/24 for JAM WiFi speakers...")
    print("=" * 60)
    print("This will scan 254 IPs, please wait...\n")

    # Generate all IPs
    ips = [f"{network_prefix}.{i}" for i in range(1, 255)]

    speakers_found = []
    checked = 0

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_speaker, ip): ip for ip in ips}

        for future in as_completed(futures):
            checked += 1
            ip, is_speaker, data = future.result()

            if is_speaker:
                print(f"\n✅ FOUND SPEAKER at {ip}")
                speakers_found.append((ip, data))
                if data:
                    print(f"   Device: {data.get('DeviceName', 'Unknown')}")
                    print(f"   Model: {data.get('hardware', 'Unknown')}")
                    print(f"   Firmware: {data.get('firmware', 'Unknown')}")
                    print(f"   MAC: {data.get('MAC', 'Unknown')}")

            # Progress indicator
            if checked % 50 == 0:
                print(f"Progress: {checked}/254 IPs checked...")

    print("\n" + "=" * 60)
    if speakers_found:
        print(f"✅ Found {len(speakers_found)} speaker(s)!\n")

        for ip, data in speakers_found:
            print(f"Speaker: {ip}")
            print(f"  Name: {data.get('DeviceName', 'Unknown') if data else 'Unknown'}")
            print(f"  API: http://{ip}/httpapi.asp")
            print()

        print("=" * 60)
        print("Test commands:")
        print("=" * 60)
        for ip, _ in speakers_found:
            print(f"  ./venv/bin/python3 test_speaker.py {ip}")
        print()

    else:
        print(f"❌ No JAM WiFi speakers found on {network_prefix}.0/24")
        print("\nMake sure:")
        print("  - Speakers are powered on")
        print("  - Speakers are in WiFi mode (not Bluetooth)")
        print("  - Speakers are connected to your WiFi network")
        print("  - You can reach this network from this computer")

def main():
    if len(sys.argv) > 1:
        # User specified network
        if sys.argv[1] in ['-h', '--help']:
            print("JAM WiFi Speaker Network Scanner")
            print("=" * 60)
            print()
            print("Usage:")
            print("  python scan_network.py                 # Auto-detect network")
            print("  python scan_network.py 192.168.1       # Scan 192.168.1.0/24")
            print("  python scan_network.py 10.0.0          # Scan 10.0.0.0/24")
            print()
            print("Examples:")
            print("  python scan_network.py")
            print("  python scan_network.py 192.168.0")
            print("  python scan_network.py 10.5.0")
            sys.exit(0)

        network_prefix = sys.argv[1]
    else:
        # Auto-detect
        network_prefix = get_local_network()
        if network_prefix:
            print(f"Auto-detected network: {network_prefix}.0/24")
            print()
        else:
            print("❌ Could not auto-detect network")
            print("Please specify network manually:")
            print("  python scan_network.py 192.168.1")
            sys.exit(1)

    scan_network(network_prefix)

if __name__ == "__main__":
    main()
