import psutil
import time
from tabulate import tabulate


def get_network_speed():
    for interface, stats in psutil.net_if_stats().items():
        if stats.isup:
            return stats.speed
    return None


def get_system_usage():
    # Получаем информацию о загрузке CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # Получаем информацию о памяти
    mem = psutil.virtual_memory()
    mem_percent = mem.percent

    # Получаем информацию о дисках
    disk_percent = {}
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disk_percent[partition.mountpoint] = usage.percent

    # Получаем информацию о сети
    net_io_counters = psutil.net_io_counters()
    total_bytes = net_io_counters.bytes_sent + net_io_counters.bytes_recv
    last_total_bytes = getattr(get_system_usage, 'last_total_bytes', total_bytes)
    network_speed = get_network_speed()
    if network_speed is not None and network_speed > 0:
        net_percent = (total_bytes - last_total_bytes) / (network_speed * 1024 * 1024 / 8) * 100
    else:
        net_percent = 0
    get_system_usage.last_total_bytes = total_bytes

    return [cpu_percent, mem_percent] + list(disk_percent.values()) + [net_percent]


def get_workload_info():
    header = ["CPU", "Memory"] + [f"Disk {i}" for i in range(1, len(psutil.disk_partitions()) + 1)] + ["Network"]
    data = [get_system_usage()]
    workload_info = tabulate(data, headers=header, tablefmt="plain")
    return workload_info
