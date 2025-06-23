Here's the corrected Python script:

```Python
import psutil
import time

while True:
    cpu_percent = psutil.cpu_percent()
    print(f"CPU usage percentage: {cpu_percent}%")
    time.sleep(2)
```

This script will run indefinitely and print the current CPU usage every 2 seconds.