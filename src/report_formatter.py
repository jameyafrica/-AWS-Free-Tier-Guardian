from tabulate import tabulate


def format_ec2_table(ec2_results):
    """
    Formats EC2 scan results as a readable table string.
    Returns a friendly message if there's nothing to show.
    """
    if not ec2_results:
        return "Nothing to report — no running EC2 instances."

    headers = ["Instance ID", "Type", "Region", "Free Tier Eligible"]
    rows = [
        [
            instance["id"],
            instance["type"],
            instance["region"],
            "Y" if instance["is_free_tier_eligible"] else "N",
        ]
        for instance in ec2_results
    ]
    return tabulate(rows, headers=headers, tablefmt="grid")


def format_s3_table(s3_results):
    """
    Formats S3 scan results as a readable table string.
    Returns a friendly message if there's nothing to show.
    """
    if not s3_results:
        return "Nothing to report — no S3 buckets found."

    headers = ["Bucket Name", "Size (GB)", "Over Limit"]
    rows = [
        [
            bucket["name"],
            bucket["size_gb"],
            "Y" if bucket["over_free_tier_limit"] else "N",
        ]
        for bucket in s3_results
    ]
    return tabulate(rows, headers=headers, tablefmt="grid")