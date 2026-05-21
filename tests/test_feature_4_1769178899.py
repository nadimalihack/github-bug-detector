import pytest
try:
    import src.feature_4_1769178899 as feature_module
except ImportError:
    pytest.fail('Feature not implemented (ImportError)')

def test_feature_4():
    assert feature_module.feature_func() == 'success'
