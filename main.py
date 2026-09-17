from botocore.exceptions import ClientError
from src.ec2_scanner import get_running_instances

print("Guardian starting...")

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