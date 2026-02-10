# JAM WiFi Speaker Control - Quick Start

## 🎯 Your Speaker (Example)
After setup, document your speaker here:
- **IP Address:** 192.168.1.100
- **Name:** Living Room
- **Model:** JAM SYMPHONY
- **Status:** ✅ Configured and working

> Copy this file to `QUICK_START.md` and update with your speaker details

## 🚀 Quick Commands

### Control Your Speaker

Replace `192.168.1.100` with your speaker's IP address:

```bash
# Get status
curl 'http://192.168.1.100/httpapi.asp?command=getPlayerStatus'

# Set volume to 70%
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:vol:70'

# Play
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:play'

# Pause
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:pause'

# Next/Previous track
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:next'
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:prev'
```

### Using Python

```bash
# Interactive control
./venv/bin/python3 discover_speakers.py

# Test speaker
./venv/bin/python3 test_speaker.py 192.168.1.100
```

## 📋 All Available Scripts

### Discovery & Testing
- **`test_speaker.py <IP>`** - Quick test of speaker at specific IP
- **`scan_network.py`** - Auto-detect and scan your network
- **`discover_speakers.py`** - Auto-discover speakers with interactive control
- **`diagnostics.py`** - Network diagnostics and troubleshooting

### Setup & Configuration
- **`setup.py`** - Complete setup wizard (name + WiFi + reboot)
- **`setup.py`** - WiFi-only setup (works offline)
- **`check_speaker_hotspot.py`** - Verify connection to speaker hotspot

### Documentation
- **`README.md`** - Complete API documentation
- **`SETUP_GUIDE.md`** - Detailed setup instructions
- **`PAIRING_INSTRUCTIONS.txt`** - Step-by-step pairing guide

## 🔧 Setting Up a New Speaker

```bash
# Run the complete setup wizard
./venv/bin/python3 setup.py
```

Follow the prompts to:
1. Set speaker name
2. Configure WiFi
3. Automatically reboot and connect

## 📖 Common Tasks

### Find Speaker IP After Setup
```bash
# Method 1: Auto-detect and scan
./venv/bin/python3 scan_network.py

# Method 2: Scan specific network
./venv/bin/python3 scan_network.py 192.168.0

# Method 3: Check router's DHCP client list
# Login to router and look for JAM device
```

### Control Volume
```bash
# Replace with your speaker IP
IP=192.168.1.100

# Set to specific level (0-100)
curl "http://$IP/httpapi.asp?command=setPlayerCmd:vol:50"

# Mute/Unmute
curl "http://$IP/httpapi.asp?command=setPlayerCmd:mute:1"
curl "http://$IP/httpapi.asp?command=setPlayerCmd:mute:0"
```

### Playback Control
```bash
IP=192.168.1.100

# Play/Pause
curl "http://$IP/httpapi.asp?command=setPlayerCmd:play"
curl "http://$IP/httpapi.asp?command=setPlayerCmd:pause"

# Stop
curl "http://$IP/httpapi.asp?command=setPlayerCmd:stop"

# Next/Previous
curl "http://$IP/httpapi.asp?command=setPlayerCmd:next"
curl "http://$IP/httpapi.asp?command=setPlayerCmd:prev"
```

### Get Information
```bash
IP=192.168.1.100

# Device info
curl "http://$IP/httpapi.asp?command=getStatus"

# Player status (what's playing)
curl "http://$IP/httpapi.asp?command=getPlayerStatus"

# Extended status
curl "http://$IP/httpapi.asp?command=getStatusEx"
```

## 🎵 Multi-Room Audio

If you have multiple JAM speakers:

```bash
# Group speakers (master IP groups with slave IP)
curl 'http://MASTER_IP/httpapi.asp?command=ConnectMasterAp:ssid:ethSLAVE_IP:eth'

# Ungroup speaker
curl 'http://SPEAKER_IP/httpapi.asp?command=multiroom:Ungroup'

# Get group info
curl 'http://SPEAKER_IP/httpapi.asp?command=multiroom:getSlaveList'
```

## 💡 Tips

**Save Speaker IP as Environment Variable:**
```bash
# Add to ~/.zshrc or ~/.bashrc
export JAM_SPEAKER="192.168.1.100"

# Create aliases
alias jam-vol='curl "http://$JAM_SPEAKER/httpapi.asp?command=setPlayerCmd:vol:$1"'
alias jam-play='curl "http://$JAM_SPEAKER/httpapi.asp?command=setPlayerCmd:play"'
alias jam-pause='curl "http://$JAM_SPEAKER/httpapi.asp?command=setPlayerCmd:pause"'

# Usage
jam-vol 60
jam-play
```

**Set Static IP:**
- Configure DHCP reservation in your router
- Makes speaker always accessible at same IP

**Home Automation:**
- Integrate with Home Assistant
- Use LinkPlay integration for advanced control

## 📚 More Information

- **Full Documentation:** See README.md
- **Setup Help:** See SETUP_GUIDE.md
- **Troubleshooting:** See SETUP_GUIDE.md
- **API Reference:** See README.md

## ✅ Success!

You now have full control of your JAM WiFi speakers via HTTP API - no discontinued app needed! 🎉
