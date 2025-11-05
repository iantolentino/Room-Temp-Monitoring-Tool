# 🌡️ ThermoGuard - Device Temperature Monitor

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

A comprehensive real-time temperature monitoring application that protects your device from overheating with instant alerts and detailed temperature tracking.

---

## 🚀 Features

### 🔍 Real-time Monitoring
- **Live Temperature Tracking** - Continuous monitoring of device temperature
- **Visual Status Indicator** - Color-coded alerts (Green → Orange → Red)
- **Temperature History Graph** - Visualize trends over time
- **Auto-refresh** - Configurable update intervals (1-10 seconds)

### ⚠️ Smart Alert System
- **Desktop Notifications** - Pop-up alerts with sound
- **Email Alerts** - Get notified anywhere (Gmail supported)
- **Dual Threshold System** - Separate warning and critical levels
- **Alert Cooldown** - Prevent spam with configurable delays

### 📊 Advanced Features
- **Historical Data** - 5-minute temperature history graph
- **System Information** - CPU and memory usage monitoring
- **Customizable Settings** - Adjust all thresholds and preferences
- **Auto-save** - Settings persist between sessions

---

## 🛠️ Installation

### Prerequisites
- **Python 3.6 or higher**
- **Windows OS** (for best compatibility)

### Step 1: Install Required Packages
```bash
pip install psutil plyer matplotlib
```

### Step 2: Download the Application
Save the Python script as `thermoguard.py`

### Step 3: Run the Application
```bash
python thermoguard.py
```

---

## 📧 Email Setup (Optional but Recommended)

### For Gmail Users:
1. **Enable 2-Factor Authentication**
   - Go to your Google Account settings
   - Navigate to **Security** → **2-Step Verification** → Turn ON

2. **Generate App Password**
   - Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Select **"Mail"** and **"Windows Computer"**
   - Copy the 16-character password

3. **Configure in App**
   - Check "Enable Email Alerts"
   - **Sender Email**: Your Gmail address
   - **App Password**: The 16-character password from step 2
   - **Receiver Email**: Where you want alerts sent
   - Click **"Save Email Settings"**
   - Test with **"Test Email"** button

---

## 🎯 Quick Start Guide

### 1. **Launch the Application**
```bash
python thermoguard.py
```

### 2. **Set Temperature Thresholds**
- **Warning Temperature**: 45°C (recommended)
- **Critical Temperature**: 50°C (recommended)
- Click **"Update Settings"**

### 3. **Enable Monitoring**
- Click **"Start Alert Monitoring"**
- The system will now actively monitor and alert you

### 4. **Configure Email (Optional)**
- Follow the email setup instructions above
- Test with the "Test Email" button

---

## 📖 How to Use

### Main Interface Overview
- **Current Temperature**: Large display with real-time reading
- **Status Indicator**: Color circle shows current status
- **Status Text**: Detailed status message with alert state
- **History Graph**: Visual temperature trends

### Controls Panel
- **Start/Stop Monitoring**: Toggle alert system on/off
- **Refresh Rate**: How often to check temperature (1-10 seconds)
- **Refresh Now**: Manual immediate temperature check

### Temperature Settings
- **Warning Temp**: When to send warning alerts (orange)
- **Critical Temp**: When to send critical alerts (red)
- **Update Settings**: Save your threshold changes

### Email Settings
- **Enable/Disable**: Toggle email alerts
- **SMTP Configuration**: For Gmail use `smtp.gmail.com:587`
- **Test Email**: Verify your email setup works

---

## 🚨 Alert Types

### 🔴 Critical Alerts (Red)
- **Trigger**: Temperature ≥ Critical Threshold
- **Actions**: 
  - Red desktop notification with sound
  - Urgent email alert
  - Visual red status indicator
- **Message**: "CRITICAL TEMPERATURE ALERT!"

### 🟠 Warning Alerts (Orange)
- **Trigger**: Temperature ≥ Warning Threshold
- **Actions**:
  - Orange desktop notification with sound
  - Warning email alert  
  - Visual orange status indicator
- **Message**: "HIGH TEMPERATURE WARNING"

### 🟢 Normal Operation (Green)
- **Status**: Temperature below warning level
- **Display**: Green indicator, normal temperature reading

---

## 💡 Pro Tips

### Optimal Temperature Ranges
- **Normal**: Below 45°C ✅
- **Warning**: 45°C - 50°C ⚠️
- **Critical**: Above 50°C 🚨

### Best Practices
1. **Set realistic thresholds** for your specific hardware
2. **Enable email alerts** for remote monitoring
3. **Use 2-second refresh** for balanced performance
4. **Keep the app running** in background for continuous protection
5. **Check the history graph** to identify temperature patterns

### Troubleshooting
- **No temperature reading?** The app uses simulation mode
- **Email not working?** Verify app password and 2FA settings
- **Notifications silent?** Check Windows notification settings

---

## 🔧 Technical Details

### Supported Platforms
- **Primary**: Windows 10/11
- **Limited**: Linux/macOS (temperature reading may vary)

### Dependencies
- `psutil` - System monitoring and temperature reading
- `plyer` - Cross-platform desktop notifications
- `matplotlib` - Temperature history graphing
- `tkinter` - GUI interface (included with Python)

### Data Storage
- Settings saved in `temperature_monitor_settings.json`
- No internet required (except for email alerts)
- All data stored locally on your device

---

## 🤝 Support

### Common Issues
- **"Missing dependencies"** → Run `pip install psutil plyer matplotlib`
- **"Email login failed"** → Verify app password and 2FA
- **"No temperature sensors"** → App will use simulation mode

### Getting Help
If you encounter issues:
1. Check that all dependencies are installed
2. Verify email settings with "Test Email"
3. Ensure Windows notifications are enabled

---

## 📄 License

This project is licensed under the MIT License - feel free to use and modify for your needs.

---

## 🎉 Enjoy Your Protected System!

With ThermoGuard running, you can work with peace of mind knowing your device is protected from overheating damage. The app will automatically alert you before temperatures reach dangerous levels, giving you time to take preventive action.

**Stay cool!** ❄️

---

*Last Updated: 2024*
