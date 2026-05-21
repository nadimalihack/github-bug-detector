
import shutil
def get_disk_usage(path="/"):
    total, used, free = shutil.disk_usage(path)
    return {"total": total, "used": used, "free": free}
