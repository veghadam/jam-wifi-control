#!/bin/bash
# Quick ways to find your JAM speaker IP

echo "Method 1: Check ARP cache for recently connected devices"
echo "========================================================="
arp -a | grep -v "incomplete"

echo ""
echo "Method 2: Check router's DHCP leases (if accessible)"
echo "======================================================"
echo "Login to your router (usually 192.168.1.1 or 192.168.0.1)"
echo "Look for devices named 'JAM', 'Rhythm', 'Symphony', or 'LinkPlay'"

echo ""
echo "Method 3: Try scanning with nmap (if installed)"
echo "================================================"
if command -v nmap &> /dev/null; then
    echo "Scanning for devices with port 8080 open..."
    LOCAL_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
    if [ -n "$LOCAL_IP" ]; then
        NETWORK=$(echo $LOCAL_IP | cut -d. -f1-3)
        echo "Scanning ${NETWORK}.0/24"
        nmap -p 8080 --open ${NETWORK}.0/24 | grep -B 4 "8080/tcp"
    fi
else
    echo "nmap not installed. Install with: brew install nmap"
fi

echo ""
echo "Method 4: Check LinkPlay app pairing page"
echo "=========================================="
echo "Some speakers have a web interface at: http://<speaker-ip>/"
