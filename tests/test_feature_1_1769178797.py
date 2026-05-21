import pytest
try:
    import src.feature_1_1769178797 as feature_module
except ImportError:
    pytest.fail('Feature not implemented (ImportError)')

def test_feature_1():
    assert feature_module.feature_func() == 'success'
