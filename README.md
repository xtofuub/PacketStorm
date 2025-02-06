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
