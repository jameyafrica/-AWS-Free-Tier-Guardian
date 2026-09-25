import sys
from botocore.exceptions import ClientError, NoCredentialsError
from src.ec2_scanner import get_running_instances
from src.s3_scanner import get_bucket_summary
from src.report_formatter import format_ec2_table, format_s3_table
from src.risk_summary import calculate_total_risk
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
    """
    total_risk = calculate_total_risk(ec2_results, s3_results)

    return {
        "ec2": ec2_results,
        "s3": s3_results,
        "summary": {
            "total_risky_resources": total_risk,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="AWS Free-Tier Guardian")
    parser.add_argument("--region", default="us-east-1", type=valid_region_format)
    args = parser.parse_args()

    try:
        instances = get_running_instances()
        print(format_ec2_table(instances))

        buckets = get_bucket_summary()
        print(format_s3_table(buckets))

        report = build_report(instances, buckets)
        total_risk = report["summary"]["total_risky_resources"]

        if total_risk > 0:
            print(f"\nRISK FOUND: {total_risk} resource(s) may incur Free Tier charges.")
            sys.exit(1)
        else:
            print("\nALL CLEAR: account is fully within Free Tier limits.")
            sys.exit(0)

    except NoCredentialsError:
        print("AWS credentials not found — run `aws configure` to set them up.")
        sys.exit(1)

    except ClientError as e:
        print("AWS rejected this request — check the IAM policy attached to 'free-tier-guardian-bot'.")
        print(f"Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()