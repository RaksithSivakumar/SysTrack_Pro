import psutil
import platform
import datetime
from plyer import notification
import socket
import speedtest
from screeninfo import get_monitors
import os
import ctypes
import subprocess
import win32gui
import winreg
import pygetwindow as gw
import serial.tools.list_ports
import keyboard
import cpuinfo
import GPUtil

def get_size(bytes, suffix="B"):
    """ Scale bytes to its proper format e.g: 1253656 => '1.20MB' 1253656678 => '1.17GB' """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='Battery Monitor',
    )
def insert_cpu_data():
    conn = sqlite3.connect('system_monitor.db')
    cursor = conn.cursor()

    # Insert CPU data
    cpufreq = psutil.cpu_freq()
    cursor.execute('''
        INSERT INTO cpu (physical_cores, total_cores, max_frequency, min_frequency, current_frequency, total_cpu_usage)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (psutil.cpu_count(logical=False), psutil.cpu_count(logical=True), cpufreq.max, cpufreq.min, cpufreq.current, psutil.cpu_percent()))

    conn.commit()
    conn.close()

def cpu():
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

    print("="*40, "Boot Time", "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)  # Change this line
    print("Boot Time:", bt)


    print("=" * 40, "CPU Info", "=" * 40)
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))

    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")

    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

def get_intel_gpu_info():
    try:
        system_platform = platform.system().lower()

        if system_platform == "windows":
            command = ["wmic", "path", "win32_videocontroller", "get", "*"]
            output = subprocess.check_output(command, text=True)
            print(output)

        elif system_platform == "linux":
            command = ["lshw", "-C", "display"]
            output = subprocess.check_output(command, text=True)
            print(output)

        elif system_platform == "darwin":
            command = ["system_profiler", "SPDisplaysDataType"]
            output = subprocess.check_output(command, text=True)
            print(output)

        else:
            print("Unsupported platform.")

    except Exception as e:
        print(f"Error getting Intel GPU information: {e}")

def battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    power_plugged = battery.power_plugged
    print(f"Battery Percentage: {percent}%")
    print(f"Is Plugged In: {power_plugged}")

def is_internet_on():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def check_internet_speed():
    if is_internet_on():
        try:
            st = speedtest.Speedtest()
            st.get_best_server()  # Correct method name
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000
            print(f"Download Speed: {download_speed:.2f} Mbps")
            print(f"Upload Speed: {upload_speed:.2f} Mbps")
        except speedtest.ConfigRetrievalError as e:
            print(f"Error retrieving Speedtest configuration: {e}")
        except Exception as e:
            print(f"Error checking speed: {e}")
    else:
        print("Internet is not available.")


def disk_usage():
    disk_usage = psutil.disk_usage('/')
    print(f"Total Disk Space: {get_size(disk_usage.total)}")
    print(f"Used Disk Space: {get_size(disk_usage.used)}")
    print(f"Free Disk Space: {get_size(disk_usage.free)}")
    print(f"Disk Usage Percentage: {disk_usage.percent}%")

def screen_size():
    monitors = get_monitors()
    for monitor in monitors:
        print(f"Screen Resolution: {monitor.width}x{monitor.height}")

def get_drive_space():
    drive_info = []
    for partition in psutil.disk_partitions():
        drive_letter = partition.device
        drive_name = partition.mountpoint
        try:
            drive_usage = psutil.disk_usage(drive_name)
            total_space_gb = drive_usage.total / (1024 ** 3)
            used_space_gb = drive_usage.used / (1024 ** 3)
            drive_info.append({
                'drive_letter': drive_letter,
                'drive_name': drive_name,
                'total_space_gb': total_space_gb,
                'used_space_gb': used_space_gb
            })
        except Exception as e:
            print(f"Error getting information for {drive_name}: {e}")

    return drive_info

def given_drive():
    drive_info = get_drive_space()
    for drive in drive_info:
        print(f"Drive {drive['drive_letter']} ({drive['drive_name']}):")
        print(f"  Total Space: {drive['total_space_gb']:.2f} GB")
        print(f"  Used Space: {drive['used_space_gb']:.2f} GB")
        print()

def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        return window_title if window_title else "None"
    except Exception as e:
        print(f"Error getting active window title: {e}")

def monitor_active_window():
    print("Monitoring active window. Press 'Esc' to exit.")

    while True:
        window_title = get_active_window_title()
        print(f"Active Window: {window_title}")

        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            print(f"Key Pressed: {event.name}")

        if event.name == "esc":
            print("Exiting the window monitor.")
            break

def get_antivirus_software():
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)

        antivirus_count = 0

        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            subkey_path = f"{key_path}\\{subkey_name}"

            try:
                subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)

                try:
                    display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                    print(f"Antivirus: {display_name}")
                    antivirus_count += 1
                except FileNotFoundError:
                    pass

                winreg.CloseKey(subkey)

            except Exception as e:
                print(f"Error accessing registry subkey: {e}")

        winreg.CloseKey(key)

        print(f"Total Antivirus Programs: {antivirus_count}")

    except Exception as e:
        print(f"Error accessing registry: {e}")

def get_bt_devices():
    devices = gw.getWindowsWithTitle("Bluetooth Device")

    if not devices:
        print("No Bluetooth devices found.")
        return

    print("Connected Bluetooth Devices:")
    print("Device Name\t\tDevice Address")

    for device in devices:
        device_info = device.title.split('-')
        device_name = device_info[0].strip()
        device_address = device_info[1].strip()
        print(f"{device_name}\t\t{device_address}")

def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing command: {e}"


def get_cpu_temperature():
    try:
        if platform.system() == "Windows":
            import wmi
            w = wmi.WMI(namespace="root/OpenHardwareMonitor")
            temperature_infos = w.Sensor()
            cpu_temperature = next((sensor.Value for sensor in temperature_infos if sensor.Name == "CPU Core"), None)
            if cpu_temperature:
                return f"CPU Temperature: {cpu_temperature}°C"
        elif platform.system() == "Linux":
            pass
        elif platform.system() == "Darwin":
            pass
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")
    return "CPU Temperature: N/A"

def get_gpu_temperature():
    try:
        if platform.system() == "Windows":
            gpu = GPUtil.getGPUs()[0]
            return f"GPU Temperature: {gpu.temperature}°C"
        elif platform.system() == "Linux":
            pass
        elif platform.system() == "Darwin":
            pass
    except Exception as e:
        print(f"Error getting GPU temperature: {e}")
    return "GPU Temperature: N/A"

def get_network_info():
    try:
        interfaces = psutil.net_if_addrs()
        for iface, addrs in interfaces.items():
            print(f"Network Interface: {iface}")
            for addr in addrs:
                print(f"  - {addr.family.name}: {addr.address}")
    except Exception as e:
        print(f"Error getting network information: {e}")


def get_disk_io():
    try:
        disk_io = psutil.disk_io_counters()
        print(f"Read Bytes: {disk_io.read_bytes / (1024 ** 3):.2f} GB")
        print(f"Write Bytes: {disk_io.write_bytes / (1024 ** 3):.2f} GB")
    except Exception as e:
        print(f"Error getting disk I/O information: {e}")

def get_network_io():
    try:
        net_io = psutil.net_io_counters()
        print(f"Bytes Sent: {net_io.bytes_sent / (1024 ** 3):.2f} GB")
        print(f"Bytes Received: {net_io.bytes_recv / (1024 ** 3):.2f} GB")
    except Exception as e:
        print(f"Error getting network I/O information: {e}")

def get_system_uptime():
    try:
        uptime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        print(f"System Uptime: {uptime}")
    except Exception as e:
        print(f"Error getting system uptime: {e}")

import sqlite3
from datetime import datetime, timedelta
import os

def get_chrome_history():
    try:
        # Get the user's profile directory
        profile_dir = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default')

        # Check if the 'History' file exists
        history_db_path = os.path.join(profile_dir, 'History')
        if not os.path.exists(history_db_path):
            raise FileNotFoundError("Chrome history database not found.")

        # Connect to the database
        connection = sqlite3.connect(history_db_path)
        cursor = connection.cursor()

        # Query to retrieve history data
        query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC"

        # Execute the query
        cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

        # Close the connection
        connection.close()

        return results

    except sqlite3.Error as e:
        print(f"Error accessing Chrome history: {e}")
        return None
    except FileNotFoundError as e:
        print(e)
        return None

def print_chrome_history():
    history = get_chrome_history()

    if history:
        print("="*40, "Chrome History", "="*40)
        for url, title, last_visit_time in history:
            last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
            print(f"URL: {url}")
            print(f"Title: {title}")
            print(f"Last Visit Time: {last_visit_time}")
            print("-" * 80)
    else:
        print("Failed to retrieve Chrome history.")


def system_monitor_active_window():
    cpu()
    get_intel_gpu_info()
    battery()
    check_internet_speed()
    get_drive_space()
    given_drive()
    get_active_window_title()
    monitor_active_window()
    get_antivirus_software()
    get_bt_devices()
    get_network_info()
    get_disk_io()
    get_network_io()
    get_system_uptime()
    print_chrome_history()

system_monitor_active_window()
