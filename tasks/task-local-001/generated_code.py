Here is a simple Python script using the `psutil` library, which provides an interface to retrieve various system details such as CPU usage, memory information, etc.

Please note that this will work only on systems with battery (like laptops). For desktops without batteries, it won't show anything meaningful. Also, ensure you have necessary permissions and don't forget to install the required libraries before running this script.

```Python
import psutil

def get_battery_info():
    # Check if we are connected to a battery (laptop)
    battery = psutil.sensors_battery()
    
    if battery is None:
        return "No battery found."

    percent = battery.percent  # Get the battery percentage
    power_left = battery.secsleft  # Get the seconds left on the battery

    return f"Battery: {percent}% ({power_left} seconds remaining)"

print(get_battery_info())
```

You can install the `psutil` library using pip:

```bash
pip install psutil
```

If you are running this script in an environment where it doesn't have access to the necessary permissions or if your system is not a laptop with a battery, it will show "No battery found."