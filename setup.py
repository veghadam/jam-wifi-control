#!/usr/bin/env python3
"""
JAM WiFi Speaker Setup - FIXED VERSION
Uses the correct wlanConnectApEx command from decompiled app
"""

import urllib.request
import urllib.error
import json
import sys
import time

SPEAKER_IP = "10.10.10.254"
BASE_URL = f"http://{SPEAKER_IP}/httpapi.asp"

def http_get(url, timeout=10):
    """Simple HTTP GET"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return None

def check_speaker():
    """Check if speaker is accessible"""
    print("=" * 70)
    print("Checking speaker connection...")
    print("=" * 70)

    url = f"{BASE_URL}?command=getStatus"
    result = http_get(url)

    if result:
        try:
            data = json.loads(result)
            print(f"✅ Speaker found!")
            print(f"   Name: {data.get('DeviceName', 'Unknown')}")
            print(f"   MAC: {data.get('MAC', 'Unknown')}")
            print(f"   Firmware: {data.get('firmware', 'Unknown')}")
            return True
        except:
            print(f"✅ Speaker responding")
            return True
    else:
        print("❌ Cannot reach speaker at 10.10.10.254")
        return False

def set_device_name(name):
    """Set the device name"""
    print("\n" + "=" * 70)
    print(f"Setting device name to: {name}")
    print("=" * 70)

    url = f"{BASE_URL}?command=setDeviceName:{name}"
    result = http_get(url)

    if result and ("OK" in result or "ok" in result.lower()):
        print(f"✅ Name set successfully!")

        # Verify
        verify_url = f"{BASE_URL}?command=getStatus"
        verify_result = http_get(verify_url)
        if verify_result:
            try:
                status = json.loads(verify_result)
                print(f"   Verified name: {status.get('DeviceName', 'Unknown')}")
            except:
                pass
        return True

    print("⚠️  Could not set name")
    return False

def configure_wifi_correct(ssid, password, channel="0"):
    """
    Configure speaker WiFi using wlanConnectApEx (the ACTUAL command from the app)

    This is decompiled from the official JAM WiFi app:
    http://10.10.10.254/httpapi.asp?command=wlanConnectApEx:ssid=HEX:ch=0:auth=WPA2PSK:encry=AES:pwd=HEX:chext=1
    """
    print("\n" + "=" * 70)
    print("Configuring WiFi with wlanConnectApEx (official app command)...")
    print("=" * 70)

    # Convert to hex (uppercase to match app)
    ssid_hex = ssid.encode('utf-8').hex().upper()
    password_hex = password.encode('utf-8').hex().upper() if password else ""

    print(f"Network: {ssid}")
    print(f"Password: {'*' * len(password) if password else '(none)'}")
    print(f"SSID (hex): {ssid_hex}")
    if password:
        print(f"Password (hex): {password_hex}")
    print()

    # Build command exactly like the app does
    if password:
        # WPA2 secured network
        auth = "WPA2PSK"
        encry = "AES"
        pwd_param = f":pwd={password_hex}"
    else:
        # Open network
        auth = "OPEN"
        encry = "NONE"
        pwd_param = ":pwd="

    cmd = f"wlanConnectApEx:ssid={ssid_hex}:ch={channel}:auth={auth}:encry={encry}{pwd_param}:chext=1"
    url = f"{BASE_URL}?command={cmd}"

    print(f"Sending command: wlanConnectApEx")
    print(f"Parameters: ssid={ssid}, ch={channel}, auth={auth}, encry={encry}")
    print()

    result = http_get(url, timeout=15)

    if result:
        print(f"Response: {result}")
        if "OK" in result or "ok" in result.lower():
            print("\n✅ WiFi configuration sent!")
            print("\n⏳ Speaker is now connecting to your WiFi...")
            print("   The speaker will leave its hotspot and connect to your network.")
            print("   This happens automatically!")
            return True
        elif "unknown" in result.lower():
            print(f"\n❌ Command not recognized: {result}")
            print("   Your speaker may have different firmware.")
            return False
        else:
            print(f"\n⚠️  Unexpected response: {result}")
            return False
    else:
        print("\n⚠️  No response (speaker may be connecting)")
        print("   If connection drops now, it's probably working!")
        return True  # Connection drop might mean success

def wait_for_connection(ssid):
    """Wait for speaker to connect"""
    print("\n" + "=" * 70)
    print("Waiting for speaker to connect...")
    print("=" * 70)
    print("\nThe speaker is now:")
    print("  1. Leaving the hotspot (10.10.10.254 will disappear)")
    print("  2. Connecting to your WiFi")
    print("  3. Getting an IP from your router")
    print()
    print("This takes about 10-30 seconds...")
    print()

    for i in range(30):
        print(".", end="", flush=True)
        time.sleep(1)

    print("\n")

def main():
    print("=" * 70)
    print("JAM WiFi Speaker - FIXED Setup")
    print("Using official app command: wlanConnectApEx")
    print("=" * 70)
    print()

    # Check speaker
    if not check_speaker():
        print("\nMake sure:")
        print("  1. Speaker is in pairing mode (WiFi LED blinking)")
        print("  2. You are connected to the speaker's WiFi hotspot")
        sys.exit(1)

    # Get configuration from user
    print("\n" + "=" * 70)
    print("Configuration")
    print("=" * 70)
    print()

    name = input("Enter speaker name (e.g., 'Kitchen', 'Living Room'): ").strip()
    ssid = input("Enter WiFi network name (SSID): ").strip()
    if not ssid:
        print("❌ SSID cannot be empty")
        sys.exit(1)

    password = input("Enter WiFi password (leave empty for open network): ").strip()

    # Confirm
    print("\n" + "=" * 70)
    print("Configuration Summary")
    print("=" * 70)
    print(f"  Speaker Name: {name if name else '(skip)'}")
    print(f"  WiFi Network: {ssid}")
    print(f"  WiFi Password: {'*' * len(password) if password else '(none)'}")
    print("=" * 70)

    confirm = input("\nProceed with configuration? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Setup cancelled")
        sys.exit(0)

    # Set name first (if provided)
    if name:
        set_device_name(name)

    # Configure WiFi using the CORRECT command from decompiled app
    if configure_wifi_correct(ssid, password):
        wait_for_connection(ssid)

        print("=" * 70)
        print("✅ Setup Complete!")
        print("=" * 70)
        print()
        print("Next steps:")
        print(f"  1. Reconnect your Mac to: {ssid}")
        print("  2. Wait 20-30 seconds for speaker to fully connect")
        print("  3. Find the speaker:")
        print("     ./venv/bin/python3 discover_speakers.py")
        if name:
            print(f"     (Look for device named: {name})")
        print("  4. Test it:")
        print("     ./venv/bin/python3 test_speaker.py <SPEAKER_IP>")
        print()
        print("💡 Check your router's DHCP list to find the speaker's IP")
    else:
        print("\n❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(0)
