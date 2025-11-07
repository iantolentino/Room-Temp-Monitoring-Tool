import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import psutil
import winsound
from plyer import notification
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

# Configure matplotlib for dark mode
plt.style.use('dark_background')

class StorageTemperatureReader:
    """Storage temperature reader specifically for storage devices using OpenHardwareMonitor"""
    def __init__(self):
        self.wmi_available = False
        self.ohm_available = True
        self.initialize_wmi()
    
    def initialize_wmi(self):
        """Initialize WMI connection and check OpenHardwareMonitor availability"""
        try:
            import wmi
            self.wmi_available = True
            print("✅ WMI support initialized")
            
            # Test if OpenHardwareMonitor is running
            try:
                w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                sensors = w.Sensor()
                self.ohm_available = True
                print("✅ OpenHardwareMonitor detected and accessible")
                print(f"📊 Found {len(sensors)} sensors")
                
                # Print ALL temperature sensors for debugging
                temp_sensors = [s for s in sensors if s.SensorType == "Temperature"]
                print("🌡️ All temperature sensors:")
                for sensor in temp_sensors:
                    print(f"  - {sensor.Name}: {sensor.Value}°C (Parent: {sensor.Parent})")
                    
            except Exception as e:
                print("❌ OpenHardwareMonitor not detected or not running")
                print("💡 Please run OpenHardwareMonitor as Administrator")
                self.ohm_available = False
                
        except ImportError:
            print("❌ WMI not available - install: pip install wmi")
            self.wmi_available = False
            self.ohm_available = False
    
    def _is_storage_sensor(self, sensor_name, parent_name):
        """Check if sensor belongs to a storage device"""
        storage_keywords = [
            'hdd', 'ssd', 'disk', 'drive', 'nvme', 'sata', 
            'hard disk', 'solid state', 'samsung', 'crucial',
            'western digital', 'seagate', 'kingston', 'adata',
            'sandisk', 'intel ssd', 'toshiba', 'hitachi'
        ]
        
        sensor_lower = sensor_name.lower()
        parent_lower = parent_name.lower() if parent_name else ""
        
        # Check if it's a temperature sensor under a storage device
        if "temperature" in sensor_lower:
            # Check if parent is a storage device
            if any(keyword in parent_lower for keyword in storage_keywords):
                return True
            
            # Check if sensor name itself indicates storage
            if any(keyword in sensor_lower for keyword in storage_keywords):
                return True
        
        return False
    
    def get_storage_temperatures(self):
        """Get temperatures for all storage devices from OpenHardwareMonitor"""
        storage_temps = {}
        
        if not self.ohm_available:
            print("❌ OpenHardwareMonitor not available - no temperature data")
            return None
        
        try:
            import wmi
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            sensors = w.Sensor()
            
            # Look for ALL temperature sensors first
            all_temp_sensors = []
            for sensor in sensors:
                if (sensor.SensorType == "Temperature" and 
                    sensor.Value is not None):
                    
                    all_temp_sensors.append({
                        'name': sensor.Name,
                        'value': float(sensor.Value),
                        'parent': sensor.Parent if hasattr(sensor, 'Parent') else "Unknown"
                    })
            
            print(f"🔍 Found {len(all_temp_sensors)} temperature sensors total")
            
            # Filter for storage temperatures
            storage_sensors = []
            for sensor in all_temp_sensors:
                if self._is_storage_sensor(sensor['name'], sensor['parent']):
                    storage_sensors.append(sensor)
                else:
                    print(f"  Skipping non-storage: {sensor['name']} (Parent: {sensor['parent']})")
            
            print(f"💾 Found {len(storage_sensors)} storage temperature sensors")
            
            # Organize storage temperatures
            for sensor in storage_sensors:
                # Use parent name if available, otherwise use sensor name
                if sensor['parent'] and sensor['parent'] != "Unknown":
                    device_name = sensor['parent']
                else:
                    device_name = sensor['name']
                
                # Subtract 10°C from actual reading for room temperature uniformity
                raw_temp = sensor['value']
                adjusted_temp = raw_temp - 10
                storage_temps[device_name] = adjusted_temp
                
                print(f"  {device_name}: {raw_temp}°C -> {adjusted_temp}°C (adjusted -10°C)")
            
            # If we found storage temperatures, return them
            if storage_temps:
                print("📊 Storage temperatures found (adjusted -10°C):")
                for device, temp in storage_temps.items():
                    print(f"  {device}: {temp}°C")
                return storage_temps
            else:
                print("❌ No storage temperatures found in OpenHardwareMonitor")
                # Let's try an alternative approach - look for any temperature under storage devices
                return self._find_storage_temps_alternative(sensors)
            
        except Exception as e:
            print(f"❌ Error reading storage temperatures: {e}")
            self.ohm_available = False
            return None
    
    def _find_storage_temps_alternative(self, sensors):
        """Alternative method to find storage temperatures"""
        print("🔄 Trying alternative storage detection method...")
        storage_temps = {}
        
        # Get all hardware items to find storage devices
        try:
            import wmi
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            hardware_items = w.Hardware()
            
            storage_devices = []
            for hardware in hardware_items:
                hw_name = hardware.Name if hardware.Name else ""
                hw_lower = hw_name.lower()
                
                # Check if this is a storage device
                storage_keywords = ['ssd', 'hdd', 'disk', 'drive', 'samsung', 'crucial', 'wd', 'seagate']
                if any(keyword in hw_lower for keyword in storage_keywords):
                    storage_devices.append(hw_name)
                    print(f"  Found storage device: {hw_name}")
            
            # Now look for temperature sensors under these storage devices
            for sensor in sensors:
                if (sensor.SensorType == "Temperature" and 
                    sensor.Value is not None and
                    hasattr(sensor, 'Parent') and
                    sensor.Parent in storage_devices):
                    
                    # Subtract 10°C from actual reading
                    raw_temp = float(sensor.Value)
                    adjusted_temp = raw_temp - 10
                    storage_temps[sensor.Parent] = adjusted_temp
                    print(f"  Found temperature for {sensor.Parent}: {raw_temp}°C -> {adjusted_temp}°C (adjusted -10°C)")
        
        except Exception as e:
            print(f"❌ Alternative method failed: {e}")
        
        return storage_temps if storage_temps else None
    
    def get_average_storage_temperature(self):
        """Get the average temperature across all storage devices"""
        storage_temps = self.get_storage_temperatures()
        if storage_temps:
            avg_temp = sum(storage_temps.values()) / len(storage_temps)
            print(f"📈 Average storage temperature: {avg_temp:.1f}°C (adjusted)")
            return avg_temp
        else:
            return None
    
    def get_max_storage_temperature(self):
        """Get the maximum temperature among all storage devices"""
        storage_temps = self.get_storage_temperatures()
        if storage_temps:
            max_temp = max(storage_temps.values())
            max_device = max(storage_temps, key=storage_temps.get)
            print(f"🔥 Hottest storage: {max_device} at {max_temp:.1f}°C (adjusted)")
            return max_temp
        else:
            return None
    
    def get_detailed_sensor_info(self):
        """Get detailed information about all available sensors"""
        if not self.wmi_available:
            return "WMI not available"
        
        try:
            import wmi
            info = []
            
            # OpenHardwareMonitor sensors
            if self.ohm_available:
                try:
                    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                    sensors = w.Sensor()
                    info.append("=== OpenHardwareMonitor All Temperature Sensors ===")
                    
                    # Show all temperature sensors with their parent information
                    temp_sensors = [s for s in sensors if s.SensorType == "Temperature" and s.Value is not None]
                    
                    if temp_sensors:
                        for sensor in temp_sensors:
                            parent_info = sensor.Parent if hasattr(sensor, 'Parent') else "No parent"
                            raw_temp = float(sensor.Value)
                            adjusted_temp = raw_temp - 10
                            info.append(f"  {sensor.Name}: {raw_temp}°C -> {adjusted_temp}°C (Parent: {parent_info})")
                    else:
                        info.append("No temperature sensors found")
                        
                except Exception as e:
                    info.append(f"OpenHardwareMonitor error: {e}")
            
            return "\n".join(info) if info else "No sensor information available"
            
        except Exception as e:
            return f"Error getting sensor info: {e}"

class ModernTemperatureMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("ThermoGuard Pro - Storage Temperature Monitor")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Configure dark theme colors
        self.bg_color = "#1e1e1e"
        self.card_bg = "#2d2d2d"
        self.text_color = "#ffffff"
        self.accent_color = "#007acc"
        self.warning_color = "#ffa500"
        self.critical_color = "#ff4444"
        self.success_color = "#44ff44"
        
        # Apply dark theme to root
        self.root.configure(bg=self.bg_color)
        
        # Temperature thresholds (adjusted values - already have -10°C subtracted)
        self.critical_temp = 20  # °C (30-10)
        self.warning_temp = 17   # °C (27-10)
        
        # Monitoring state
        self.is_monitoring = True
        self.alert_monitoring_active = True
        self.monitor_thread = None
        self.email_thread = None
        
        # Alert tracking
        self.last_warning_time = 0
        self.warning_cooldown = 30
        self.last_email_time = 0
        self.last_warning_email_time = 0
        self.last_critical_email_time = 0
        self.email_interval = 3600  # 60 minutes in seconds
        self.warning_email_interval = 60  # 1 minute for warning alerts
        self.critical_email_interval = 60  # 1 minute for critical alerts
        
        # Temperature history for graphing
        self.temp_history = deque(maxlen=50)
        self.time_history = deque(maxlen=50)
        
        # For email statistics
        self.min_temp = float('inf')
        self.max_temp = float('-inf')
        
        # Storage temperatures storage
        self.storage_temperatures = {}
        self.current_status = "NORMAL"
        
        # Storage temperature reader
        self.temp_reader = StorageTemperatureReader()
        
        # Email configuration
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'supercompnxp@gmail.com',
            'sender_password': 'your_app_password_here',  # Set this in your environment
            'receiver_email': 'supercompnxp@gmail.com'
        }
        
        self.load_settings()
        self.setup_modern_ui()
        self.start_realtime_updates()
        self.start_email_scheduler()
        
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('temperature_monitor_settings.json'):
                with open('temperature_monitor_settings.json', 'r') as f:
                    settings = json.load(f)
                    self.critical_temp = settings.get('critical_temp', 20)
                    self.warning_temp = settings.get('warning_temp', 17)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'critical_temp': self.critical_temp,
                'warning_temp': self.warning_temp
            }
            with open('temperature_monitor_settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def setup_modern_ui(self):
        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors for dark theme
        self.style.configure('.', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TLabelframe', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TLabelframe.Label', background=self.card_bg, foreground=self.text_color)
        self.style.configure('TButton', background=self.card_bg, foreground=self.text_color)
        self.style.configure('TCombobox', background=self.card_bg, foreground=self.text_color)
        self.style.configure('TEntry', background=self.card_bg, foreground=self.text_color)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(header_frame, text="🌡️ ThermoGuard Pro", 
                               font=("Arial", 24, "bold"), foreground=self.accent_color)
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(header_frame, text="Storage Temperature Monitoring System", 
                                  font=("Arial", 12), foreground="#888")
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Status card
        status_card = ttk.LabelFrame(main_frame, text="System Status", padding="15")
        status_card.grid(row=1, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Sensor status
        self.sensor_status_var = tk.StringVar()
        sensor_status_label = ttk.Label(status_card, textvariable=self.sensor_status_var,
                                      font=("Arial", 10))
        sensor_status_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Current time
        self.time_var = tk.StringVar(value="Loading...")
        time_label = ttk.Label(status_card, textvariable=self.time_var,
                              font=("Arial", 10), foreground="#888")
        time_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Temperature display card
        temp_card = ttk.LabelFrame(main_frame, text="Temperature Overview", padding="15")
        temp_card.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Storage temperatures display
        storage_frame = ttk.LabelFrame(temp_card, text="Storage Devices", padding="10")
        storage_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Create scrollable frame for storage devices
        storage_canvas = tk.Canvas(storage_frame, height=120, bg=self.card_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(storage_frame, orient="vertical", command=storage_canvas.yview)
        self.scrollable_storage_frame = ttk.Frame(storage_canvas)
        
        self.scrollable_storage_frame.bind(
            "<Configure>",
            lambda e: storage_canvas.configure(scrollregion=storage_canvas.bbox("all"))
        )
        
        storage_canvas.create_window((0, 0), window=self.scrollable_storage_frame, anchor="nw")
        storage_canvas.configure(yscrollcommand=scrollbar.set, bg=self.card_bg)
        
        storage_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        storage_frame.grid_rowconfigure(0, weight=1)
        storage_frame.grid_columnconfigure(0, weight=1)
        
        # Temperature statistics
        stats_frame = ttk.Frame(temp_card)
        stats_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Average temperature
        avg_frame = ttk.Frame(stats_frame)
        avg_frame.grid(row=0, column=0, padx=20)
        ttk.Label(avg_frame, text="Average", font=("Arial", 11)).grid(row=0, column=0)
        self.avg_temp_var = tk.StringVar(value="-- °C")
        self.avg_temp_display = ttk.Label(avg_frame, textvariable=self.avg_temp_var, 
                                         font=("Arial", 16, "bold"))
        self.avg_temp_display.grid(row=1, column=0, pady=5)
        
        # Max temperature
        max_frame = ttk.Frame(stats_frame)
        max_frame.grid(row=0, column=1, padx=20)
        ttk.Label(max_frame, text="Maximum", font=("Arial", 11)).grid(row=0, column=0)
        self.max_temp_var = tk.StringVar(value="-- °C")
        self.max_temp_display = ttk.Label(max_frame, textvariable=self.max_temp_var, 
                                         font=("Arial", 16, "bold"))
        self.max_temp_display.grid(row=1, column=0, pady=5)
        
        # Status indicator
        status_indicator_frame = ttk.Frame(stats_frame)
        status_indicator_frame.grid(row=0, column=2, padx=20)
        ttk.Label(status_indicator_frame, text="Status", font=("Arial", 11)).grid(row=0, column=0)
        self.status_indicator = tk.Canvas(status_indicator_frame, width=40, height=40, bg=self.card_bg, highlightthickness=0)
        self.status_indicator.grid(row=1, column=0, pady=5)
        
        # Status text
        self.status_var = tk.StringVar(value="Initializing...")
        status_label = ttk.Label(stats_frame, textvariable=self.status_var,
                                font=("Arial", 12))
        status_label.grid(row=0, column=3, padx=20)
        
        # Controls card
        controls_card = ttk.LabelFrame(main_frame, text="Monitoring Controls", padding="15")
        controls_card.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Start/Stop buttons
        button_frame = ttk.Frame(controls_card)
        button_frame.grid(row=0, column=0, columnspan=4, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="▶ Start Monitoring", 
                                      command=self.start_alert_monitoring)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹ Stop Monitoring", 
                                     command=self.stop_alert_monitoring, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Refresh controls
        ttk.Label(button_frame, text="Update:").grid(row=0, column=2, padx=(20,5))
        self.refresh_rate_var = tk.StringVar(value="2")
        refresh_combo = ttk.Combobox(button_frame, textvariable=self.refresh_rate_var,
                                    values=["1", "2", "5", "10"], width=5, state="readonly")
        refresh_combo.grid(row=0, column=3, padx=5)
        ttk.Label(button_frame, text="sec").grid(row=0, column=4, padx=(0,10))
        
        # Action buttons
        ttk.Button(button_frame, text="🔄 Refresh Now", 
                  command=self.manual_refresh).grid(row=0, column=5, padx=5)
        
        ttk.Button(button_frame, text="📊 Sensor Info", 
                  command=self.show_sensor_info).grid(row=0, column=6, padx=5)
        
        ttk.Button(button_frame, text="✉️ Test Email", 
                  command=self.send_test_email).grid(row=0, column=7, padx=5)
        
        # Settings card
        settings_card = ttk.LabelFrame(main_frame, text="Temperature Settings", padding="15")
        settings_card.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Warning temperature
        ttk.Label(settings_card, text="Warning Threshold:").grid(row=0, column=0, sticky=tk.W)
        self.warning_var = tk.StringVar(value=str(self.warning_temp))
        warning_entry = ttk.Entry(settings_card, textvariable=self.warning_var, width=8)
        warning_entry.grid(row=0, column=1, padx=5)
        ttk.Label(settings_card, text="°C").grid(row=0, column=2, padx=(0,20))
        
        # Critical temperature
        ttk.Label(settings_card, text="Critical Threshold:").grid(row=0, column=3, sticky=tk.W)
        self.critical_var = tk.StringVar(value=str(self.critical_temp))
        critical_entry = ttk.Entry(settings_card, textvariable=self.critical_var, width=8)
        critical_entry.grid(row=0, column=4, padx=5)
        ttk.Label(settings_card, text="°C").grid(row=0, column=5, padx=(0,20))
        
        # Update settings button
        ttk.Button(settings_card, text="💾 Save Settings", 
                  command=self.update_settings).grid(row=0, column=6, padx=10)
        
        # Information card
        info_card = ttk.LabelFrame(main_frame, text="System Information", padding="15")
        info_card.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Last update
        self.last_update_var = tk.StringVar(value="Last update: --")
        last_update_label = ttk.Label(info_card, textvariable=self.last_update_var,
                                     font=("Arial", 9))
        last_update_label.grid(row=0, column=0, sticky=tk.W)
        
        # Next email report
        self.next_email_var = tk.StringVar(value="Next report: --")
        next_email_label = ttk.Label(info_card, textvariable=self.next_email_var,
                                    font=("Arial", 9))
        next_email_label.grid(row=0, column=1, sticky=tk.W, padx=(20,0))
        
        # Email status
        self.email_status_var = tk.StringVar(value="Email: Ready")
        email_status_label = ttk.Label(info_card, textvariable=self.email_status_var,
                                      font=("Arial", 9))
        email_status_label.grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        
        # Temperature graph
        graph_card = ttk.LabelFrame(main_frame, text="Temperature History", padding="15")
        graph_card.grid(row=6, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure with dark theme
        self.fig, self.ax = plt.subplots(figsize=(10, 4), facecolor=self.card_bg)
        self.ax.set_facecolor(self.card_bg)
        self.ax.tick_params(colors=self.text_color)
        self.ax.xaxis.label.set_color(self.text_color)
        self.ax.yaxis.label.set_color(self.text_color)
        self.ax.title.set_color(self.text_color)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_card)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.update_sensor_status()
    
    def update_sensor_status(self):
        """Update sensor status display"""
        if self.temp_reader.ohm_available:
            status = "✅ Connected to OpenHardwareMonitor • All temperatures adjusted by -10°C"
        else:
            status = "❌ OpenHardwareMonitor not available • Run as Administrator"
        
        self.sensor_status_var.set(status)
    
    def show_sensor_info(self):
        """Show detailed sensor information"""
        info = self.temp_reader.get_detailed_sensor_info()
        messagebox.showinfo("Sensor Information", info)
    
    def start_realtime_updates(self):
        """Start real-time temperature updates immediately"""
        self.is_monitoring = True
        self.update_time_display()
        self.monitor_thread = threading.Thread(target=self.monitor_temperature, daemon=True)
        self.monitor_thread.start()
        
    def start_email_scheduler(self):
        """Start the email scheduler thread"""
        self.email_thread = threading.Thread(target=self.email_scheduler, daemon=True)
        self.email_thread.start()
        
    def update_time_display(self):
        """Update the current time display"""
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_var.set(f'🕒 {current_time}')
        
        # Update next email report time
        next_email_time = self.last_email_time + self.email_interval
        time_until_next = next_email_time - time.time()
        if time_until_next > 0:
            minutes = int(time_until_next // 60)
            seconds = int(time_until_next % 60)
            self.next_email_var.set(f'Next report: {minutes:02d}:{seconds:02d}')
        else:
            self.next_email_var.set('Next report: Now')
            
        self.root.after(1000, self.update_time_display)
        
    def get_system_info(self):
        """Get system usage info"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            return cpu_percent, memory_percent
        except:
            return None, None
    
    def update_status_indicator(self, temperature):
        """Update the status indicator color based on temperature"""
        if temperature is None:
            color = "#666666"  # Gray for no data
            status_color = "#666666"
        elif temperature >= self.critical_temp:
            color = self.critical_color
            status_color = self.critical_color
        elif temperature >= self.warning_temp:
            color = self.warning_color
            status_color = self.warning_color
        else:
            color = self.success_color
            status_color = self.success_color
        
        self.status_indicator.delete("all")
        self.status_indicator.create_oval(5, 5, 35, 35, fill=color, outline=color, width=3)
        
        return status_color
    
    def send_desktop_notification(self, title, message, temp):
        """Send system desktop notification"""
        try:
            notification.notify(
                title=title,
                message=f"{message}\nHottest storage: {temp:.1f}°C",
                timeout=10,
                app_name="ThermoGuard Pro"
            )
            print(f"Desktop notification sent: {title}")
        except Exception as e:
            print(f"Error sending desktop notification: {e}")
        
        # Play sound alert
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        except:
            pass
    
    def send_regular_email_report(self):
        """Send regular monitoring email report"""
        current_max = self.temp_reader.get_max_storage_temperature()
        
        body = f"""
Storage Temperature Monitoring Report
=====================================

Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This automated report provides an overview of the current storage temperature status.

Temperature Statistics (60-Minute Period):
• Current Temperature: {current_max if current_max else 'N/A':.1f}°C
• Minimum Temperature: {self.min_temp if self.min_temp != float('inf') else 'N/A':.1f}°C
• Maximum Temperature: {self.max_temp if self.max_temp != float('-inf') else 'N/A':.1f}°C

System Status Overview:
• Warning Threshold: {self.warning_temp}°C
• Critical Threshold: {self.critical_temp}°C
• Current Status: {self.current_status}

Monitoring Details:
• Device: {os.environ.get('COMPUTERNAME', 'Unknown Device')}
• Report Type: Regular Monitoring Report
• Monitoring Interval: 60 Minutes

This is an automated notification from the Storage Temperature Monitoring System.
No response is required unless immediate action is indicated above.
"""
        
        return self._send_email("Storage Temperature Monitoring Report", body)
    
    def send_warning_email_alert(self, current_max):
        """Send warning temperature alert email"""
        actions = [
            "⚠️ TEMPERATURE WARNING - MONITORING REQUIRED:",
            "• Check ventilation around storage devices",
            "• Monitor temperature trends closely",
            "• Ensure cooling system is functioning properly",
            "• Consider optimizing server load if possible",
            "• Prepare contingency plans if temperature continues to rise"
        ]
        
        body = f"""
🚨 TEMPERATURE WARNING ALERT
============================

Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

URGENT: Storage temperatures have exceeded warning thresholds and require attention.

CRITICAL INFORMATION:
• Current Temperature: {current_max:.1f}°C
• Warning Threshold: {self.warning_temp}°C
• Critical Threshold: {self.critical_temp}°C
• Status: WARNING - Elevated Temperature

IMMEDIATE ACTIONS REQUIRED:
{chr(10).join(actions)}

Device: {os.environ.get('COMPUTERNAME', 'Unknown Device')}

This is an automated WARNING alert from the Storage Temperature Monitoring System.
Continuous monitoring will be performed and updates sent every minute.
"""
        
        return self._send_email("🚨 TEMPERATURE WARNING ALERT", body)
    
    def send_critical_email_alert(self, current_max):
        """Send critical temperature alert email"""
        actions = [
            "🔥 CRITICAL TEMPERATURE ALERT - IMMEDIATE ACTION REQUIRED:",
            "• CHECK COOLING SYSTEM IMMEDIATELY",
            "• REDUCE SERVER LOAD IF POSSIBLE",
            "• ENSURE PROPER VENTILATION AROUND STORAGE DEVICES",
            "• MONITOR TEMPERATURES CONTINUOUSLY",
            "• CONSIDER TEMPORARY SHUTDOWN IF TEMPERATURES CONTINUE TO RISE",
            "• IMPLEMENT EMERGENCY COOLING MEASURES"
        ]
        
        body = f"""
🔥 CRITICAL TEMPERATURE EMERGENCY
=================================

Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EMERGENCY: Storage temperatures have reached CRITICAL levels requiring IMMEDIATE action.

CRITICAL INFORMATION:
• Current Temperature: {current_max:.1f}°C
• Warning Threshold: {self.warning_temp}°C
• Critical Threshold: {self.critical_temp}°C
• Status: CRITICAL - Immediate Intervention Required

EMERGENCY ACTIONS REQUIRED:
{chr(10).join(actions)}

Device: {os.environ.get('COMPUTERNAME', 'Unknown Device')}

This is an automated CRITICAL ALERT from the Storage Temperature Monitoring System.
Continuous monitoring will be performed and updates sent every minute until resolved.
"""
        
        return self._send_email("🔥 CRITICAL TEMPERATURE EMERGENCY", body)
    
    def _send_email(self, subject, body):
        """Send email with given subject and body"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['receiver_email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent: {subject}")
            self.email_status_var.set("Email: Sent ✓")
            self.root.after(5000, lambda: self.email_status_var.set("Email: Ready"))
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            self.email_status_var.set("Email: Failed ✗")
            self.root.after(5000, lambda: self.email_status_var.set("Email: Ready"))
            return False
    
    def send_test_email(self):
        """Send a test email"""
        try:
            success = self.send_regular_email_report()
            if success:
                messagebox.showinfo("Success", "Test email sent successfully!")
            else:
                messagebox.showerror("Error", "Failed to send test email. Check your email configuration.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send test email: {str(e)}")
    
    def email_scheduler(self):
        """Enhanced email scheduler with conditional sending"""
        while self.is_monitoring:
            try:
                current_time = time.time()
                current_max = self.temp_reader.get_max_storage_temperature()
                
                if current_max is not None:
                    # Determine current status
                    if current_max >= self.critical_temp:
                        new_status = "CRITICAL"
                        # Send critical email every minute
                        if current_time - self.last_critical_email_time >= self.critical_email_interval:
                            print("🔥 Sending CRITICAL temperature alert...")
                            self.send_critical_email_alert(current_max)
                            self.last_critical_email_time = current_time
                            self.last_email_time = current_time  # Also update regular email timer
                    
                    elif current_max >= self.warning_temp:
                        new_status = "WARNING"
                        # Send warning email every minute
                        if current_time - self.last_warning_email_time >= self.warning_email_interval:
                            print("⚠️ Sending WARNING temperature alert...")
                            self.send_warning_email_alert(current_max)
                            self.last_warning_email_time = current_time
                            self.last_email_time = current_time  # Also update regular email timer
                    
                    else:
                        new_status = "NORMAL"
                        # Send regular email every 60 minutes
                        if current_time - self.last_email_time >= self.email_interval:
                            print("📧 Sending regular monitoring report...")
                            self.send_regular_email_report()
                            self.last_email_time = current_time
                            
                            # Reset min/max for next period
                            self.min_temp = float('inf')
                            self.max_temp = float('-inf')
                    
                    self.current_status = new_status
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Email scheduler error: {e}")
                time.sleep(60)
    
    def update_storage_display(self):
        """Update the storage devices display"""
        # Clear existing labels
        for widget in self.scrollable_storage_frame.winfo_children():
            widget.destroy()
        
        # Create new labels for each storage device
        if self.storage_temperatures:
            row = 0
            for device_name, temp in self.storage_temperatures.items():
                # Device label
                device_label = ttk.Label(self.scrollable_storage_frame, text=f"💾 {device_name}:", 
                                       font=("Arial", 9))
                device_label.grid(row=row, column=0, padx=5, pady=2, sticky=tk.W)
                
                # Temperature value
                temp_label = ttk.Label(self.scrollable_storage_frame, text=f"{temp:.1f} °C", 
                                     font=("Arial", 9, "bold"))
                temp_label.grid(row=row, column=1, padx=5, pady=2, sticky=tk.W)
                
                row += 1
        else:
            no_data_label = ttk.Label(self.scrollable_storage_frame, text="❌ No storage temperature sensors found", 
                                    font=("Arial", 9), foreground="#ff4444")
            no_data_label.grid(row=0, column=0, padx=5, pady=5)
    
    def update_graph(self):
        """Update the temperature history graph"""
        self.ax.clear()
        
        if len(self.temp_history) > 0:
            time_minutes = [t/60 for t in self.time_history]
            
            self.ax.plot(time_minutes, list(self.temp_history), 'r-', linewidth=2, label='Max Storage Temperature')
            self.ax.axhline(y=self.warning_temp, color='orange', linestyle='--', alpha=0.7, label=f'Warning ({self.warning_temp}°C)')
            self.ax.axhline(y=self.critical_temp, color='red', linestyle='--', alpha=0.7, label=f'Critical ({self.critical_temp}°C)')
            
            self.ax.set_ylabel('Temperature (°C)', color=self.text_color)
            self.ax.set_xlabel('Time (minutes)', color=self.text_color)
            self.ax.set_title('Temperature History Trend', color=self.text_color)
            self.ax.legend(facecolor=self.card_bg, edgecolor=self.text_color, labelcolor=self.text_color)
            self.ax.grid(True, alpha=0.3)
            
            if self.temp_history:
                self.ax.set_ylim(max(0, min(self.temp_history) - 5), max(100, max(self.temp_history) + 10))
        
        self.canvas.draw()
    
    def monitor_temperature(self):
        """Main monitoring loop"""
        start_time = time.time()
        
        while self.is_monitoring:
            try:
                # Get all storage temperatures
                self.storage_temperatures = self.temp_reader.get_storage_temperatures()
                max_temp = self.temp_reader.get_max_storage_temperature()
                avg_temp = self.temp_reader.get_average_storage_temperature()
                cpu_percent, memory_percent = self.get_system_info()
                
                if max_temp is not None:
                    current_time = time.time() - start_time
                    
                    # Update min/max for email reports
                    if max_temp < self.min_temp:
                        self.min_temp = max_temp
                    if max_temp > self.max_temp:
                        self.max_temp = max_temp
                    
                    # Update display immediately
                    self.root.after(0, self.update_display, max_temp, avg_temp, cpu_percent, memory_percent, current_time)
                    
                    # Update history with max temperature
                    self.temp_history.append(max_temp)
                    self.time_history.append(current_time)
                    
                    # Check for alerts only if alert monitoring is active
                    if self.alert_monitoring_active:
                        current_absolute_time = time.time()
                        
                        if max_temp >= self.critical_temp:
                            # Send critical alerts (with cooldown)
                            if current_absolute_time - self.last_warning_time > self.warning_cooldown:
                                self.root.after(0, self.send_desktop_notification,
                                              "🔥 CRITICAL TEMPERATURE ALERT",
                                              "Storage temperature is critically high!",
                                              max_temp)
                                self.last_warning_time = current_absolute_time
                                
                        elif max_temp >= self.warning_temp:
                            # Send warning alerts (with cooldown)
                            if current_absolute_time - self.last_warning_time > self.warning_cooldown:
                                self.root.after(0, self.send_desktop_notification,
                                              "⚠️ HIGH TEMPERATURE WARNING",
                                              "Storage temperature is above normal",
                                              max_temp)
                                self.last_warning_time = current_absolute_time
                else:
                    # No temperature data available
                    current_time = time.time() - start_time
                    self.root.after(0, self.update_display, None, None, None, None, current_time)
                
                # Get refresh rate from UI
                try:
                    refresh_delay = max(1, float(self.refresh_rate_var.get()))
                except:
                    refresh_delay = 2
                    
                time.sleep(refresh_delay)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)
    
    def update_display(self, max_temp, avg_temp, cpu_percent, memory_percent, current_time):
        """Update the UI display with current readings"""
        # Update storage devices display
        self.update_storage_display()
        
        # Update average and max temperatures
        if avg_temp is not None:
            self.avg_temp_var.set(f"{avg_temp:.1f} °C")
        else:
            self.avg_temp_var.set("-- °C")
            
        if max_temp is not None:
            self.max_temp_var.set(f"{max_temp:.1f} °C")
        else:
            self.max_temp_var.set("-- °C")
        
        # Update status indicator and get color
        status_color = self.update_status_indicator(max_temp)
        
        if max_temp is None:
            status_text = "❌ No data - Check OpenHardwareMonitor"
            self.avg_temp_display.config(foreground="#666666")
            self.max_temp_display.config(foreground="#666666")
        elif max_temp >= self.critical_temp:
            status_text = f"🔥 CRITICAL - {max_temp:.1f}°C"
            self.avg_temp_display.config(foreground=self.critical_color)
            self.max_temp_display.config(foreground=self.critical_color)
        elif max_temp >= self.warning_temp:
            status_text = f"⚠️ WARNING - {max_temp:.1f}°C"
            self.avg_temp_display.config(foreground=self.warning_color)
            self.max_temp_display.config(foreground=self.warning_color)
        else:
            status_text = f"✅ NORMAL - {max_temp:.1f}°C"
            self.avg_temp_display.config(foreground=self.success_color)
            self.max_temp_display.config(foreground=self.success_color)
        
        # Add alert status to display
        if self.alert_monitoring_active:
            status_text += " • Alerts ON"
        else:
            status_text += " • Alerts OFF"
            
        self.status_var.set(status_text)
        
        update_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.last_update_var.set(f"Last update: {update_time}")
        
        self.update_graph()
    
    def start_alert_monitoring(self):
        """Start alert monitoring (notifications)"""
        self.alert_monitoring_active = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        messagebox.showinfo("Monitoring Started", "Storage temperature monitoring is now active!\n\nYou will receive notifications and email alerts based on temperature conditions.")
    
    def stop_alert_monitoring(self):
        """Stop alert monitoring (notifications)"""
        self.alert_monitoring_active = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        messagebox.showinfo("Monitoring Stopped", "Storage temperature monitoring is now inactive.")
    
    def manual_refresh(self):
        """Force an immediate temperature refresh"""
        self.storage_temperatures = self.temp_reader.get_storage_temperatures()
        max_temp = self.temp_reader.get_max_storage_temperature()
        avg_temp = self.temp_reader.get_average_storage_temperature()
        cpu_percent, memory_percent = self.get_system_info()
        if max_temp is not None:
            self.update_display(max_temp, avg_temp, cpu_percent, memory_percent, 
                              len(self.time_history) * float(self.refresh_rate_var.get()))
    
    def update_settings(self):
        """Update temperature threshold settings"""
        try:
            new_warning = float(self.warning_var.get())
            new_critical = float(self.critical_var.get())
            
            if new_warning >= new_critical:
                messagebox.showerror("Error", "Warning temperature must be lower than critical temperature")
                return
            
            self.warning_temp = new_warning
            self.critical_temp = new_critical
            self.save_settings()
            
            messagebox.showinfo("Success", "Temperature settings updated successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for temperature thresholds")
    
    def on_closing(self):
        """Clean up when closing the application"""
        self.is_monitoring = False
        self.save_settings()
        self.root.destroy()

def main():
    # Check dependencies
    try:
        import psutil
        from plyer import notification
        # Try to import WMI (required)
        try:
            import wmi
            print("✅ WMI support available")
        except ImportError:
            print("❌ WMI not available - install with: pip install wmi")
            messagebox.showerror("Missing Dependency", "WMI is required for this application.\n\nPlease install it with: pip install wmi")
            return
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install psutil plyer matplotlib wmi")
        messagebox.showerror("Missing Dependencies", f"Missing required packages:\n\nPlease install: pip install psutil plyer matplotlib wmi")
        return
    
    # Create and run the application
    root = tk.Tk()
    app = ModernTemperatureMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()