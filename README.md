# SysTrack_Pro

> A comprehensive, cross-platform system monitoring toolkit built with Python — delivering real-time hardware metrics, network diagnostics, process tracking, and automated alerting from a single unified interface.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/RaksithSivakumar/systrack_pro)
[![Issues](https://img.shields.io/github/issues/RaksithSivakumar/systrack_pro)](https://github.com/RaksithSivakumar/systrack_pro/issues)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Module Reference](#module-reference)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Known Limitations](#known-limitations)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Overview

SysTrack_Pro is a Python-based system monitoring solution designed for IT professionals, developers, and power users who need granular visibility into their machine's performance. It collects and surfaces metrics across CPU, GPU, memory, disk, battery, network, and active processes — and can persist data to a local SQLite database for trend analysis and historical reporting.

---

## Features

| Category | Capability |
|---|---|
| **CPU** | Physical/logical core counts, per-core usage, clock frequency (min/max/current), temperature via OpenHardwareMonitor (Windows) |
| **GPU** | Temperature and utilization via GPUtil (NVIDIA); Intel/AMD GPU info via platform-native commands |
| **Memory & Disk** | Drive-by-drive space breakdown, I/O read/write counters, real-time disk usage percentage |
| **Battery** | Charge percentage, plug-in status, low-battery desktop notifications via `plyer` |
| **Network** | Interface enumeration, IP addresses, bytes sent/received, internet connectivity check, download/upload speed test |
| **Active Window** | Foreground window title tracking, real-time keystroke logging (for authorized audit use) |
| **Security** | Installed antivirus software detection via Windows Registry scan |
| **Browser History** | Chrome browsing history extraction with timestamps (local profile only) |
| **System Info** | OS version, hostname, machine architecture, boot time, system uptime |
| **Bluetooth** | Connected Bluetooth device enumeration (Windows) |
| **Persistence** | SQLite database logging of CPU metrics for historical analysis |
| **Notifications** | Desktop alerts for configurable threshold events |

---

## Architecture

```
systrack_pro/
├── main.py                  # Entry point — orchestrates all monitoring modules
├── requirements.txt         # Python dependency manifest
├── system_monitor.db        # SQLite database (auto-created on first run)
└── modules/
    ├── cpu.py               # CPU info, frequency, usage, temperature
    ├── gpu.py               # GPU info and temperature
    ├── battery.py           # Battery status and notifications
    ├── network.py           # Network interfaces, I/O, speed test
    ├── disk.py              # Disk partitions, usage, I/O counters
    ├── display.py           # Screen resolution via screeninfo
    ├── window_monitor.py    # Active window and keystroke tracking
    ├── security.py          # Antivirus detection via Windows Registry
    ├── bluetooth.py         # Bluetooth device listing
    ├── browser_history.py   # Chrome history extraction
    └── db.py                # SQLite persistence layer
```

---

## Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows 10/11 (primary); Linux and macOS supported for select modules
- **GPU Temperature:** NVIDIA GPU required for `GPUtil`; Intel GPU info uses platform-native tools
- **CPU Temperature (Windows):** [OpenHardwareMonitor](https://openhardwaremonitor.org/) must be running

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/RaksithSivakumar/systrack_pro.git
cd systrack_pro
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python main.py
```

> **Note:** On Windows, some features (registry access, window monitoring) require running as Administrator.

---

## Usage

Running `main.py` executes the full monitoring suite in sequence and prints results to stdout. It also persists CPU data to the local SQLite database.

```bash
python main.py
```

**Example output (CPU section):**

```
======================================== System Information ========================================
System: Windows
Node Name: DESKTOP-ABC123
Release: 10
Version: 10.0.19045
Machine: AMD64
Processor: Intel64 Family 6 Model 142 Stepping 10, GenuineIntel

======================================== CPU Info ========================================
Physical cores: 4
Total cores: 8
Max Frequency: 1800.00Mhz
Min Frequency: 400.00Mhz
Current Frequency: 1267.00Mhz
CPU Usage Per Core:
  Core 0: 12.5%
  Core 1: 8.3%
  ...
Total CPU Usage: 15.2%
```

To monitor a specific component only, import and call individual functions:

```python
from main import cpu, battery, check_internet_speed

cpu()
battery()
check_internet_speed()
```

---

## Module Reference

### `cpu()`
Prints system info, boot time, core counts, frequency details, and per-core CPU usage.

### `get_cpu_temperature()`
Returns CPU core temperature (Windows only; requires OpenHardwareMonitor running).

### `get_intel_gpu_info()`
Retrieves GPU info using platform-native commands (`wmic` on Windows, `lshw` on Linux, `system_profiler` on macOS).

### `get_gpu_temperature()`
Returns GPU temperature using `GPUtil` (requires NVIDIA GPU on Windows).

### `battery()`
Prints battery percentage and charging status; triggers a desktop notification if battery is low.

### `is_internet_on()`
Returns `True` if a connection to `8.8.8.8:53` can be established within 5 seconds.

### `check_internet_speed()`
Runs a Speedtest and prints download/upload speeds in Mbps.

### `disk_usage()`
Prints total, used, and free disk space with percentage.

### `get_drive_space()` / `given_drive()`
Enumerates all disk partitions and prints per-drive space details.

### `get_disk_io()`
Prints cumulative disk read/write totals in GB.

### `get_network_info()`
Lists all network interfaces and their IP addresses.

### `get_network_io()`
Prints cumulative bytes sent and received in GB.

### `screen_size()`
Prints the resolution of all connected monitors.

### `get_active_window_title()`
Returns the title of the currently focused window (Windows only).

### `monitor_active_window()`
Continuously prints the active window title and logs keystrokes. Press `Esc` to stop.

### `get_antivirus_software()`
Scans the Windows Registry for installed antivirus programs and prints their names.

### `get_bt_devices()`
Lists connected Bluetooth devices (Windows only; relies on window title heuristics).

### `get_system_uptime()`
Prints the system boot timestamp.

### `print_chrome_history()`
Reads and prints Chrome browsing history from the local user profile database.

### `insert_cpu_data()`
Persists a snapshot of CPU metrics to the `system_monitor.db` SQLite database.

---

## Database Schema

SysTrack_Pro logs CPU metrics to a local SQLite database (`system_monitor.db`).

**Table: `cpu`**

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Auto-increment row ID |
| `physical_cores` | INTEGER | Number of physical CPU cores |
| `total_cores` | INTEGER | Total logical cores (includes HT) |
| `max_frequency` | REAL | Maximum CPU frequency (MHz) |
| `min_frequency` | REAL | Minimum CPU frequency (MHz) |
| `current_frequency` | REAL | Current CPU frequency (MHz) |
| `total_cpu_usage` | REAL | Aggregate CPU usage percentage |
| `timestamp` | DATETIME | Record insertion time (default: now) |

---

## Configuration

SysTrack_Pro does not currently use an external config file. Thresholds and paths are set directly in `main.py`. Key values to customise:

| Variable / Location | Default | Purpose |
|---|---|---|
| `show_notification()` — `app_name` | `'Battery Monitor'` | Notification sender label |
| `is_internet_on()` — host | `8.8.8.8` | Host used for connectivity check |
| Chrome history path | `~\AppData\Local\Google\Chrome\User Data\Default` | Chrome profile location |
| `system_monitor.db` | Project root | SQLite database path |

---

## Known Limitations

- **Windows-first:** Active window tracking, antivirus detection, Bluetooth enumeration, and CPU temperature monitoring are Windows-only. Linux and macOS stubs exist but are not fully implemented.
- **Chrome history access:** Chrome must be closed (or the `History` file unlocked) before querying, as SQLite cannot read a locked file.
- **Bluetooth detection:** Uses window title heuristics via `pygetwindow`, which is fragile and may not reliably detect all devices.
- **`datetime` import conflict:** The codebase imports both `datetime` (module) and `datetime.datetime` (class) — this causes a `NameError` on `datetime.fromtimestamp()`. Use `datetime.datetime.fromtimestamp()` consistently.
- **NVIDIA GPU only:** `GPUtil` only supports NVIDIA GPUs. Intel/AMD temperature monitoring requires additional tooling.

---

## Contributing

Contributions are welcome. Please follow this workflow:

1. Fork the repository on GitHub.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and add tests where applicable.
4. Ensure your code passes existing tests and follows PEP 8 style.
5. Open a Pull Request with a clear description of the change and its motivation.

Please open an issue first for significant changes so the approach can be discussed before implementation.

---

## Contact

**Raksith**
- Email: [risivandev@gmail.com](mailto:risivandev@gmail.com)
- GitHub Issues: [Open an issue](https://github.com/RaksithSivakumar/systrack_pro/issues)

---

*SysTrack_Pro — Know your system, in real time.*
