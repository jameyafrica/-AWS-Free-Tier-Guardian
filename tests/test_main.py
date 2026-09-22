import pytest
from main import valid_region_format
from main import build_report

def test_valid_region_format_accepts_well_formed_region():
    assert valid_region_format("us-east-1") == "us-east-1"

def test_valid_region_format_accepts_multi_word_direction():
    assert valid_region_format("ap-southeast-1") == "ap-southeast-1"

def test_valid_region_format_rejects_missing_zone_number():
    with pytest.raises(Exception):
        valid_region_format("us-east")

def test_valid_region_format_rejects_gibberish():
    with pytest.raises(Exception):
        valid_region_format("banana")
def test_build_report_counts_risky_resources():
    ec2_results = [
        {"id": "i-1", "is_free_tier_eligible": True},
        {"id": "i-2", "is_free_tier_eligible": False},
    ]
    s3_results = [
        {"name": "bucket-a", "over_free_tier_limit": False},
        {"name": "bucket-b", "over_free_tier_limit": True},
    ]

    report = build_report(ec2_results, s3_results)

    assert report["ec2"] == ec2_results
    assert report["s3"] == s3_results
    assert report["summary"]["total_risky_resources"] == 2

def test_build_report_handles_empty_lists():
    report = build_report([], [])
    assert report["summary"]["total_risky_resources"] == 0