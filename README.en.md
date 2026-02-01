# QA TestCase Writer

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A Claude Code skill that automatically generates TestRail-compatible CSV test cases.

---

## Introduction

QA engineers spend significant time writing test cases. Manual creation often leads to:

- ⏱️ **Time-consuming**: Hours spent creating test cases per feature
- 🔍 **Coverage gaps**: Missing critical scenarios like security tests and edge cases
- 📋 **Format errors**: Mistakes in manually creating TestRail CSV format
- 🔄 **Repetitive work**: Rewriting similar test cases repeatedly

**QA TestCase Writer** solves these problems:

✅ Auto-generates test cases from Figma, Jira, PDF, and more
✅ Creates CSV files ready for direct TestRail upload
✅ Automatically includes security tests (SQL Injection, XSS, etc.)
✅ Generates risk analysis, question lists, and coverage checklists
✅ Quality assurance through validation scripts

---

## Key Features

- ✅ **Multiple Input Formats**
  Supports Figma, Axure, Jira, Confluence, PDF, PPT, and website URLs

- ✅ **TestRail-Compatible CSV**
  No need to worry about complex CSV formatting - upload directly to TestRail

- ✅ **Separate UI/UX and Security Tests**
  Manages UI/UX test cases and security test cases in separate CSV files

- ✅ **5 Output Files**
  Provides risk analysis, question lists, and checklists in addition to test cases

- ✅ **Automated Quality Validation**
  Validates CSV format and test case quality with verification scripts

---

## Quick Start

### Prerequisites

- Claude Code CLI must be installed
- Python 3.8 or higher (for validation scripts)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/[username]/qa-testcase-writer.git
cd qa-testcase-writer
```

2. **Copy to Claude Code skills directory**

```bash
cp -r full_qa-testcase-writer ~/.claude/skills/
```

3. **Restart Claude Code**

```bash
claude restart
```

### Create Your First Test Cases

In Claude Code, request:

```
Create test cases from Figma URL https://www.figma.com/file/example
```

5 files will be generated within minutes:

- `[Feature]_testcases.csv`
- `[Feature]_security_testcases.csv`
- `[Feature]_risk_analysis.md`
- `[Feature]_questions.md`
- `[Feature]_checklist.md`

---

## Usage Examples

### Example 1: Generate Test Cases from Figma Design

**Input**:
```
Create test cases from this Figma design
https://www.figma.com/file/abc123/login-page
```

**Output**: `Login_testcases.csv` and 4 other files

---

### Example 2: Generate Test Cases from Live Website

**Input**:
```
Write test cases for this website
https://example.com/login
```

**Output**: `Website_testcases.csv` and 4 other files

---

### Example 3: Generate Test Cases from Specifications (PDF/PPT)

**Input**: After uploading specification.pdf
```
Generate TestRail CSV from this specification
```

**Output**: `Specification_testcases.csv` and 4 other files

---

## Output Files Details

| # | Filename | Purpose | TestRail Upload |
|---|----------|---------|-----------------|
| 1 | `[Feature]_testcases.csv` | UI/UX test cases | ✅ Yes |
| 2 | `[Feature]_security_testcases.csv` | Security test cases | ✅ Yes |
| 3 | `[Feature]_risk_analysis.md` | Risk items and mitigation strategies | - |
| 4 | `[Feature]_questions.md` | Questions about unclear requirements | - |
| 5 | `[Feature]_checklist.md` | Coverage verification checklist | - |

### 1. UI/UX Test Cases CSV Example

```csv
"Section","Section Hierarchy","Title","Preconditions","Steps","Expected Result","Priority"
"Login","","","","","","Highest"
"Normal Cases","Login > Normal Cases","Login with valid account","1. User role: Regular user
2. Access path: Main > Login
3. Test account: test@example.com / Pass1234!","1. Navigate to login page (URL: /login)
2. Enter 'test@example.com' in email field
3. Enter 'Pass1234!' in password field
4. Click 'Login' button","1. Navigate to dashboard page (URL: /dashboard)
2. Display 'test@example.com' in top-right corner
3. Show 'Login successful' toast message","High"
"Error Cases","Login > Error Cases","Incorrect password input","1. Account registered
2. Correct email: test@example.com","1. Navigate to login page
2. Enter 'test@example.com' in email field
3. Enter 'WrongPass123!' in password field
4. Click 'Login' button","1. Login fails
2. Display 'Password does not match' error message
3. Clear password field","High"
```

### 2. Security Test Cases CSV Example

```csv
"Section","Section Hierarchy","Title","Preconditions","Steps","Expected Result","Priority"
"Security Tests","","","","","","Highest"
"Input Attacks","Security Tests > Input Attacks","Block SQL Injection attack","1. Navigate to login page","1. Enter '' OR '1'='1' in email field
2. Enter 'password' in password field
3. Click 'Login' button","1. SQL Injection attack blocked
2. Login fails
3. Display error message (DB info not exposed)","Highest"
"Input Attacks","Security Tests > Input Attacks","Block XSS attack (Script tag)","1. Navigate to login page","1. Enter '<script>alert(1)</script>' in email field
2. Click 'Login' button","1. Script not executed
2. Input value escaped
3. Page functions normally","Highest"
"Auth/Authorization","Security Tests > Auth/Authorization","Block unauthenticated page access","1. Logged out state
2. Protected page URL obtained (e.g., /mypage)","1. Enter protected page URL directly in browser address bar
2. Press Enter","1. Redirect to login page
2. Display 'Login required' message","High"
```

### 3. Risk Analysis MD Example

```markdown
# Risk Analysis

