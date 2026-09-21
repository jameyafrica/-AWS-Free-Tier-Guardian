from src.s3_scanner import is_over_free_tier_limit


def test_under_limit_is_not_flagged():
    assert is_over_free_tier_limit(4.99) is False


def test_exactly_at_limit_is_not_flagged():
    assert is_over_free_tier_limit(5.0) is False


def test_over_limit_is_flagged():
    assert is_over_free_tier_limit(5.01) is True