import boto3

FREE_TIER_S3_LIMIT_GB = 5.0

def get_bucket_summary():
    """
    Scans all S3 buckets in the AWS account and summarizes each one.

    Returns:
        list[dict]: one dict per bucket, each containing:
            - "name": bucket name (str)
            - "size_gb": total size of all objects in the bucket, in GB,
              rounded to 2 decimal places (float)
            - "object_count": number of objects in the bucket (int)
        Returns an empty list if the account has no buckets.
    """
    s3 = boto3.client("s3")

    # list_buckets() only returns bucket names/metadata, not their contents
    buckets = s3.list_buckets().get("Buckets", [])

    if not buckets:
        return []

    summaries = []

    for bucket in buckets:
        bucket_name = bucket["Name"]
        total_size_bytes = 0
        object_count = 0

        # A paginator walks through ALL pages of results automatically,
        # even if a bucket has more than the 1000-object-per-response limit
        paginator = s3.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket=bucket_name):
            # An empty bucket has no "Contents" key at all in the response
            for obj in page.get("Contents", []):
                total_size_bytes += obj["Size"]
                object_count += 1

        # Convert bytes -> GB (1024^3 bytes per GB), rounded per the AC
        size_gb = round(total_size_bytes / (1024 ** 3), 2)

        summaries.append({
            "name": bucket_name,
            "size_gb": size_gb,
            "object_count": object_count,
        })

    return summaries