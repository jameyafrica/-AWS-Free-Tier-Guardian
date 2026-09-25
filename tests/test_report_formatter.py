from src.report_formatter import format_ec2_table, format_s3_table


def test_format_ec2_table_empty():
    assert format_ec2_table([]) == "Nothing to report — no running EC2 instances."


def test_format_ec2_table_with_data():
    data = [{"id": "i-123", "type": "t2.micro", "region": "us-east-1", "is_free_tier_eligible": True}]
    output = format_ec2_table(data)
    assert "i-123" in output
    assert "Y" in output


def test_format_s3_table_empty():
    assert format_s3_table([]) == "Nothing to report — no S3 buckets found."


def test_format_s3_table_with_data():
    data = [{"name": "my-bucket", "size_gb": 1.23, "over_free_tier_limit": False}]
    output = format_s3_table(data)
    assert "my-bucket" in output
    assert "N" in output