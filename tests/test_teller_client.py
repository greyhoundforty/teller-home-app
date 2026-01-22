"""
Tests for Teller API client.
"""
import pytest
from unittest.mock import Mock, patch
from src.teller_client import TellerClient


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"test": "data"}
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def teller_client():
    """Create a TellerClient instance with a test token."""
    return TellerClient(app_token="test_token")


def test_client_initialization():
    """Test client initialization."""
    client = TellerClient(app_token="test_token")
    assert client.app_token == "test_token"
    assert client.BASE_URL == "https://api.teller.io"


def test_client_initialization_without_token():
    """Test client initialization fails without token."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError):
            TellerClient()


@patch('src.teller_client.requests.Session.get')
def test_get_accounts(mock_get, teller_client, mock_response):
    """Test fetching accounts."""
    mock_response.json.return_value = [
        {"id": "acc_123", "name": "Checking"},
        {"id": "acc_456", "name": "Savings"}
    ]
    mock_get.return_value = mock_response
    
    accounts = teller_client.get_accounts()
    
    assert len(accounts) == 2
    assert accounts[0]["id"] == "acc_123"
    mock_get.assert_called_once()


@patch('src.teller_client.requests.Session.get')
def test_get_account(mock_get, teller_client, mock_response):
    """Test fetching a specific account."""
    mock_response.json.return_value = {"id": "acc_123", "name": "Checking"}
    mock_get.return_value = mock_response
    
    account = teller_client.get_account("acc_123")
    
    assert account["id"] == "acc_123"
    assert account["name"] == "Checking"


@patch('src.teller_client.requests.Session.get')
def test_get_account_balances(mock_get, teller_client, mock_response):
    """Test fetching account balances."""
    mock_response.json.return_value = {"available": "1234.56", "ledger": "1234.56"}
    mock_get.return_value = mock_response
    
    balances = teller_client.get_account_balances("acc_123")
    
    assert balances["available"] == "1234.56"
    assert balances["ledger"] == "1234.56"


@patch('src.teller_client.requests.Session.get')
def test_get_transactions(mock_get, teller_client, mock_response):
    """Test fetching transactions."""
    mock_response.json.return_value = [
        {"id": "txn_1", "amount": "-10.50"},
        {"id": "txn_2", "amount": "-25.00"}
    ]
    mock_get.return_value = mock_response
    
    transactions = teller_client.get_transactions("acc_123", count=2)
    
    assert len(transactions) == 2
    assert transactions[0]["id"] == "txn_1"


@patch('src.teller_client.requests.Session.get')
def test_test_connection_success(mock_get, teller_client, mock_response):
    """Test connection test with successful connection."""
    mock_response.json.return_value = []
    mock_get.return_value = mock_response
    
    result = teller_client.test_connection()
    
    assert result is True


@patch('src.teller_client.requests.Session.get')
def test_test_connection_failure(mock_get, teller_client):
    """Test connection test with failed connection."""
    mock_get.side_effect = Exception("Connection error")
    
    result = teller_client.test_connection()
    
    assert result is False
