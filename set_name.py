#!/usr/bin/env python3
"""
Set speaker device name
Can be used in pairing mode (10.10.10.254) or when on network
"""

import urllib.request
import sys

def set_name(speaker_ip, name):
    """Try different commands to set device name"""

    print(f"Attempting to set speaker name to: {name}")
    print(f"Speaker IP: {speaker_ip}")
    print("="*60)

    # Try different command formats
    commands = [
        f"setDeviceName:{name}",
        f"DeviceName:{name}",
        f"setDeviceName&name={name}",
        f"setName:{name}",
        f"setSSID:{name}",
        f"setDeviceName:{name.encode('utf-8').hex()}",  # hex encoded
    ]

    for idx, cmd in enumerate(commands, 1):
        print(f"\n{idx}. Testing: {cmd}")
        url = f"http://{speaker_ip}/httpapi.asp?command={cmd}"

        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                result = response.read().decode('utf-8')
                print(f"   Response: {result}")

                if "OK" in result or "ok" in result.lower():
                    print(f"   ✅ SUCCESS!")

                    # Verify by getting status
                    print("\n   Verifying name change...")
                    verify_url = f"http://{speaker_ip}/httpapi.asp?command=getStatus"
                    with urllib.request.urlopen(verify_url, timeout=5) as verify_response:
                        import json
                        status = json.loads(verify_response.read().decode('utf-8'))
                        print(f"   Current name: {status.get('DeviceName', 'Unknown')}")

                    return True
                elif "unknown" not in result.lower():
                    print(f"   ⚠️  Different response (not 'unknown command')")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "="*60)
    print("Could not find working command to set name")
    print("You may need to set it after speaker is on WiFi")
    return False

def main():
    if len(sys.argv) < 2:
        print("Set JAM WiFi Speaker Device Name")
        print("="*60)
        print()
        print("Usage:")
        print("  In pairing mode (connected to speaker hotspot):")
        print("    python set_name.py <NEW_NAME>")
        print()
        print("  When speaker is on network:")
        print("    python set_name.py <NEW_NAME> <SPEAKER_IP>")
        print()
        print("Examples:")
        print("  python set_name.py 'Living Room'")
        print("  python set_name.py 'Kitchen Speaker' 192.168.1.100")
        sys.exit(1)

    name = sys.argv[1]

    # Check if IP provided, otherwise assume pairing mode
    if len(sys.argv) > 2:
        speaker_ip = sys.argv[2]
    else:
        speaker_ip = "10.10.10.254"  # Default pairing mode IP

    set_name(speaker_ip, name)

if __name__ == "__main__":
    main()
