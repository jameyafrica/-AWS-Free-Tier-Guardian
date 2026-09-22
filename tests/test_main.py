import pytest
from main import valid_region_format

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