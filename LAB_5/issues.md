# Static Analysis Issues and Fixes

## 1. Overview

The original Income Tax Calculator was analysed using three static analysis tools:

- **Pylint** – Identifies programming errors, code-quality issues, and maintainability problems.
- **Bandit** – Identifies potential security vulnerabilities in Python code.
- **Flake8** – Checks code formatting and compliance with Python coding conventions.

The initial analysis revealed security vulnerabilities, functional issues, unused variables, naming inconsistencies, and formatting violations.

## 2. Identified Issues and Fixes

| No. | Issue | Type | Original Location | Description | Fix Approach |
|---|---|---|---|---|---|
| 1 | Insecure AES ECB encryption | Security – Medium | `encryptPan()` | ECB mode does not provide semantic security and can expose patterns in encrypted data. | Replaced ECB with authenticated AES-GCM encryption using a random nonce. |
| 2 | Weak RSA key size | Security – Medium | `signingKey()` | The original RSA key used only 1024 bits, which is no longer considered sufficiently secure. | Increased the RSA key size to 2048 bits. |
| 3 | Unsafe XML parsing | Security | `parseForm16()` | The original code used `minidom.parseString()` to process XML input, creating potential XML security risks. | Replaced it with the safer `defusedxml.ElementTree` parser. |
| 4 | CGI handler usage | Security – High | `runAsCgi()` | The original implementation used the CGI handler flagged by Bandit. | Removed the CGI handler and its unused entry point. |
| 5 | Hardcoded encryption key | Security | Global `PAN_KEY` | The encryption key was embedded directly in the source code, exposing sensitive key material. | Moved key configuration to the `PAN_ENCRYPTION_KEY` environment variable. |
| 6 | Incomplete PAN validation | Functional | `isValidPan()` | `re.match()` could accept a valid PAN prefix followed by additional characters. | Replaced it with `re.fullmatch()` and added an input-type check. |
| 7 | Bare exception handling | Code Quality | `isValidPan()` | A bare `except` could hide unexpected errors and make debugging difficult. | Removed unnecessary exception handling. |
| 8 | Incorrect progressive tax calculation | Functional | `newRegimeTax()` | The original implementation applied one marginal tax rate to the entire taxable income instead of calculating tax across individual slabs. | Introduced a reusable progressive slab calculation function. |
| 9 | Incorrect age boundary | Functional | `basicExemption()` | A taxpayer aged exactly 80 did not receive the intended senior-citizen exemption. | Changed the condition to include age 80 in the applicable category. |
| 10 | Unused imports and variables | Code Quality | Multiple locations | Unused imports and variables increased clutter and triggered static-analysis warnings. | Removed unused imports and variables. |
| 11 | Naming and documentation issues | Maintainability | Multiple functions | Function names did not follow standard Python naming conventions, and docstrings were missing. | Adopted snake_case naming and added docstrings. |
| 12 | Formatting violations | Code Quality | Multiple locations | The original source contained long lines, missing blank lines, semicolon-separated statements, and a missing final newline. | Reformatted the source to comply with PEP 8 and Flake8. |

## 3. Static Analysis Results

### 3.1 Results Before Fixes

| Tool | Initial Result |
|---|---|
| Pylint | 4.57/10 |
| Bandit | 6 potential security findings |
| Flake8 | 22 reported violations |

### 3.2 Results After Fixes

| Tool | Final Result |
|---|---|
| Pylint | 10.00/10 |
| Bandit | 0 potential security findings |
| Flake8 | 0 violations |

## 4. Improvements Achieved

The following improvements were achieved:

1. Improved encryption security by replacing AES ECB with AES-GCM.
2. Removed hardcoded encryption keys and introduced environment-based key configuration.
3. Increased RSA key strength from 1024 bits to 2048 bits.
4. Replaced unsafe XML parsing with `defusedxml`.
5. Removed the deprecated CGI handler.
6. Improved PAN validation to enforce the exact required format.
7. Corrected progressive tax calculation.
8. Corrected the age-based exemption boundary.
9. Removed unused imports and variables.
10. Improved naming conventions, documentation, and code formatting.

## 5. Conclusion

The static analysis process helped identify security vulnerabilities, functional issues, and maintainability problems in the original Income Tax Calculator.

After implementing the necessary corrections, the application achieved a Pylint score of **10.00/10**, with **zero security findings in Bandit** and **zero formatting violations in Flake8**.

The final implementation is more secure, readable, maintainable, and reliable than the original version.