Request URL: https://www.figma.com/file/abc123/login-page

| Risk Item | Likelihood | Impact | Mitigation Strategy |
|-----------|------------|--------|---------------------|
| Session hijacking | Medium | High | Enforce HTTPS, use HttpOnly cookies |
| Brute force attack | High | Medium | Lock account after 5 failed attempts, apply CAPTCHA |
| SQL Injection | Low | Very High | Use Prepared Statements, validate input |
```

### 4. Questions MD Example

```markdown
# Questions About Unclear Requirements

Request URL: https://www.figma.com/file/abc123/login-page

## High Priority

1. Is there a time limit for password reset email sending? (e.g., once per day)
2. How long should auto-login persist? (e.g., 30 days)
3. Is there an account lockout policy on login failure?

## Medium Priority

4. Is social login supported (Google, Facebook, etc.)?
5. What are the minimum password length and complexity requirements?
```

### 5. Checklist MD Example

```markdown
# Coverage Verification Checklist

## Required Features

- [x] Login normal cases
- [x] Login error cases
- [x] Password recovery
- [ ] Social login (needs requirements confirmation)

## Security Tests

- [x] Block SQL Injection
- [x] Block XSS attacks
- [x] Block unauthenticated access

## Edge Cases

- [x] Empty input
- [x] Whitespace-only input
- [x] Prevent double-click duplicate requests
```

---

## Technical Implementation

This skill leverages the following technologies:

### MCP Integration

- **Figma MCP**: Auto-extracts Components, Text, Input properties, and Interactive flows from Figma designs
- **Atlassian MCP**: Extracts issue descriptions, Acceptance Criteria, attachments, and linked issues from Jira/Confluence
- **Playwright/Chrome-in-Chrome MCP**: Crawls websites and analyzes UI components

### Test Design Methodologies

- **Boundary Value Analysis**
- **Equivalence Partitioning**
- **State Transition Testing**
- **Nielsen's UX Usability Principles** for validation

### Quality Assurance

- CSV format validation script (TestRail compatibility)
- Test case quality check script
- Coverage verification checklist

### Reference Materials

- `references/edge-cases.md` - Edge case checklist
- `references/test-techniques.md` - Test technique guide
- `references/nielsen-heuristics.md` - UX usability principles
- `references/security-testcases.csv` - Security test template

---

## Validation Scripts

You can validate generated CSV files:

```bash
# Validate CSV format
python scripts/validate_csv.py [filename].csv

# Quality check (coverage, priority, etc.)
python scripts/quality_check.py [filename].csv

# Final validation before TestRail upload
python scripts/testrail_upload_check.py [filename].csv
```

Once all validations pass, you can safely upload to TestRail.

---

## FAQ

### Setup Related

**Q1. I'm getting MCP connection errors**

A: Check if MCP servers are active in Claude Code. Use `claude mcp list` command to verify Figma MCP and Atlassian MCP status.

**Q2. I'm getting permission errors running Python scripts**

A: Grant execution permissions to scripts: `chmod +x scripts/*.py`

### Usage Related

**Q3. Too few test cases are generated**

A: The requirements document may lack detail. For Figma, provide detailed Component descriptions. For Jira, provide detailed Acceptance Criteria for more test cases.

**Q4. Security test cases were not generated**

A: Security tests are separated into a different CSV file (`[Feature]_security_testcases.csv`). Check that file. At least 3 security tests are automatically included.

### Advanced Usage

**Q5. Can I add custom test techniques?**

A: Yes, modify `references/test-techniques.md` and `references/edge-cases.md` files to add project-specific test techniques. SKILL.md references these files.

---

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Contributing

Issues and Pull Requests are welcome. Before contributing, please:

1. Include reproduction steps in bug reports
2. Explain use cases in feature requests
3. Submit PRs with tests

---

## Contact

For issues or questions, please use GitHub Issues.

---

## Related Documentation

- [SKILL.md](full_qa-testcase-writer/SKILL.md) - Detailed skill guide and writing rules
- [Test Technique Guide](full_qa-testcase-writer/references/test-techniques.md)
- [Edge Case Checklist](full_qa-testcase-writer/references/edge-cases.md)
- [Security Test Template](full_qa-testcase-writer/references/security-testcases.csv)

---

## Requirements

- Claude Code CLI (latest version recommended)
- Python 3.8 or higher (for validation scripts)
- Supported MCP servers: Figma, Atlassian, Playwright, Chrome-in-Chrome

---

## Supported Input Formats

| Format | MCP/Tool | Extracted Content |
|--------|---------|-------------------|
| Figma URL | Figma MCP | Components, Text, Input properties, Interactive flows |
| Axure URL | Playwright/Chrome-in-Chrome MCP | Widget Notes, Interactions, Dynamic Panels |
| Jira/Confluence | Atlassian MCP | Issue descriptions, AC, attachments, linked issues |
| Website URL | Playwright/Chrome-in-Chrome MCP | UI components, labels, screen transition paths |
| PDF/PPT/Screenshots | Image analysis | UI components, labels, screen transition paths |
