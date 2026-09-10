import boto3
from moto import mock_aws
from src.ec2_scanner import get_running_instances


@mock_aws
def test_get_running_instances_returns_free_tier_eligible_instance():
    # Given: a fake EC2 environment with one running t2.micro instance
    client = boto3.client("ec2", region_name="us-east-1")
    client.run_instances(ImageId="ami-12345678", MinCount=1, MaxCount=1, InstanceType="t2.micro")

    # When: we scan for running instances
    result = get_running_instances(region="us-east-1")

    # Then: the instance is returned and correctly flagged as Free Tier eligible
    assert len(result) == 1
    assert result[0]["type"] == "t2.micro"
    assert result[0]["is_free_tier_eligible"] is True


@mock_aws
def test_get_running_instances_flags_non_eligible_type():
    # Given: a fake EC2 environment with one running m5.large instance
    client = boto3.client("ec2", region_name="us-east-1")
    client.run_instances(ImageId="ami-12345678", MinCount=1, MaxCount=1, InstanceType="m5.large")

    # When: we scan for running instances
    result = get_running_instances(region="us-east-1")

    # Then: the instance is returned but flagged as NOT Free Tier eligible
    assert len(result) == 1
    assert result[0]["type"] == "m5.large"
    assert result[0]["is_free_tier_eligible"] is False


@mock_aws
def test_get_running_instances_excludes_stopped_instances():
    # Given: a fake EC2 environment with one instance that is then stopped
    client = boto3.client("ec2", region_name="us-east-1")
    response = client.run_instances(ImageId="ami-12345678", MinCount=1, MaxCount=1, InstanceType="t2.micro")
    instance_id = response["Instances"][0]["InstanceId"]
    client.stop_instances(InstanceIds=[instance_id])

    # When: we scan for running instances
    result = get_running_instances(region="us-east-1")

    # Then: the stopped instance should NOT appear in the results
    assert len(result) == 0