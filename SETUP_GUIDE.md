# JAM WiFi Speaker Setup Guide

## Quick Setup Process

### Option 1: Using the Setup Script (Recommended)

```bash
# Make script executable
chmod +x setup.py

# Run the setup wizard
./venv/bin/python3 setup.py
```

The script will guide you through:
1. Connecting to the speaker's WiFi hotspot
2. Scanning available networks
3. Configuring WiFi credentials
4. Connecting the speaker to your network

### Option 2: Manual Setup via Browser

1. **Enter Pairing Mode:**
   - Press and hold the WiFi button on your JAM speaker
   - Wait for WiFi LED to blink (usually 3-5 seconds)
   - Speaker creates WiFi hotspot: `JAM SYMPHONY_XXXX` or `JAM-XXXX`

2. **Connect to Speaker:**
   - On your Mac/PC, go to WiFi settings
   - Connect to the JAM hotspot (no password required)
   - Wait for connection to establish

3. **Configure via Browser:**
   - Open browser and go to: `http://10.10.10.254`
   - You should see the LinkPlay configuration interface
   - Select your home WiFi network
   - Enter your WiFi password
   - Click "Connect" or "Apply"

4. **Return to Home Network:**
   - Wait 10-20 seconds for speaker to connect
   - Reconnect your Mac/PC to your home WiFi
   - Speaker should now be on your network

### Option 3: Direct API Configuration

```bash
# 1. Connect to speaker's hotspot first
# 2. Run these commands:

# Get available networks
curl 'http://10.10.10.254/httpapi.asp?command=wlanGetApListEx'

# Configure WiFi (replace SSID_HEX and PASSWORD_HEX)
# SSID in hex: echo -n "YourSSID" | xxd -p
# Password in hex: echo -n "YourPassword" | xxd -p

curl 'http://10.10.10.254/httpapi.asp?command=wlanConnectAp:ssid=SSID_HEX:ch=0:auth=4:encry=4:pwd=PASSWORD_HEX:chext=0'
```

## Finding Your Speaker After Setup

### Method 1: Use Discovery Script
```bash
./venv/bin/python3 scan_network.py
```

### Method 2: Check Router
- Login to your router (usually http://192.168.3.1 or http://192.168.1.1)
- Look at DHCP clients/connected devices
- Find device named "JAM SYMPHONY_XXXX"

### Method 3: Check ARP Cache
```bash
arp -a | grep -i jam
```

### Method 4: Manual Scan
```bash
# Scan for devices with port 8080 open
nmap -p 8080 --open 192.168.3.0/24
```

## Troubleshooting

### Speaker Won't Enter Pairing Mode
- **Solution:** Hold WiFi button for 5-10 seconds until LED blinks rapidly
- Try factory reset: Hold WiFi button for 15+ seconds
- Power cycle the speaker

### Can't See Speaker's WiFi Hotspot
- **Check:** Make sure WiFi LED is blinking on speaker
- **Check:** Look for networks starting with "JAM", "SYMPHONY", or "HMDX"
- **Check:** Speaker might already be connected to your WiFi (check router)
- Try moving closer to the speaker

### Can't Connect to 10.10.10.254
- **Check:** Verify you're connected to the speaker's WiFi hotspot (not your home WiFi)
- **Check:** Try pinging: `ping 10.10.10.254`
- **Check:** Disable VPN if you have one active
- Try different browser or clear cache
- Check firewall settings

### Configuration Succeeds but Speaker Doesn't Connect
- **Check:** SSID and password are correct (case-sensitive!)
- **Check:** Your WiFi is 2.4GHz (speaker may not support 5GHz)
- **Check:** Router security is WPA/WPA2-PSK (not WPA3)
- **Check:** Router MAC filtering isn't blocking speaker
- **Check:** Router has available DHCP addresses
- Try using a mobile hotspot first to test

### Speaker Connects but Can't Find It on Network
- **Wait:** Give it 30-60 seconds after configuration
- **Check:** Router's connected devices list
- **Check:** Your computer is on the same network
- **Check:** Network allows device-to-device communication (not guest network)
- Try pinging broadcast: `ping 192.168.3.255`

### Factory Reset
If all else fails, factory reset the speaker:
1. Hold WiFi button for 15-20 seconds
2. Speaker will reset to factory settings
3. Start setup process again

## Quick Test After Setup

Once you find the speaker's IP:

```bash
# Test connection
./venv/bin/python3 test_speaker.py <SPEAKER_IP>

# Quick status check
curl 'http://<SPEAKER_IP>/httpapi.asp?command=getStatus'

# Set volume
curl 'http://<SPEAKER_IP>/httpapi.asp?command=setPlayerCmd:vol:50'
```

## Network Requirements

- **WiFi Standard:** 802.11 b/g/n
- **Frequency:** 2.4 GHz (5GHz may not be supported)
- **Security:** WPA/WPA2-PSK (WPA3 may not work)
- **Ports:** 8080, 8819, 8899 (outbound)
- **Protocols:** HTTP, UPnP/SSDP

## Advanced: WiFi Configuration Parameters

When using the API directly:

```
wlanConnectAp:ssid=<HEX>:ch=<CHANNEL>:auth=<AUTH>:encry=<ENCRY>:pwd=<HEX>:chext=0

Parameters:
- ssid: Network SSID in hexadecimal
- ch: WiFi channel (use 0 for auto)
- auth: Authentication type
    0 = Open
    1 = WEP
    4 = WPA/WPA2-PSK
- encry: Encryption type
    0 = None
    1 = WEP
    4 = AES/TKIP
- pwd: Password in hexadecimal (empty for open networks)
- chext: Extended channel (0 = 20MHz, 1 = 40MHz)
```

### Convert String to Hex
```bash
# On Mac/Linux
echo -n "YourSSID" | xxd -p
echo -n "YourPassword" | xxd -p

# In Python
"YourSSID".encode().hex()
"YourPassword".encode().hex()
```

## Multiple Speakers Setup

To set up multiple speakers:

1. Set up each speaker individually using this guide
2. Give each a unique device name (optional)
3. Once all are on WiFi, use multi-room commands to group them
4. See README.md for multi-room grouping commands

## Support

If you're still having issues:

1. Check speaker firmware version: Should be 4.2.x or higher
2. Try connecting speaker directly to router with ethernet (if supported)
3. Check LinkPlay documentation: https://developer.arylic.com/httpapi/
4. Reset speaker to factory defaults and try again
