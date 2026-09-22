from src.s3_scanner import is_over_free_tier_limit
import boto3
from moto import mock_aws

from src import s3_scanner
from src.s3_scanner import is_over_free_tier_limit



def test_under_limit_is_not_flagged():
    assert is_over_free_tier_limit(4.99) is False


def test_exactly_at_limit_is_not_flagged():
    assert is_over_free_tier_limit(5.0) is False


def test_over_limit_is_flagged():
    assert is_over_free_tier_limit(5.01) is True


@mock_aws
def test_get_bucket_summary_flags_over_and_under_limit(monkeypatch):
    monkeypatch.setattr(s3_scanner, "FREE_TIER_S3_LIMIT_GB", 500 / (1024 ** 3))

    s3 = boto3.client("s3", region_name="us-east-1")

    s3.create_bucket(Bucket="bucket-under")
    s3.put_object(Bucket="bucket-under", Key="small.txt", Body=b"x")

    s3.create_bucket(Bucket="bucket-over")
    s3.put_object(Bucket="bucket-over", Key="small.txt", Body=b"x" * 1000)

    summaries = s3_scanner.get_bucket_summary()

    under = next(b for b in summaries if b["name"] == "bucket-under")
    over = next(b for b in summaries if b["name"] == "bucket-over")

    assert under["object_count"] == 1
    assert under["over_free_tier_limit"] is False

    assert over["object_count"] == 1
    assert over["over_free_tier_limit"] is True
