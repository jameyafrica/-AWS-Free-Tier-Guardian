from botocore.exceptions import ClientError
from src.ec2_scanner import get_running_instances
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

    except ClientError as e:
        print("AWS rejected this request — likely a permissions issue.")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()        