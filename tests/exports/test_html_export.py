
from backend.src.exports.html_exporter import export_html
def test_html():
    assert "<html>" in export_html("test")
