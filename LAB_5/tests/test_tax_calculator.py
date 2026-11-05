import base64
import os

import pytest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from tax_calculator import (
    basic_exemption,
    better_regime,
    calculate_slab_tax,
    encrypt_pan,
    is_valid_pan,
    new_regime_tax,
    old_regime_tax,
    parse_form16,
    signing_key,
)


# -------------------------------
# Progressive Tax Calculation
# -------------------------------

def test_calculate_slab_tax():
    slabs = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (float("inf"), 0.15),
    ]

    assert calculate_slab_tax(600000, slabs) == 10000


def test_new_regime_tax():
    assert new_regime_tax(1275000) == 0
    assert new_regime_tax(1800000) == 150800


def test_new_regime_tax_negative_salary():
    with pytest.raises(ValueError):
        new_regime_tax(-100000)


# -------------------------------
# Old Regime and Exemptions
# -------------------------------

def test_basic_exemption():
    assert basic_exemption(35) == 250000
    assert basic_exemption(60) == 300000
    assert basic_exemption(79) == 300000
    assert basic_exemption(80) == 500000
    assert basic_exemption(85) == 500000


def test_negative_age():
    with pytest.raises(ValueError):
        basic_exemption(-1)


def test_old_regime_tax():
    deductions = {"80C": 200000, "80D": 30000}

    assert old_regime_tax(1800000, 35, deductions) == 279240


def test_negative_deductions():
    with pytest.raises(ValueError):
        old_regime_tax(1800000, 35, {"80C": -10000})


def test_better_regime():
    deductions = {"80C": 200000, "80D": 30000}

    assert better_regime(1800000, 35, deductions) == "new"


# -------------------------------
# PAN Validation
# -------------------------------

def test_valid_pan():
    assert is_valid_pan("ABCDE1234F") is True


@pytest.mark.parametrize(
    "pan",
    [
        "ABCDE1234",
        "ABCDE1234FXYZ",
        "abcde1234f",
        "12345ABCDE",
        "",
        None,
    ],
)
def test_invalid_pan(pan):
    assert is_valid_pan(pan) is False


# -------------------------------
# PAN Encryption
# -------------------------------

def test_encrypt_pan():
    key = base64.urlsafe_b64encode(os.urandom(32)).decode()
    os.environ["PAN_ENCRYPTION_KEY"] = key

    encrypted = encrypt_pan("ABCDE1234F")

    assert isinstance(encrypted, str)
    assert encrypted != "ABCDE1234F"


def test_encryption_uses_random_nonce():
    key = base64.urlsafe_b64encode(os.urandom(32)).decode()
    os.environ["PAN_ENCRYPTION_KEY"] = key

    first = encrypt_pan("ABCDE1234F")
    second = encrypt_pan("ABCDE1234F")

    assert first != second


def test_encrypted_pan_can_be_decrypted():
    raw_key = os.urandom(32)
    encoded_key = base64.urlsafe_b64encode(raw_key).decode()
    os.environ["PAN_ENCRYPTION_KEY"] = encoded_key

    encrypted = bytes.fromhex(encrypt_pan("ABCDE1234F"))

    nonce = encrypted[:12]
    ciphertext = encrypted[12:]

    decrypted = AESGCM(raw_key).decrypt(
        nonce,
        ciphertext,
        None,
    )

    assert decrypted.decode("utf-8") == "ABCDE1234F"


def test_missing_encryption_key(monkeypatch):
    monkeypatch.delenv("PAN_ENCRYPTION_KEY", raising=False)

    with pytest.raises(ValueError):
        encrypt_pan("ABCDE1234F")


def test_invalid_encryption_key():
    os.environ["PAN_ENCRYPTION_KEY"] = "invalid-key"

    with pytest.raises(ValueError):
        encrypt_pan("ABCDE1234F")


# -------------------------------
# RSA Key Generation
# -------------------------------

def test_signing_key():
    key = signing_key()

    assert key.key_size == 2048
    assert key.public_key() is not None


# -------------------------------
# Form 16 XML Parsing
# -------------------------------

def test_parse_form16():
    xml = (
        "<form16>"
        "<salary>1800000</salary>"
        "<tds>150000</tds>"
        "</form16>"
    )

    assert parse_form16(xml) == (1800000, 150000)


def test_parse_form16_missing_element():
    xml = "<form16><salary>1800000</salary></form16>"

    with pytest.raises(ValueError):
        parse_form16(xml)


def test_parse_form16_invalid_values():
    xml = (
        "<form16>"
        "<salary>invalid</salary>"
        "<tds>150000</tds>"
        "</form16>"
    )

    with pytest.raises(ValueError):
        parse_form16(xml)


def test_parse_form16_invalid_xml():
    with pytest.raises(Exception):
        parse_form16("<form16><salary>1800000</form16>")