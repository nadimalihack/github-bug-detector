
from backend.src.exports.json_exporter import export_json
def test_json():
    assert export_json({"a": 1}) == '{"a": 1}'
