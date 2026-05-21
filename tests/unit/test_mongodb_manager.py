"""
Unit tests for MongoDB manager module
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


class TestMongoDBManager:
    """Test cases for MongoDB manager"""
    
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    def test_init_with_uri(self, mock_client):
        """Test initialization with MongoDB URI"""
        from mongodb_manager import MongoDBManager
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        
        assert manager.uri == "mongodb://localhost:27017"
        mock_client.assert_called_once()
        
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    def test_init_without_uri(self, mock_client):
        """Test initialization without URI"""
        from mongodb_manager import MongoDBManager
        
        with pytest.raises(ValueError):
            MongoDBManager()
            
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_connect_success(self, mock_client):
        """Test successful database connection"""
        from mongodb_manager import MongoDBManager
        
        mock_client.return_value.admin.command = AsyncMock(return_value={"ok": 1})
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        result = await manager.connect()
        
        assert result is True
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_connect_failure(self, mock_client):
        """Test failed database connection"""
        from mongodb_manager import MongoDBManager
        
        mock_client.return_value.admin.command = AsyncMock(side_effect=Exception("Connection failed"))
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        
        with pytest.raises(Exception):
            await manager.connect()
            
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_insert_document(self, mock_client):
        """Test document insertion"""
        from mongodb_manager import MongoDBManager
        
        mock_collection = Mock()
        mock_collection.insert_one = AsyncMock(return_value=Mock(inserted_id="doc_id"))
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        doc_id = await manager.insert_document("test_db", "test_collection", {"key": "value"})
        
        assert doc_id == "doc_id"
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_find_documents(self, mock_client):
        """Test finding documents"""
        from mongodb_manager import MongoDBManager
        
        mock_cursor = Mock()
        mock_cursor.to_list = AsyncMock(return_value=[{"_id": "1", "key": "value"}])
        mock_collection = Mock()
        mock_collection.find.return_value = mock_cursor
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        documents = await manager.find_documents("test_db", "test_collection", {"key": "value"})
        
        assert len(documents) == 1
        assert documents[0]["key"] == "value"
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_find_one_document(self, mock_client):
        """Test finding single document"""
        from mongodb_manager import MongoDBManager
        
        mock_collection = Mock()
        mock_collection.find_one = AsyncMock(return_value={"_id": "1", "key": "value"})
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        document = await manager.find_one_document("test_db", "test_collection", {"key": "value"})
        
        assert document["key"] == "value"
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_update_document(self, mock_client):
        """Test document update"""
        from mongodb_manager import MongoDBManager
        
        mock_collection = Mock()
        mock_collection.update_one = AsyncMock(return_value=Mock(modified_count=1))
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        result = await manager.update_document(
            "test_db", "test_collection",
            {"_id": "1"},
            {"$set": {"key": "new_value"}}
        )
        
        assert result == 1
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_delete_document(self, mock_client):
        """Test document deletion"""
        from mongodb_manager import MongoDBManager
        
        mock_collection = Mock()
        mock_collection.delete_one = AsyncMock(return_value=Mock(deleted_count=1))
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        result = await manager.delete_document("test_db", "test_collection", {"_id": "1"})
        
        assert result == 1
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_count_documents(self, mock_client):
        """Test document counting"""
        from mongodb_manager import MongoDBManager
        
        mock_collection = Mock()
        mock_collection.count_documents = AsyncMock(return_value=10)
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        count = await manager.count_documents("test_db", "test_collection", {})
        
        assert count == 10
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_create_index(self, mock_client):
        """Test index creation"""
        from mongodb_manager import MongoDBManager
        
        mock_collection = Mock()
        mock_collection.create_index = AsyncMock(return_value="index_name")
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        index_name = await manager.create_index("test_db", "test_collection", "field_name")
        
        assert index_name == "index_name"
        
    @pytest.mark.asyncio
    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_aggregate(self, mock_client):
        """Test aggregation pipeline"""
        from mongodb_manager import MongoDBManager
        
        mock_cursor = Mock()
        mock_cursor.to_list = AsyncMock(return_value=[{"count": 5}])
        mock_collection = Mock()
        mock_collection.aggregate.return_value = mock_cursor
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        
        manager = MongoDBManager(uri="mongodb://localhost:27017")
        pipeline = [{"$group": {"_id": "$field", "count": {"$sum": 1}}}]
        results = await manager.aggregate("test_db", "test_collection", pipeline)
        
        assert len(results) == 1
        assert results[0]["count"] == 5
