import pytest
try:
    import src.feature_3_1769178888 as feature_module
except ImportError:
    pytest.fail('Feature not implemented (ImportError)')

def test_feature_3():
    assert feature_module.feature_func() == 'success'
