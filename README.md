# TofuNuke 🚀

**TofuNuke** is a Python script designed to scan and deauthenticate Wi-Fi networks with surgical precision and maximum chaos. Built for penetration testers, security researchers, and chaos enthusiasts, this tool leverages `airodump-ng` and `aireplay-ng` to unleash havoc on wireless networks.

---

## Features ✨

- **Real-Time Network Scanning**: Discover nearby Wi-Fi networks in real-time with detailed information (BSSID, ESSID, Channel).  
- **Selective or Mass Deauth**: Choose to nuke a single network or unleash chaos on all detected networks.  
- **Continuous Deauth**: Keep the deauth attack running indefinitely until manually stopped.  
- **Rich Terminal Interface**: Beautifully formatted output using the `rich` library for maximum visual impact.  
- **NetworkManager Restoration**: Automatically restarts NetworkManager after the attack to restore normal network functionality.  

---

## Installation 🛠️

### Prerequisites
- **Python 3.x**  
- **Aircrack-ng Suite**  
- **Wireless Adapter** (supports monitor mode, e.g., Alfa AWUS036ACH)  

### Steps
1. **Install Dependencies**:  
   ```bash
   sudo apt update
   sudo apt install aircrack-ng
   pip install rich

   ```bash
    git clone https://github.com/tofuubx/packetstorm
    cd packetstorm
   sudo python3 packetstorm.py

Usage 🎯

Select Interface:

   The script will list all available network interfaces. Choose the one you want to use (e.g., wlan0).

Scan Networks:

   The script will scan for nearby Wi-Fi networks for 30 seconds and display them in real-time.

Choose Deauth Mode:

   Option 1: Nuke all networks.

Option 2: Selectively nuke one network.

Launch the Attack:

Sit back and watch the chaos unfold.

Stop the Attack:

Press Ctrl+C to stop the continuous deauth attack.


