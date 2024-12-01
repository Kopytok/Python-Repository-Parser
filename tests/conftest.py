import pytest
import os


@pytest.fixture(scope="session")
def repo_path():
    return os.environ.get("TEST_REPO_PATH")
