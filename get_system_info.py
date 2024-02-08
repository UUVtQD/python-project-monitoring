import psutil
import platform
from datetime import datetime

uname = platform.uname()

SYSTEM_HEADER = "System Information"
print(len(SYSTEM_HEADER))

print("="*20, SYSTEM_HEADER, "="*20)
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")