# 🌡️ ThermoGuard - Real-Time Temperature Monitor
 
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey)

**Protect your computer from overheating with real-time temperature monitoring and instant alerts!**

ThermoGuard is a powerful yet easy-to-use application that continuously monitors your device's temperature and alerts you before it reaches dangerous levels. Perfect for gamers, developers, servers and anyone who wants to protect their hardware.

---

## 🚀 **Quick Start**

### **1. Installation (2 minutes)**
```bash
# Download the script and save as thermoguard.py

# Install required packages
pip install -r requirements.txt

# Or install individually:
pip install psutil plyer matplotlib wmi
```

### **2. Run the Application**
```bash
python thermoguard.py
```

### **3. Enable Real Hardware Monitoring (Recommended)**
1. **Download** [OpenHardwareMonitor](https://openhardwaremonitor.org/downloads/)
2. **Extract** the ZIP file
3. **Run as Administrator**: Right-click `OpenHardwareMonitor.exe` → "Run as administrator"
4. **Keep it running** in the background

**That's it!** ThermoGuard will now show real hardware temperatures.

---

## ✨ **Key Features**

### 🔍 **Real-Time Monitoring**
- **Live Temperature Display** - Large, easy-to-read temperature display
- **Color-Coded Status** - Green (Normal) → Orange (Warning) → Red (Critical)
- **Temperature History Graph** - Visualize trends over 5 minutes
- **Auto-Refresh** - Updates every 1-10 seconds (your choice)

### ⚠️ **Smart Alert System**
- **Desktop Notifications** - Pop-up alerts with sound
- **Email Alerts** - Get notified anywhere (Gmail supported)
- **Dual Threshold System** - Separate warning and critical levels
- **Anti-Spam Protection** - Prevents repeated alerts

### 🛡️ **Hardware Protection**
- **Real Hardware Readings** - Uses OpenHardwareMonitor for accurate temperatures
- **Multiple Sensor Support** - CPU, cores, and system temperatures
- **Automatic Fallbacks** - Works even without special software
- **System Resource Monitoring** - CPU and memory usage

---

## 🎯 **How to Use**

### **Basic Monitoring**
1. **Launch the application**
2. **Set your temperature thresholds:**
   - **Warning**: 45°C (recommended)
   - **Critical**: 50°C (recommended)
3. **Click "Start Alert Monitoring"**
4. **The system will protect your device automatically**

### **Email Alerts Setup (Optional)**
1. **Check "Enable Email Alerts"**
2. **Configure Gmail settings:**
   - **SMTP Server**: `smtp.gmail.com`
   - **Port**: `587`
   - **Sender Email**: Your Gmail address
   - **App Password**: [Get from Google](#-gmail-app-password-setup)
   - **Receiver Email**: Where to send alerts
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

### **Step 3: Use in ThermoGuard**
- **App Password**: Paste the 16-character code
- **Sender Email**: Your full Gmail address

---

## 🖥️ **Interface Guide**

### **Main Display**
- **🌡️ Current Temperature**: Large digital readout
- **🔴 Status Indicator**: Color circle (Green/Orange/Red)
- **📊 Status Text**: Detailed status with alert state
- **🕒 Last Update**: When temperature was last checked

### **Control Panel**
- **▶️ Start/Stop Monitoring**: Toggle alert system
- **⚡ Refresh Rate**: How often to check (1-10 seconds)
- **🔄 Refresh Now**: Manual immediate check
- **📡 Sensor Info**: View detailed hardware information

### **Temperature Settings**
- **⚠️ Warning Temperature**: When to send warnings
- **🔥 Critical Temperature**: When to send critical alerts
- **💾 Update Settings**: Save your preferences

### **Email Settings**
- **📧 Enable/Disable**: Toggle email alerts
- **🔧 Configuration**: SMTP server and credentials
- **✉️ Test Email**: Verify your setup works

---

## 🛠️ **Troubleshooting**

### **Common Issues & Solutions**

#### **❌ "No temperature sensors detected"**
- **Solution**: Install and run OpenHardwareMonitor as Administrator
- **Alternative**: The app will use realistic simulations

#### **❌ Email alerts not working**
- **Solution**: Verify app password and 2-factor authentication
- **Check**: Use "Test Email" button to diagnose

#### **❌ Notifications not showing**
- **Solution**: Check Windows notification settings
- **Windows 10/11**: Settings → System → Notifications → Enable app notifications

#### **❌ "Missing dependencies" error**
- **Solution**: Run: `pip install psutil plyer matplotlib wmi`

### **Sensor Status Meanings**
- **✅ Green Status**: Reading real hardware temperatures
- **🟡 Orange Status**: Using limited built-in sensors
- **🔴 Red Status**: Using simulations (install OpenHardwareMonitor)

---

## 💡 **Pro Tips**

### **Optimal Temperature Ranges**
- **🟢 Normal**: Below 45°C - Everything is fine!
- **🟠 Warning**: 45°C-50°C - Monitor closely
- **🔴 Critical**: Above 50°C - Take action immediately

### **Best Practices**
1. **Run OpenHardwareMonitor as Administrator** for best accuracy
2. **Set realistic thresholds** for your specific hardware
3. **Enable email alerts** for remote monitoring
4. **Use 2-second refresh rate** for balanced performance
5. **Keep the app running** in background for continuous protection

### **Performance Tips**
- The app uses minimal system resources
- Runs efficiently in the background
- Automatic saving of all settings
- No internet required (except for email alerts)

---

## 🔧 **Technical Details**

### **Supported Systems**
- **Windows 7, 8, 10, 11** (full support)
- **Linux/macOS** (limited temperature reading)
- **Python 3.6+** required

### **Temperature Sources (Priority Order)**
1. **OpenHardwareMonitor** (most accurate)
2. **Windows WMI Thermal Zones** (built-in)
3. **psutil Sensors** (limited support)
4. **Realistic Simulation** (always works)

### **Data & Privacy**
- ✅ **All data stored locally**
- ✅ **No internet required** (except email)
- ✅ **No data collection**
- ✅ **Open-source code**
- ✅ **Settings saved in local JSON file**

---

## ❓ **Frequently Asked Questions**

### **Q: Is this software safe?**
**A:** Absolutely! The code is open and uses only trusted libraries. No malware, no data collection.

### **Q: Will it slow down my computer?**
**A:** No, it uses minimal resources (typically <1% CPU).

### **Q: Do I need to keep OpenHardwareMonitor open?**
**A:** Yes, run it as Administrator and keep it open for real temperature readings.

### **Q: Can I use it with other email providers?**
**A:** Yes! Adjust SMTP settings for Outlook (smtp-mail.outlook.com:587) or other providers.

### **Q: What if I don't install OpenHardwareMonitor?**
**A:** The app will use realistic simulations based on CPU usage - still very useful!

---

## 🆘 **Getting Help**

### **Quick Diagnostics**
1. **Check the console window** for detailed error messages
2. **Use "Sensor Info" button** to see available hardware sensors
3. **Test email configuration** with the test button
4. **Verify OpenHardwareMonitor** is running as Administrator

### **Common Error Messages**
- **"WMI not available"** → Run `pip install wmi`
- **"OpenHardwareMonitor not detected"** → Run OHM as Admin
- **"Email login failed"** → Check app password and 2FA

---

## 📄 **License**

This project is licensed under the **MIT License** - feel free to use, modify, and distribute for any purpose.

*ThermoGuard - Because your hardware deserves protection.*
