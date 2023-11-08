import platform
import psutil
from ..utils import run_command_async


async def get_system_info_full():
    data = {
        'kernel_version': (await run_command_async('uname -r')).strip(),
        'cpu_info': (await run_command_async('lscpu')).strip(),
        'memory_info': (await run_command_async('free -h')).strip(),
        'disk_space': (await run_command_async('df -h')).strip()
    }
    return {'data': data}


async def get_system_info_simple():
    data = {
        'kernel': platform.uname().release,
        'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
        'cpu': platform.processor(),
        'memory': f'Total: {round(psutil.virtual_memory().total / (1024.0 ** 3))} GB, Available: {round(psutil.virtual_memory().available / (1024.0 ** 3))} GB'
    }
    return {'data': data}
