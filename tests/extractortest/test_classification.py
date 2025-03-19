import pytest

from tests.security_analysis.diff_extractor import (
    classify_severity,
    classify_owasp,
    extract_cve_ids_from_msg,
)

@pytest.mark.parametrize(
    "commit_msg,expected_severity",
    [
        ("Fix buffer overflow in parser", "High"),
        ("RCE vulnerability patch", "Critical"),
        ("some random text", "Low"),
    ],
)
def test_classify_severity(commit_msg, expected_severity):
    assert classify_severity(commit_msg) == expected_severity

@pytest.mark.parametrize(
    "commit_msg,expected_owasp",
    [
        ("Fix buffer overflow in parser", "A05:2021 - Security Misconfiguration"),
        ("SQL injection found", "A03:2021 - Injection"),
        ("Nothing special here", "Unknown Category"),
    ],
)
def test_classify_owasp(commit_msg, expected_owasp):
    assert classify_owasp(commit_msg) == expected_owasp

def test_extract_cve_ids():
    msg = "This commit references CVE-2023-1234 and CVE-2021-0001"
    cves = extract_cve_ids_from_msg(msg)
    assert "CVE-2023-1234" in cves
    assert "CVE-2021-0001" in cves
