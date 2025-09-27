# Overview

The **Security Analysis Module** is a Python-based tool designed to analyze security-related commits in Git repositories. It automatically scans commit messages, classifies security vulnerabilities based on **OWASP** and **CVE**, and generates detailed security reports.

---

## Key Features

- **Automated Security Commit Detection**  
  Scans commit messages for security-related keywords.

- **Classification Based on OWASP & CVE**  
  Categorizes security risks using industry-standard frameworks.

- **Severity Level Assessment**  
  Assigns risk levels: **Critical**, **High**, **Medium**, **Low**.

- **Multi-Format Reporting**  
  Generates reports in **CSV**, **JSON**, and **Markdown** formats.

- **Continuous Monitoring Mode**  
  Periodically scans repositories for new security issues.

- **Patch File Generation**  
  Extracts security-related code changes into patch files stored in the `patches/` directory.

---

## ⚙️ Installation

### Prerequisites

- **Python 3.x** must be installed on your system.

### Clone the Repository

```
git clone <repository_link>

```

### Install Dependencies

```
pip install -r requirements.txt
```

## Usage Guide

### Running a Basic Scan

To scan a Git repository for security-related commits, run:

```
cd tests\security_analysis
python diff_extractor.py --repo "<path_to_repository>"
```

#### Explanation:

--repo specifies the target repository to scan.
The tool extracts commits, classifies security risks, and generates reports.

### Running Continuous Monitoring

To enable real-time scanning and automated security tracking, run:

```
python diff_extractor.py --repo "<path_to_repository>" --continuous --interval 60
```

#### Explanation:

- --continuous enables automatic scanning at set intervals.
- --interval 60 sets the scan interval to 60 seconds.
- Viewing Generated Reports

After running the tool, the following outputs are generated:

- CSV Report: report.csv – Structured data for analysis.
- JSON Report: report.json – Machine-readable format.
- Markdown Report: report.md – Human-readable summary.
- Patch Files: Stored in the patches/ directory, containing the diff of security-related code changes.

To view the reports, you can list the files:

```
ls
```

And, for example, display the CSV report:

```
cat report.csv
```

### Example of a Security Alert

If a high-risk commit is found, the CLI will display an alert similar to:

[⚠️ ALERT] High-risk security commit detected!
Commit Hash: abc1234
Severity Level: Critical
CVE Details: CVE-2023-XXXX - Remote Code Execution vulnerability
OWASP Category: A03:2021 - Injection
This enables developers to quickly identify and address potential security risks.

### Developer Notes

Main Script: diff_extractor.py
Security Classification: Utilizes mappings defined in OWASP_MAPPING and SECURITY_KEYWORDS
Reports Directory: patches/ – Stores generated patch files
License
This project is open-source and available under the [LICENSE]MIT License.

### Support & Contact

For issues or feature requests, please open an issue in the repository.
