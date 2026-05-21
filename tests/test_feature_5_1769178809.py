import pytest
try:
    import src.feature_5_1769178809 as feature_module
except ImportError:
    pytest.fail('Feature not implemented (ImportError)')

def test_feature_5():
    assert feature_module.feature_func() == 'success'
