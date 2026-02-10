# JAM WiFi Speaker Control

Control your JAM WiFi speakers (Symphony, Rhythm, Voice) using the LinkPlay HTTP API - no discontinued app needed!

This project provides a complete replacement for the discontinued JAM WiFi mobile app, allowing you to:
- Set up new speakers (WiFi configuration)
- Control playback (play, pause, volume, next/previous)
- Configure device names
- Discover speakers on your network
- Create multi-room audio groups

## 🎯 Features

- **Complete Setup Tool** - Configure WiFi and device name in one step
- **Auto-Discovery** - Find speakers on your network automatically
- **Offline Setup** - WiFi configuration works without internet
- **Multi-Room Support** - Group multiple speakers
- **Network Diagnostics** - Troubleshooting tools included
- **Pure Python** - No external dependencies except standard library

## 🚀 Quick Start

### Prerequisites

- Python 3.6+
- JAM WiFi Speaker (Symphony, Rhythm, or Voice model)
- Mac/Linux/Windows computer

### Installation

```bash
# Clone the repository
git clone https://github.com/veghadam/jam-wifi-control.git
cd jam-wifi-control

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setup a New Speaker

1. **Put speaker in pairing mode:**
   - Press and hold WiFi button for 5-10 seconds
   - Wait for WiFi LED to blink
   - Speaker creates hotspot: `JAM SYMPHONY_XXXX`

2. **Connect your computer to speaker's WiFi hotspot**

3. **Run the setup script:**
   ```bash
   python3 setup.py
   ```

4. **Follow the prompts:**
   - Enter speaker name (e.g., "Living Room")
   - Enter your WiFi network name
   - Enter WiFi password
   - Confirm and wait for speaker to connect

5. **Done!** Speaker will automatically reboot and connect to your WiFi

### Control an Existing Speaker

```bash
# Find speakers on your network
python3 scan_network.py  # or scan_192_168_1.py for different subnet

# Test a specific speaker
python3 test_speaker.py 192.168.1.100

# Interactive control
python3 discover_speakers.py
```

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[PAIRING_INSTRUCTIONS.txt](PAIRING_INSTRUCTIONS.txt)** - Step-by-step pairing guide
- **[API_REFERENCE.md](#api-reference)** - HTTP API command reference

## 🛠️ Available Tools

### Setup & Configuration
- **`setup.py`** - Main setup wizard (configure speaker name + WiFi)

### Discovery & Control
- **`discover_speakers.py`** - Auto-discover speakers with interactive control
- **`scan_network.py`** - Network scanner (auto-detects network or specify subnet)
- **`test_speaker.py`** - Quick test of specific speaker IP
- **`diagnostics.py`** - Network troubleshooting tools

### Advanced
- **`set_name.py`** - Change speaker device name

## 🎵 API Examples

### Control via Command Line

```bash
# Get status
curl 'http://192.168.1.100/httpapi.asp?command=getPlayerStatus'

# Set volume to 50%
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:vol:50'

# Play/Pause
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:play'
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:pause'

# Next/Previous
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:next'
curl 'http://192.168.1.100/httpapi.asp?command=setPlayerCmd:prev'
```

### Control via Python

```python
from discover_speakers import JAMSpeaker

# Connect to speaker
speaker = JAMSpeaker("192.168.1.100")

# Control playback
speaker.set_volume(60)
speaker.play()
speaker.pause()
speaker.next_track()

# Get status
status = speaker.get_status()
print(f"Volume: {status['vol']}")
```

## 🔧 Troubleshooting

### Speaker won't enter pairing mode
- Hold WiFi button longer (10-15 seconds)
- Try factory reset: hold WiFi button for 20+ seconds
- Power cycle the speaker

### Can't connect to speaker hotspot
- Make sure WiFi LED is blinking
- Look for networks starting with "JAM" or "HMDX"
- Move closer to the speaker

### Speaker won't connect to WiFi
- Check SSID and password are correct (case-sensitive!)
- Ensure WiFi is 2.4GHz (speakers don't support 5GHz)
- Verify router uses WPA/WPA2 (not WPA3)
- Check router has available DHCP addresses

### Can't find speaker after setup
- Wait 30-60 seconds after configuration
- Check router's DHCP client list
- Run network scan: `python3 scan_network.py`
- Check speaker and computer are on same network

## 🏗️ Technical Details

### Supported Models
- JAM Symphony (HX-W14901)
- JAM Rhythm (HX-W09901)
- JAM Voice (HX-P590)

### Requirements
- **WiFi**: 802.11 b/g/n, 2.4GHz
- **Security**: WPA/WPA2-PSK (WPA3 may not work)
- **Ports**: 8080 (HTTP), 8819, 8899

### LinkPlay Protocol
JAM WiFi speakers use the LinkPlay A31 module (firmware 4.2.x). This project uses the LinkPlay HTTP API for communication.

**Key Commands:**
- `getStatus` - Device information
- `getPlayerStatus` - Playback status
- `wlanConnectApEx:ssid=HEX:ch=0:auth=WPA2PSK:encry=AES:pwd=HEX:chext=1` - WiFi configuration (extracted from official app)
- `setDeviceName:NAME` - Change device name
- `setPlayerCmd:CMD` - Playback control

**Note:** The WiFi configuration command was reverse-engineered from the official JAM WiFi Android app to ensure 100% compatibility.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Areas for Contribution
- Support for additional LinkPlay devices
- Home Assistant integration
- Web-based control interface
- Streaming service integration (Spotify, etc.)
- Multi-room synchronization improvements

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LinkPlay API Documentation](https://developer.arylic.com/httpapi/)
- [AndersFluur/LinkPlayApi](https://github.com/AndersFluur/LinkPlayApi)
- [Home Assistant LinkPlay Integration](https://github.com/nagyrobi/home-assistant-custom-components-linkplay)

## ⚠️ Disclaimer

This is an unofficial project and is not affiliated with, endorsed by, or connected to JAM Audio, HMDX, or LinkPlay. Use at your own risk.

## 📮 Support

- **Issues**: [GitHub Issues](https://github.com/veghadam/jam-wifi-control/issues)
- **Discussions**: [GitHub Discussions](https://github.com/veghadam/jam-wifi-control/discussions)

---

**Made with ❤️ by the community**

*Giving new life to discontinued hardware*
