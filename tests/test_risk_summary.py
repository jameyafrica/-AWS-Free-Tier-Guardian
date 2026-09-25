from src.risk_summary import calculate_total_risk


def test_zero_risk(safe_ec2_instance, safe_s3_bucket):
    assert calculate_total_risk([safe_ec2_instance], [safe_s3_bucket]) == 0


def test_ec2_only_risk(risky_ec2_instance, safe_s3_bucket):
    assert calculate_total_risk([risky_ec2_instance], [safe_s3_bucket]) == 1


def test_s3_only_risk(safe_ec2_instance, risky_s3_bucket):
    assert calculate_total_risk([safe_ec2_instance], [risky_s3_bucket]) == 1


def test_both_risk(risky_ec2_instance, risky_s3_bucket):
    assert calculate_total_risk([risky_ec2_instance], [risky_s3_bucket]) == 2