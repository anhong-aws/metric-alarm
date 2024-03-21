import pytest
from moto import mock_aws
from sts_manager import STSManager

@pytest.mark.sts
def test_get_assumed_role_credentials():
    # Create an instance of the STSManager class
    sts_manager = STSManager()

    # Define the account ID and role name for testing
    test_account_id = '123456789012'
    test_role = 'TestRole'

    # Call the get_assumed_role_credentials method
    credentials = sts_manager.get_assumed_role_credentials(test_account_id, test_role)

    # Assert that the credentials are returned as a dictionary
    assert isinstance(credentials, dict), "The credentials should be a dictionary."

    # Assert that the dictionary contains the necessary keys
    assert 'AccessKeyId' in credentials, "The credentials should have an AccessKeyId."
    assert 'SecretAccessKey' in credentials, "The credentials should have a SecretAccessKey."
    assert 'SessionToken' in credentials, "The credentials should have a SessionToken."


@pytest.mark.sts_mock
@mock_aws
def test_get_assumed_role_credentials_mock():
    # Mock the assume_role call
    with mock_aws():
        # Create an instance of the STSManager class
        sts_manager = STSManager()

        # Define the account ID and role name for testing
        test_account_id = '123456789012'
        test_role = 'TestRole'
        # Call the get_assumed_role_credentials method
        credentials = sts_manager.get_assumed_role_credentials(test_account_id, test_role)
        print(credentials)
        # Assert that the credentials are returned as a dictionary
        assert isinstance(credentials, dict), "The credentials should be a dictionary."

        # Assert that the dictionary contains the necessary keys
        assert 'AccessKeyId' in credentials, "The credentials should have an AccessKeyId."
        assert 'SecretAccessKey' in credentials, "The credentials should have a SecretAccessKey."
        assert 'SessionToken' in credentials, "The credentials should have a SessionToken."