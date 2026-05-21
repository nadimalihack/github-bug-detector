
from backend.src.exports.csv_exporter import export_csv
def test_csv():
    assert "a" in export_csv({"a": 1})
