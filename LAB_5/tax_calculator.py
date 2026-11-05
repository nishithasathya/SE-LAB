"""Tax calculator with improved security and code quality."""

import base64
import os
import re

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from defusedxml import ElementTree

# Tax settings modelled on FY 2025-26.
STANDARD_DEDUCTION_NEW = 75000
STANDARD_DEDUCTION_OLD = 50000
REBATE_LIMIT_NEW = 1200000
CESS = 0.04

NEW_SLABS = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30),
]

OLD_SLABS = [
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]


def calculate_slab_tax(income, slabs, exemption=0):
    """Calculate tax progressively across the supplied income slabs."""
    taxable_income = max(0, income)
    total_tax = 0
    lower_limit = exemption

    for upper_limit, rate in slabs:
        if taxable_income <= lower_limit:
            break

        slab_income = min(taxable_income, upper_limit) - lower_limit
        total_tax += slab_income * rate
        lower_limit = upper_limit

    return total_tax


def slab_rate(income):
    """Return the marginal new-regime tax rate for an income level."""
    for upper_limit, rate in NEW_SLABS:
        if income <= upper_limit:
            return rate

    return NEW_SLABS[-1][1]


def new_regime_tax(salary):
    """Calculate simplified new-regime tax, including rebate and cess."""
    if salary < 0:
        raise ValueError("Salary cannot be negative.")

    taxable_income = max(0, salary - STANDARD_DEDUCTION_NEW)

    tax_amount = calculate_slab_tax(taxable_income, NEW_SLABS)

    if taxable_income <= REBATE_LIMIT_NEW:
        tax_amount = 0

    cess_amount = tax_amount * CESS
    return round(tax_amount + cess_amount)


def basic_exemption(age):
    """Return the old-regime basic exemption for the taxpayer's age."""
    if age < 0:
        raise ValueError("Age cannot be negative.")

    if 60 <= age < 80:
        return 300000

    if age >= 80:
        return 500000

    return 250000


def old_regime_tax(salary, age, deductions):
    """Calculate simplified old-regime tax after deductions and cess."""
    if salary < 0:
        raise ValueError("Salary cannot be negative.")

    if any(value < 0 for value in deductions.values()):
        raise ValueError("Deductions cannot be negative.")

    total_deductions = sum(deductions.values())
    taxable_income = max(
        0,
        salary - STANDARD_DEDUCTION_OLD - total_deductions,
    )

    exemption = basic_exemption(age)
    total_tax = calculate_slab_tax(
        taxable_income,
        OLD_SLABS,
        exemption,
    )

    return round(total_tax * (1 + CESS))


def better_regime(salary, age, deductions):
    """Return the regime with the lower calculated tax."""
    new_tax = new_regime_tax(salary)
    old_tax = old_regime_tax(salary, age, deductions)

    if new_tax <= old_tax:
        return "new"

    return "old"


def is_valid_pan(pan):
    """Check whether a PAN follows the exact ten-character format."""
    if not isinstance(pan, str):
        return False

    return bool(re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan))


def encrypt_pan(pan):
    """Encrypt a PAN using AES-GCM and an externally supplied key."""
    encoded_key = os.environ.get("PAN_ENCRYPTION_KEY")

    if not encoded_key:
        raise ValueError(
            "PAN_ENCRYPTION_KEY is not configured."
        )

    try:
        key = base64.urlsafe_b64decode(encoded_key)
    except (ValueError, TypeError) as error:
        raise ValueError("Invalid PAN encryption key.") from error

    if len(key) != 32:
        raise ValueError(
            "PAN encryption key must decode to exactly 32 bytes."
        )

    nonce = os.urandom(12)
    cipher = AESGCM(key)

    encrypted_data = cipher.encrypt(
        nonce,
        pan.encode("utf-8"),
        None,
    )

    return (nonce + encrypted_data).hex()


def signing_key():
    """Generate an RSA private key using a 2048-bit key size."""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


def parse_form16(xml_text):
    """Safely extract salary and TDS values from Form 16 XML."""
    root = ElementTree.fromstring(xml_text)

    salary_text = root.findtext("salary")
    tds_text = root.findtext("tds")

    if salary_text is None or tds_text is None:
        raise ValueError(
            "Form 16 XML must contain salary and tds elements."
        )

    try:
        salary = int(salary_text)
        tds = int(tds_text)
    except ValueError as error:
        raise ValueError(
            "Salary and TDS values must be integers."
        ) from error

    return salary, tds


def main():
    """Run sample calculations and demonstrate calculator features."""
    print("New regime, salary 12,75,000:", new_regime_tax(1275000))
    print("New regime, salary 18,00,000:", new_regime_tax(1800000))

    deductions = {"80C": 200000, "80D": 30000}

    print(
        "Old regime, salary 18,00,000:",
        old_regime_tax(1800000, 35, deductions),
    )
    print(
        "Better regime:",
        better_regime(1800000, 35, deductions),
    )
    print("Basic exemption at age 80:", basic_exemption(80))
    print("Valid PAN?", is_valid_pan("ABCDE1234F"))

    form16 = "<form16><salary>1800000</salary><tds>150000</tds></form16>"
    print("Form 16:", parse_form16(form16))
    print("Signing key size:", signing_key().key_size)

    try:
        encrypted_pan = encrypt_pan("ABCDE1234F")
        print("PAN encrypted successfully:", bool(encrypted_pan))
    except ValueError as error:
        print("PAN encryption skipped:", error)


if __name__ == "__main__":
    main()
