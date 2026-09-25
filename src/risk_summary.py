def calculate_total_risk(ec2_results, s3_results):
    """
    Counts total risky resources: EC2 instances that are NOT
    free-tier-eligible, plus S3 buckets flagged over_free_tier_limit.
    """
    risky_ec2 = sum(1 for instance in ec2_results if not instance["is_free_tier_eligible"])
    risky_s3 = sum(1 for bucket in s3_results if bucket["over_free_tier_limit"])
    return risky_ec2 + risky_s3