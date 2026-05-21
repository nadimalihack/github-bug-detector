
import csv
import io
def export_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(data.keys())
    writer.writerow(data.values())
    return output.getvalue()
