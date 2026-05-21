
import psutil
def get_network_io():
    return psutil.net_io_counters()._asdict()
