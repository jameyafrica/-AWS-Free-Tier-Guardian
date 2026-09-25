import pytest


@pytest.fixture
def safe_ec2_instance():
    return {"id": "i-001", "type": "t2.micro", "region": "us-east-1", "is_free_tier_eligible": True}


@pytest.fixture
def risky_ec2_instance():
    return {"id": "i-002", "type": "m5.large", "region": "us-east-1", "is_free_tier_eligible": False}


@pytest.fixture
def safe_s3_bucket():
    return {"name": "safe-bucket", "size_gb": 1.0, "over_free_tier_limit": False}


@pytest.fixture
def risky_s3_bucket():
    return {"name": "risky-bucket", "size_gb": 10.0, "over_free_tier_limit": True}
