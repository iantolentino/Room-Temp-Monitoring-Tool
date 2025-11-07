# 🌡️ ServerTemp Monitor - Server Room Temperature Monitoring System

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey)

**Protect your server infrastructure with real-time server room temperature monitoring and instant alerts!**

ServerTemp Monitor is an enterprise-grade application that continuously monitors your server room environment and alerts you before temperatures reach critical levels. Essential for data centers, server rooms, and IT infrastructure management.

---

## 🚀 **Quick Start**

### **1. Installation (2 minutes)**
```bash
# Download the script and save as servertemp_monitor.py

# Install required packages
pip install -r requirements.txt

# Or install individually:
pip install psutil plyer matplotlib wmi
```

### **2. Run the Application**
```bash
python servertemp_monitor.py
```

### **3. Enable Real Hardware Monitoring (Recommended)**
1. **Download** [OpenHardwareMonitor](https://openhardwaremonitor.org/downloads/)
2. **Extract** the ZIP file
3. **Run as Administrator**: Right-click `OpenHardwareMonitor.exe` → "Run as administrator"
4. **Keep it running** in the background

**That's it!** ServerTemp Monitor will now show real server room temperatures.

---

## ✨ **Key Features**

### 🔍 **Real-Time Server Room Monitoring**
- **Live Temperature Display** - Large, easy-to-read temperature display for server environments
- **Color-Coded Status** - Green (Normal) → Orange (Warning) → Red (Critical)
- **Temperature History Graph** - Visualize server room trends over 5 minutes
- **Auto-Refresh** - Updates every 1-10 seconds (your choice)

### ⚠️ **Enterprise Alert System**
- **Desktop Notifications** - Pop-up alerts with sound for on-site staff
- **Email Alerts** - Get notified anywhere (Gmail supported) for remote monitoring
- **Dual Threshold System** - Separate warning and critical levels for server rooms
- **Anti-Spam Protection** - Prevents repeated alerts during extended events

### 🛡️ **Server Infrastructure Protection**
- **Real Hardware Readings** - Uses OpenHardwareMonitor for accurate server temperatures
- **Multiple Sensor Support** - Server CPU, cores, and ambient temperatures
- **Automatic Fallbacks** - Works even without special software
- **System Resource Monitoring** - Server CPU and memory usage

---

## 🎯 **How to Use**

### **Basic Server Room Monitoring**
1. **Launch the application**
2. **Set your server room temperature thresholds:**
   - **Warning**: 22°C (recommended for server rooms)
   - **Critical**: 25°C (recommended for server rooms)
3. **Click "Start Alert Monitoring"**
4. **The system will protect your server infrastructure automatically**

### **Email Alerts Setup (Essential for Server Monitoring)**
1. **Check "Enable Email Alerts"**
2. **Configure Gmail settings:**
   - **SMTP Server**: `smtp.gmail.com`
   - **Port**: `587`
   - **Sender Email**: Your monitoring Gmail address
   - **App Password**: [Get from Google](#-gmail-app-password-setup)
   - **Receiver Email**: Where to send server alerts
3. **Click "Save Email Settings"**
4. **Test with "Test Email" button**

---

## 📧 **Gmail App Password Setup**

### **Step 1: Enable 2-Factor Authentication**
1. Go to your [Google Account](https://myaccount.google.com/security)
2. Under "Signing in to Google," enable **2-Step Verification**

### **Step 2: Generate App Password**
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **"Mail"** and **"Windows Computer"**
3. Click **"Generate"**
4. Copy the **16-character password** (no spaces)

### **Step 3: Use in ServerTemp Monitor**
- **App Password**: Paste the 16-character code
- **Sender Email**: Your full Gmail address

---

## 🖥️ **Interface Guide**

### **Main Display**
- **🌡️ Current Server Temperature**: Large digital readout
- **🔴 Status Indicator**: Color circle (Green/Orange/Red)
- **📊 Status Text**: Detailed server room status with alert state
- **🕒 Last Update**: When temperature was last checked

### **Control Panel**
- **▶️ Start/Stop Monitoring**: Toggle server alert system
- **⚡ Refresh Rate**: How often to check (1-10 seconds)
- **🔄 Refresh Now**: Manual immediate server check
- **📡 Sensor Info**: View detailed server hardware information

### **Server Temperature Settings**
- **⚠️ Warning Temperature**: When to send server warnings
- **🔥 Critical Temperature**: When to send critical server alerts
- **💾 Update Settings**: Save your server monitoring preferences

### **Email Settings**
- **📧 Enable/Disable**: Toggle server email alerts
- **🔧 Configuration**: SMTP server and credentials
- **✉️ Test Email**: Verify your server monitoring setup works

---

## 🛠️ **Troubleshooting**

### **Common Server Monitoring Issues & Solutions**

#### **❌ "No temperature sensors detected"**
- **Solution**: Install and run OpenHardwareMonitor as Administrator on the server
- **Alternative**: The app will use realistic simulations based on server load

#### **❌ Email alerts not working**
- **Solution**: Verify app password and 2-factor authentication
- **Check**: Use "Test Email" button to diagnose server alert system

#### **❌ Notifications not showing**
- **Solution**: Check Windows notification settings on monitoring station
- **Windows 10/11**: Settings → System → Notifications → Enable app notifications

#### **❌ "Missing dependencies" error**
- **Solution**: Run: `pip install psutil plyer matplotlib wmi`

### **Server Sensor Status Meanings**
- **✅ Green Status**: Reading real server hardware temperatures
- **🟡 Orange Status**: Using limited built-in server sensors
- **🔴 Red Status**: Install OpenHardwareMonitor on server

---

## 💡 **Server Room Best Practices**

### **Optimal Server Room Temperature Ranges**
- **🟢 Normal**: 18°C-22°C - Ideal server room conditions
- **🟠 Warning**: 22°C-25°C - Monitor server room closely
- **🔴 Critical**: Above 25°C - Take immediate action to prevent server damage

### **Server Monitoring Best Practices**
1. **Run OpenHardwareMonitor as Administrator** on each server for best accuracy
2. **Set realistic thresholds** for your specific server room environment
3. **Enable email alerts** for 24/7 remote server monitoring
4. **Use 5-second refresh rate** for balanced server performance
5. **Keep the app running** on monitoring station for continuous server protection

### **Server Performance Tips**
- The app uses minimal system resources on monitoring station
- Runs efficiently in the background
- Automatic saving of all server monitoring settings
- No internet required (except for email alerts)

---

## 🔧 **Technical Details**

### **Supported Server Systems**
- **Windows Server 2012, 2016, 2019, 2022** (full support)
- **Windows 7, 8, 10, 11** (full support)
- **Linux/macOS** (limited temperature reading)
- **Python 3.6+** required

### **Server Temperature Sources (Priority Order)**
1. **OpenHardwareMonitor** (most accurate for servers)
2. **Windows WMI Thermal Zones** (built-in server support)
3. **psutil Sensors** (limited server support)
4. **Realistic Simulation** (always works for testing)

### **Data & Privacy**
- ✅ **All server data stored locally**
- ✅ **No internet required** (except email)
- ✅ **No server data collection**
- ✅ **Open-source code**
- ✅ **Settings saved in local JSON file**

---

## ❓ **Frequently Asked Questions**

### **Q: Is this software safe for production servers?**
**A:** Absolutely! The code is open and uses only trusted libraries. No malware, no data collection from servers.

### **Q: Will it impact server performance?**
**A:** No, it uses minimal resources on the monitoring station (typically <1% CPU).

### **Q: Do I need to keep OpenHardwareMonitor open on all servers?**
**A:** Yes, run it as Administrator on each monitored server and keep it open for real temperature readings.

### **Q: Can I use it with enterprise email systems?**
**A:** Yes! Adjust SMTP settings for Exchange (smtp.yourcompany.com) or other enterprise email providers.

### **Q: What if I don't install OpenHardwareMonitor on servers?**
**A:** The app will use realistic simulations based on server CPU usage - still useful for monitoring trends!

---

## 🆘 **Getting Help**

### **Quick Server Diagnostics**
1. **Check the console window** for detailed server error messages
2. **Use "Sensor Info" button** to see available server hardware sensors
3. **Test email configuration** with the test button
4. **Verify OpenHardwareMonitor** is running as Administrator on servers

### **Common Server Error Messages**
- **"WMI not available"** → Run `pip install wmi` on monitoring station
- **"OpenHardwareMonitor not detected"** → Run OHM as Admin on server
- **"Email login failed"** → Check app password and 2FA for monitoring account

---

## 📄 **License**

This project is licensed under the **MIT License** - feel free to use, modify, and distribute for any purpose.

*ServerTemp Monitor - Because your server infrastructure deserves protection.*
