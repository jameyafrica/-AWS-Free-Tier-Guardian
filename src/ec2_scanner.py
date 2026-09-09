import boto3

# This allow-list defines which instance types AWS currently covers under Free Tier.
# It's a plain Python list (not fetched from AWS) because Free Tier eligibility
# isn't something boto3 can query directly — AWS documents it, but doesn't expose
# an API for "is this type free tier eligible?" So we maintain it ourselves.
FREE_TIER_INSTANCE_TYPES = ["t2.micro", "t3.micro"]

def get_running_instances(region="us-east-1"):
    """
    Scans the given AWS region for EC2 instances currently in the 'running' state.

    Returns a list of dicts, each shaped like:
        {"id": ..., "type": ..., "region": ..., "is_free_tier_eligible": ...}
    """
    client = boto3.client("ec2", region_name=region)
    # boto3 is python li
    response = client.describe_instances()

    running_instances = []

    # Reservations group instances launched together in a single request.
    # We don't care about that grouping, so we flatten it here.
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["State"]["Name"] == "running":
                running_instances.append({
                    "id": instance["InstanceId"],
                    "type": instance["InstanceType"],
                    "region": region,
                    "is_free_tier_eligible": instance["InstanceType"] in FREE_TIER_INSTANCE_TYPES
                })

    return running_instances