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

class TemperatureMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Temperature Monitor")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Temperature thresholds
        self.critical_temp = 85  # °C
        self.warning_temp = 75   # °C
        self.normal_temp = 60    # °C
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Temperature history for graphing
        self.temp_history = deque(maxlen=50)
        self.time_history = deque(maxlen=50)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Device Temperature Monitor", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Temperature display
        self.temp_var = tk.StringVar(value="Current Temperature: -- °C")
        temp_label = ttk.Label(main_frame, textvariable=self.temp_var, 
                              font=("Arial", 14))
        temp_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Status display
        self.status_var = tk.StringVar(value="Status: Not Monitoring")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                font=("Arial", 12))
        status_label.grid(row=2, column=0, columnspan=3, pady=5)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Start/Stop buttons
        self.start_button = ttk.Button(controls_frame, text="Start Monitoring", 
                                      command=self.start_monitoring)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(controls_frame, text="Stop Monitoring", 
                                     command=self.stop_monitoring, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Temperature Settings (°C)", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Warning temperature
        ttk.Label(settings_frame, text="Warning Temp:").grid(row=0, column=0, sticky=tk.W)
        self.warning_var = tk.StringVar(value=str(self.warning_temp))
        warning_entry = ttk.Entry(settings_frame, textvariable=self.warning_var, width=8)
        warning_entry.grid(row=0, column=1, padx=5)
        
        # Critical temperature
        ttk.Label(settings_frame, text="Critical Temp:").grid(row=0, column=2, padx=(20,0))
        self.critical_var = tk.StringVar(value=str(self.critical_temp))
        critical_entry = ttk.Entry(settings_frame, textvariable=self.critical_var, width=8)
        critical_entry.grid(row=0, column=3, padx=5)
        
        # Update settings button
        ttk.Button(settings_frame, text="Update Settings", 
                  command=self.update_settings).grid(row=0, column=4, padx=10)
        
        # Temperature graph
        graph_frame = ttk.LabelFrame(main_frame, text="Temperature History", padding="10")
        graph_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def get_temperature(self):
        """Get current temperature using psutil"""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if entry.current:  # Only use if current temperature is available
                                return entry.current
            # Fallback: Return a simulated temperature for demonstration
            return self.simulate_temperature()
        except Exception as e:
            print(f"Error getting temperature: {e}")
            return None
    
    def simulate_temperature(self):
        """Simulate temperature readings for demonstration"""
        import random
        # Simulate normal temperature with occasional spikes
        base_temp = 45
        spike_chance = random.random()
        
        if spike_chance > 0.95:  # 5% chance of critical spike
            return random.uniform(85, 95)
        elif spike_chance > 0.85:  # 10% chance of warning spike
            return random.uniform(75, 85)
        else:
            return random.uniform(40, 70)
    
    def send_notification(self, title, message, temp):
        """Send system notification"""
        try:
            notification.notify(
                title=title,
                message=f"{message}\nCurrent temperature: {temp:.1f}°C",
                timeout=10,
                app_name="Temperature Monitor"
            )
        except Exception as e:
            print(f"Error sending notification: {e}")
        
        # Also play a sound alert
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        except:
            pass
    
    def update_graph(self):
        """Update the temperature history graph"""
        self.ax.clear()
        
        if len(self.temp_history) > 0:
            self.ax.plot(list(self.time_history), list(self.temp_history), 'b-', linewidth=2)
            self.ax.axhline(y=self.warning_temp, color='orange', linestyle='--', label=f'Warning ({self.warning_temp}°C)')
            self.ax.axhline(y=self.critical_temp, color='red', linestyle='--', label=f'Critical ({self.critical_temp}°C)')
            
            self.ax.set_ylabel('Temperature (°C)')
            self.ax.set_xlabel('Time (seconds)')
            self.ax.set_title('Temperature Over Time')
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)
            
            # Set y-axis limits
            self.ax.set_ylim(0, max(100, max(self.temp_history) + 10))
        
        self.canvas.draw()
    
    def monitor_temperature(self):
        """Main monitoring loop"""
        start_time = time.time()
        last_warning_time = 0
        warning_cooldown = 30  # seconds between repeated warnings
        
        while self.is_monitoring:
            try:
                current_temp = self.get_temperature()
                
                if current_temp is not None:
                    # Update display
                    self.temp_var.set(f"Current Temperature: {current_temp:.1f} °C")
                    
                    # Update history
                    current_time = time.time() - start_time
                    self.temp_history.append(current_temp)
                    self.time_history.append(current_time)
                    
                    # Check temperature thresholds
                    if current_temp >= self.critical_temp:
                        self.status_var.set(f"Status: CRITICAL - {current_temp:.1f}°C")
                        self.root.config(bg='#ffcccc')  # Light red background
                        
                        # Send critical notification (with cooldown)
                        if current_time - last_warning_time > warning_cooldown:
                            self.send_notification(
                                "🔥 CRITICAL TEMPERATURE ALERT!",
                                "Device temperature is critically high!",
                                current_temp
                            )
                            last_warning_time = current_time
                            
                    elif current_temp >= self.warning_temp:
                        self.status_var.set(f"Status: WARNING - {current_temp:.1f}°C")
                        self.root.config(bg='#fff4cc')  # Light yellow background
                        
                        # Send warning notification (with cooldown)
                        if current_time - last_warning_time > warning_cooldown:
                            self.send_notification(
                                "⚠️ HIGH TEMPERATURE WARNING",
                                "Device temperature is above normal",
                                current_temp
                            )
                            last_warning_time = current_time
                            
                    else:
                        self.status_var.set(f"Status: Normal - {current_temp:.1f}°C")
                        self.root.config(bg='SystemButtonFace')  # Default background
                    
                    # Update graph
                    self.update_graph()
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)
    
    def start_monitoring(self):
        """Start the temperature monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_var.set("Status: Monitoring Started")
            
            # Start monitoring in a separate thread
            self.monitor_thread = threading.Thread(target=self.monitor_temperature, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop the temperature monitoring"""
        self.is_monitoring = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_var.set("Status: Monitoring Stopped")
        self.root.config(bg='SystemButtonFace')
    
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
            
            messagebox.showinfo("Success", "Temperature settings updated successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for temperature thresholds")

def main():
    # Check dependencies
    try:
        import psutil
        from plyer import notification
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install psutil plyer")
        return
    
    # Create and run the application
    root = tk.Tk()
    app = TemperatureMonitor(root)
    root.mainloop()

if __name__ == "__main__":
    main()