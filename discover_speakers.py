#!/usr/bin/env python3
"""
JAM WiFi Speaker Discovery and Control Script
Discovers LinkPlay-based JAM speakers on the network and tests basic API commands.
"""

import socket
import requests
import json
from typing import List, Dict, Optional

class JAMSpeakerDiscovery:
    """Discover and control JAM WiFi speakers using LinkPlay API"""

    LINKPLAY_PORT = 8080
    UPNP_PORT = 1900
    UPNP_MULTICAST = '239.255.255.250'

    @staticmethod
    def discover_upnp(timeout: int = 5) -> List[str]:
        """Discover speakers using UPnP/SSDP"""
        print("🔍 Discovering speakers via UPnP...")

        ssdp_request = (
            'M-SEARCH * HTTP/1.1\r\n'
            'HOST: 239.255.255.250:1900\r\n'
            'MAN: "ssdp:discover"\r\n'
            'MX: 3\r\n'
            'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n'
            '\r\n'
        )

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        devices = []
        try:
            sock.sendto(ssdp_request.encode(), (JAMSpeakerDiscovery.UPNP_MULTICAST, JAMSpeakerDiscovery.UPNP_PORT))

            while True:
                try:
                    data, addr = sock.recvfrom(4096)
                    response = data.decode('utf-8', errors='ignore')
                    if 'MediaRenderer' in response or 'LinkPlay' in response:
                        ip = addr[0]
                        if ip not in devices:
                            devices.append(ip)
                            print(f"   Found device at: {ip}")
                except socket.timeout:
                    break
        except Exception as e:
            print(f"   Error during UPnP discovery: {e}")
        finally:
            sock.close()

        return devices

    @staticmethod
    def scan_network(timeout: float = 0.5) -> List[str]:
        """Scan local network for speakers by trying common IP ranges"""
        print("🔍 Scanning local network for speakers...")

        # Get local IP to determine network range
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        except:
            local_ip = '192.168.1.1'
        finally:
            s.close()

        # Get network prefix (e.g., 192.168.1)
        network_prefix = '.'.join(local_ip.split('.')[:-1])
        print(f"   Scanning network: {network_prefix}.0/24")

        devices = []
        for i in range(1, 255):
            ip = f"{network_prefix}.{i}"
            try:
                # Try to connect to LinkPlay API port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, JAMSpeakerDiscovery.LINKPLAY_PORT))
                sock.close()

                if result == 0:
                    # Port is open, verify it's a LinkPlay device
                    try:
                        response = requests.get(f"http://{ip}/httpapi.asp?command=getStatusEx", timeout=2)
                        if response.status_code == 200:
                            devices.append(ip)
                            print(f"   Found speaker at: {ip}")
                    except:
                        pass
            except:
                pass

        return devices

class JAMSpeaker:
    """Control a JAM WiFi speaker via LinkPlay API"""

    def __init__(self, ip: str):
        self.ip = ip
        self.base_url = f"http://{ip}/httpapi.asp"

    def send_command(self, command: str) -> Optional[Dict]:
        """Send a command to the speaker"""
        try:
            url = f"{self.base_url}?command={command}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json() if response.text else {"raw": response.text}
            return None
        except Exception as e:
            print(f"   Error sending command: {e}")
            return None

    def get_status(self) -> Optional[Dict]:
        """Get detailed speaker status"""
        return self.send_command("getStatusEx")

    def get_device_info(self) -> Optional[Dict]:
        """Get device information"""
        return self.send_command("getStatus")

    def get_player_status(self) -> Optional[Dict]:
        """Get player status"""
        return self.send_command("getPlayerStatus")

    def set_volume(self, level: int) -> Optional[Dict]:
        """Set volume (0-100)"""
        level = max(0, min(100, level))
        return self.send_command(f"setPlayerCmd:vol:{level}")

    def play(self) -> Optional[Dict]:
        """Resume playback"""
        return self.send_command("setPlayerCmd:play")

    def pause(self) -> Optional[Dict]:
        """Pause playback"""
        return self.send_command("setPlayerCmd:pause")

    def next_track(self) -> Optional[Dict]:
        """Skip to next track"""
        return self.send_command("setPlayerCmd:next")

    def prev_track(self) -> Optional[Dict]:
        """Previous track"""
        return self.send_command("setPlayerCmd:prev")


def main():
    print("=" * 60)
    print("JAM WiFi Speaker Discovery & Test")
    print("=" * 60)
    print()

    # Try UPnP discovery first
    devices = JAMSpeakerDiscovery.discover_upnp()

    # If no devices found, try network scan
    if not devices:
        print("\nNo devices found via UPnP, trying network scan...")
        devices = JAMSpeakerDiscovery.scan_network()

    if not devices:
        print("\n❌ No JAM WiFi speakers found on the network.")
        print("   Make sure:")
        print("   - Speakers are powered on")
        print("   - Connected to the same WiFi network")
        print("   - Network allows device-to-device communication")
        return

    print(f"\n✅ Found {len(devices)} speaker(s)")
    print()

    # Test each speaker
    for idx, ip in enumerate(devices, 1):
        print("=" * 60)
        print(f"Testing Speaker #{idx}: {ip}")
        print("=" * 60)

        speaker = JAMSpeaker(ip)

        # Get device info
        print("\n📊 Device Status:")
        status = speaker.get_status()
        if status:
            print(json.dumps(status, indent=2))
        else:
            print("   Failed to get status")

        # Get player status
        print("\n🎵 Player Status:")
        player = speaker.get_player_status()
        if player:
            print(json.dumps(player, indent=2))
        else:
            print("   Failed to get player status")

        print()

    # Interactive control for first speaker
    if devices:
        print("=" * 60)
        print(f"Interactive Control - Speaker: {devices[0]}")
        print("=" * 60)
        speaker = JAMSpeaker(devices[0])

        print("\nAvailable commands:")
        print("  status  - Get current status")
        print("  vol XX  - Set volume (0-100)")
        print("  play    - Resume playback")
        print("  pause   - Pause playback")
        print("  next    - Next track")
        print("  prev    - Previous track")
        print("  quit    - Exit")
        print()

        while True:
            try:
                cmd = input("Command: ").strip().lower()

                if cmd == 'quit':
                    break
                elif cmd == 'status':
                    result = speaker.get_status()
                    print(json.dumps(result, indent=2))
                elif cmd.startswith('vol '):
                    vol = int(cmd.split()[1])
                    result = speaker.set_volume(vol)
                    print(f"Volume set to {vol}: {result}")
                elif cmd == 'play':
                    result = speaker.play()
                    print(f"Play: {result}")
                elif cmd == 'pause':
                    result = speaker.pause()
                    print(f"Pause: {result}")
                elif cmd == 'next':
                    result = speaker.next_track()
                    print(f"Next: {result}")
                elif cmd == 'prev':
                    result = speaker.prev_track()
                    print(f"Previous: {result}")
                else:
                    print("Unknown command")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
