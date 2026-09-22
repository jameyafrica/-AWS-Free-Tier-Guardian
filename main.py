from botocore.exceptions import ClientError
from src.ec2_scanner import get_running_instances
from src.s3_scanner import get_bucket_summary
import re
import argparse

print("Guardian starting...")

def valid_region_format(region_string):
    """
    Validates that a region string matches AWS's naming pattern
    (e.g. us-east-1, eu-west-2, ap-southeast-1).
    Raises argparse.ArgumentTypeError on a malformed string, which
    argparse catches and turns into a clean usage error instead of
    a crash.
    """
    pattern = r"^[a-z]{2}-[a-z]+-\d{1}$"
    if not re.match(pattern, region_string):
        raise argparse.ArgumentTypeError(
            f"'{region_string}' is not a valid AWS region format (expected something like 'us-east-1')"
        )
    return region_string   

def build_report(ec2_results, s3_results):
    """
    Combines EC2 and S3 scan results into a single report dict.

    Args:
        ec2_results: list of dicts from get_running_instances()
        s3_results: list of dicts from get_bucket_summary()

    Returns:
        dict with keys "ec2", "s3", and "summary". "summary" contains
        a single int, total_risky_resources: count of EC2 instances
        that are NOT free-tier-eligible, plus S3 buckets flagged
        over_free_tier_limit.
    """
    risky_ec2_count = sum(
        1 for instance in ec2_results
        if not instance["is_free_tier_eligible"]
    )
    risky_s3_count = sum(
        1 for bucket in s3_results
        if bucket["over_free_tier_limit"]
    )

    return {
        "ec2": ec2_results,
        "s3": s3_results,
        "summary": {
            "total_risky_resources": risky_ec2_count + risky_s3_count,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="AWS Free-Tier Guardian")
    parser.add_argument("--region", default="us-east-1", type=valid_region_format)
    args = parser.parse_args()

    try:
        instances = get_running_instances()

        if not instances:
            print("No running EC2 instances found")
        else:
            print(f"Found {len(instances)} running EC2 instance(s):")
            for instance in instances:
                print(f"  - {instance['id']} ({instance['type']}) in {instance['region']} "
                      f"| Free Tier eligible: {instance['is_free_tier_eligible']}")

        buckets = get_bucket_summary()

        if not buckets:
            print("No S3 buckets found")
        else:
            print(f"Found {len(buckets)} S3 bucket(s):")
            for bucket in buckets:
                print(f"  - {bucket['name']} ({bucket['size_gb']} GB, {bucket['object_count']} objects) "
                      f"| Over Free Tier limit: {bucket['over_free_tier_limit']}")

        report = build_report(instances, buckets)
        print(f"\nTotal risky resources: {report['summary']['total_risky_resources']}")

    except ClientError as e:
        print("AWS rejected this request — likely a permissions issue.")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()