import pytest
try:
    import src.feature_2_1769178877 as feature_module
except ImportError:
    pytest.fail('Feature not implemented (ImportError)')

def test_feature_2():
    assert feature_module.feature_func() == 'success'
