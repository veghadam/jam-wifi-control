# JAM WiFi Speaker API Control

Replace the discontinued JAM WiFi APK with direct LinkPlay API calls.

## Quick Start

### If you know the speaker IP:
```bash
./venv/bin/python3 test_speaker.py <IP_ADDRESS>

# Example:
./venv/bin/python3 test_speaker.py 192.168.3.100
```

### To find the speaker IP:

**Method 1: Check your router's DHCP clients**
- Login to router (usually http://192.168.3.1)
- Look for device named "JAM", "Rhythm", "Symphony", "LinkPlay", or similar

**Method 2: Use the original JAM app (if still installed)**
- Open the app, it may show the IP in settings

**Method 3: Speaker setup mode**
- Press and hold WiFi button on speaker
- Connect to its WiFi hotspot (name: JAM-XXXX or similar)
- Visit http://10.10.10.254 in browser
- Check current network settings

**Method 4: Use nmap (if installed)**
```bash
nmap -p 8080 --open 192.168.3.0/24
```

### To scan networks:
```bash
# Scan 192.168.3.x network
./venv/bin/python3 scan_network.py

# Scan 192.168.1.x network
./venv/bin/python3 quick_scan.py
```

## API Commands

Once you have the speaker IP, use the LinkPlay HTTP API:

### Get Status
```bash
curl 'http://<IP>/httpapi.asp?command=getStatus'
curl 'http://<IP>/httpapi.asp?command=getStatusEx'
curl 'http://<IP>/httpapi.asp?command=getPlayerStatus'
```

### Control Playback
```bash
# Volume (0-100)
curl 'http://<IP>/httpapi.asp?command=setPlayerCmd:vol:50'

# Play/Pause
curl 'http://<IP>/httpapi.asp?command=setPlayerCmd:play'
curl 'http://<IP>/httpapi.asp?command=setPlayerCmd:pause'

# Next/Previous track
curl 'http://<IP>/httpapi.asp?command=setPlayerCmd:next'
curl 'http://<IP>/httpapi.asp?command=setPlayerCmd:prev'

# Mute
curl 'http://<IP>/httpapi.asp?command=setPlayerCmd:mute:1'  # mute
curl 'http://<IP>/httpapi.asp?command=setPlayerCmd:mute:0'  # unmute
```

### Multi-room (Grouping)
```bash
# Create group (master_ip groups with slave_ip)
curl 'http://<MASTER_IP>/httpapi.asp?command=ConnectMasterAp:ssid:eth<SLAVE_IP>:eth'

# Leave group
curl 'http://<IP>/httpapi.asp?command=multiroom:Ungroup'
```

## Python Usage

```python
from discover_speakers import JAMSpeaker

# Connect to speaker
speaker = JAMSpeaker("192.168.3.100")

# Get status
status = speaker.get_status()
print(status)

# Control playback
speaker.set_volume(60)
speaker.play()
speaker.pause()
speaker.next_track()
```

## Files

- **discover_speakers.py** - Auto-discovery with interactive control
- **test_speaker.py** - Quick manual test for specific IP
- **scan_network.py** - Scan 192.168.3.x network
- **quick_scan.py** - Scan 192.168.1.x network
- **diagnostics.py** - Network troubleshooting
- **find_ip.sh** - IP discovery helper

## Troubleshooting

**No speakers found:**
1. Check speaker is powered on
2. Verify speaker is in WiFi mode (not Bluetooth)
3. Confirm speaker is on same network
4. Check firewall/network isolation settings
5. Try factory reset on speaker

**Can't connect to speaker:**
- Verify you can ping the speaker IP
- Check port 8080 is accessible
- Ensure no VPN is blocking local network access

## Resources

- [Official Arylic LinkPlay API](https://developer.arylic.com/httpapi/)
- [LinkPlay API Documentation](https://github.com/AndersFluur/LinkPlayApi)
- [Home Assistant Integration](https://github.com/nagyrobi/home-assistant-custom-components-linkplay)
