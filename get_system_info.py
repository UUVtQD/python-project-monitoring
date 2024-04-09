import psutil
import platform
import argparse
import GPUtil
import os
from datetime import datetime

from statistics import mean

TITLE = "hostname,timestamp,cpu,ram,gpu-load,gpu-ram\n"


def current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m")


def write_record(instance_name, output_dir, record):
    target_dir = os.path.join(output_dir, instance_name)
    os.makedirs(target_dir, exist_ok=True)

    timestamp, date_month = current_time()
    file_path = os.path.join(target_dir, f"{date_month}.csv")

    lines = list()
    
    if not os.path.exists(file_path):
        lines.append(TITLE)
        
    hostname = record["hostname"]
    cpu = record["cpu"]
    ram = record["ram"]
    gpu_load = record["gpu-load"]
    gpu_ram = record["gpu-ram"]

    lines.append(f"{hostname},{timestamp},{cpu},{ram},{gpu_load},{gpu_ram}\n")

    with open(file_path, "a+") as fp:
        fp.writelines(lines)
        
def main():
    """
    file format:

    timestamp           | CPU (%) | RAM (%) | GPU load (%) | GPU RAM (%)|
    2024-02-11 00:23:11 | 23.11   | 45.12   | 00.00        | 00.00      |

    timestamp format yyyy-mm-dd HH:MM:SS

    ----

    # instance-name
    # output-dir
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("instance_name", help="The unique name of the instance. They way we define it.")
    parser.add_argument("output_dir", help="The root directory where to put all the logs.")

    args = parser.parse_args()
    print(args)

    instance_name = args.instance_name
    output_dir = args.output_dir

    gpus = GPUtil.getGPUs()
    record = {
        "hostname": args.instance_name,
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "gpu-load": mean([gpu.load * 100 for gpu in gpus]),
        "gpu-ram": mean([gpu.memoryUsed / gpu.memoryTotal * 100 for gpu in gpus]),
    }

    write_record(instance_name, output_dir, record)


if __name__ == "__main__":
    main()