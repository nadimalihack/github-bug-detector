"""
Unit tests for trainer module
"""
import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


class TestModelTrainer:
    """Test cases for ModelTrainer class"""
    
    def test_init_default_params(self):
        """Test initialization with default parameters"""
        from trainer import ModelTrainer
        
        trainer = ModelTrainer()
        
        assert trainer.model is not None
        assert hasattr(trainer, 'scaler')
        
    def test_prepare_training_data(self, sample_bug_patterns):
        """Test training data preparation"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        
        X, y = trainer.prepare_training_data(df)
        
        assert X.shape[0] == len(sample_bug_patterns)
        assert len(y) == len(sample_bug_patterns)
        assert X.shape[1] > 0
        
    def test_train_model_success(self, sample_bug_patterns):
        """Test successful model training"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        
        result = trainer.train(df)
        
        assert result["success"] is True
        assert "accuracy" in result
        assert result["accuracy"] >= 0
        
    def test_train_model_with_validation_split(self, sample_bug_patterns):
        """Test model training with validation split"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns * 10)  # More data for split
        
        result = trainer.train(df, validation_split=0.2)
        
        assert result["success"] is True
        assert "validation_accuracy" in result
        
    def test_train_model_insufficient_data(self):
        """Test training with insufficient data"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame([{"file": "test.py", "bug_keywords": 1, "has_bug": 0}])
        
        with pytest.raises(ValueError):
            trainer.train(df)
            
    def test_evaluate_model(self, sample_bug_patterns):
        """Test model evaluation"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        trainer.train(df)
        
        X, y = trainer.prepare_training_data(df)
        metrics = trainer.evaluate(X, y)
        
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        
    def test_predict_single_sample(self, sample_bug_patterns):
        """Test prediction on single sample"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        trainer.train(df)
        
        sample = {"bug_keywords": 5, "commit_frequency": 10, "complexity": 0.7}
        prediction = trainer.predict_single(sample)
        
        assert prediction in [0, 1]
        
    def test_predict_probability(self, sample_bug_patterns):
        """Test probability prediction"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        trainer.train(df)
        
        sample = {"bug_keywords": 5, "commit_frequency": 10, "complexity": 0.7}
        probability = trainer.predict_probability(sample)
        
        assert 0 <= probability <= 1
        
    def test_save_model(self, sample_bug_patterns, temp_model_file):
        """Test model saving"""
        from trainer import ModelTrainer
        import pandas as pd
        import os
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        trainer.train(df)
        
        trainer.save_model(temp_model_file)
        
        assert os.path.exists(temp_model_file)
        
    def test_load_model(self, sample_bug_patterns, temp_model_file):
        """Test model loading"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer1 = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        trainer1.train(df)
        trainer1.save_model(temp_model_file)
        
        trainer2 = ModelTrainer()
        trainer2.load_model(temp_model_file)
        
        assert trainer2.model is not None
        
    def test_feature_importance(self, sample_bug_patterns):
        """Test feature importance extraction"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        trainer.train(df)
        
        importance = trainer.get_feature_importance()
        
        assert isinstance(importance, dict)
        assert len(importance) > 0
        
    def test_cross_validation(self, sample_bug_patterns):
        """Test cross-validation"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns * 5)
        
        scores = trainer.cross_validate(df, cv=3)
        
        assert len(scores) == 3
        assert all(0 <= score <= 1 for score in scores)
        
    def test_hyperparameter_tuning(self, sample_bug_patterns):
        """Test hyperparameter tuning"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns * 10)
        
        best_params = trainer.tune_hyperparameters(df)
        
        assert isinstance(best_params, dict)
        
    def test_handle_imbalanced_data(self):
        """Test handling imbalanced dataset"""
        from trainer import ModelTrainer
        import pandas as pd
        
        # Create imbalanced dataset
        data = [{"bug_keywords": i, "commit_frequency": i, "complexity": 0.5, "has_bug": 0} 
                for i in range(20)]
        data.extend([{"bug_keywords": i, "commit_frequency": i, "complexity": 0.8, "has_bug": 1} 
                     for i in range(5)])
        
        trainer = ModelTrainer()
        df = pd.DataFrame(data)
        
        result = trainer.train(df, handle_imbalance=True)
        
        assert result["success"] is True
        
    def test_normalize_features(self, sample_bug_patterns):
        """Test feature normalization"""
        from trainer import ModelTrainer
        import pandas as pd
        import numpy as np
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        
        X, y = trainer.prepare_training_data(df)
        X_normalized = trainer.normalize_features(X)
        
        assert X_normalized.shape == X.shape
        assert np.abs(X_normalized.mean()) < 1
        
    def test_generate_training_report(self, sample_bug_patterns):
        """Test training report generation"""
        from trainer import ModelTrainer
        import pandas as pd
        
        trainer = ModelTrainer()
        df = pd.DataFrame(sample_bug_patterns)
        result = trainer.train(df)
        
        report = trainer.generate_report(result)
        
        assert isinstance(report, str)
        assert len(report) > 0
