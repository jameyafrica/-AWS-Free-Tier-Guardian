# AWS Free-Tier Guardian

A command-line tool that scans your AWS account for running EC2 instances and S3 buckets that risk breaking Free Tier limits — built with Python and boto3.

---

## Problem Statement

AWS's Free Tier only covers small, specific resources (e.g., `t2.micro`/`t3.micro` EC2 instances, 5GB of S3 storage). It's easy to accidentally launch something slightly bigger, or leave a bucket growing quietly, and get hit with an unexpected bill weeks later with no warning.

**AWS Free-Tier Guardian** solves this by scanning your account on demand and flagging anything that falls outside Free Tier limits *before* it costs you money.

---

## Features

- Scans all running EC2 instances and flags any that aren't Free-Tier-eligible instance types
- Scans all S3 buckets and flags any exceeding the 5GB Free Tier storage allowance
- Prints a clean, aligned terminal table for each resource type, with a friendly "Nothing to report" message when a category is empty
- Prints a final risk summary and a distinct "ALL CLEAR" / "RISK FOUND" message
- Uses a dedicated, read-only IAM identity — this tool can never modify or delete your AWS resources
- Exits with a non-zero status code (`1`) when risk is found, `0` when the account is fully within Free Tier limits — so it can be wired into automated checks later
- Handles missing credentials and permission errors gracefully, with plain-English messages instead of raw Python tracebacks

---

## Setup

Tested end-to-end on a clean machine (Windows 11, PowerShell) as part of Issue #24.

1. Clone the repository:
```bash
   git clone https://github.com/jameyafrica/-AWS-Free-Tier-Guardian.git
   cd -AWS-Free-Tier-Guardian
```
2. Create and activate a virtual environment:
```powershell
   # Windows (PowerShell):
   python -m venv venv
   venv\Scripts\Activate.ps1
```
```bash
   # macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
```
   If PowerShell blocks the activation script with an execution-policy error, run this once first: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Configure AWS credentials for a dedicated, read-only IAM user (do not use your root account or a full-access key):
```bash
   aws configure
```
   You'll be prompted for an Access Key ID, Secret Access Key, default region (e.g. `us-east-1`), and output format (`json`).

---

## Usage

```bash
python main.py
```

Optionally scan a specific region instead of the default (`us-east-1`):

```bash
python main.py --region eu-west-1
```

**Example output** (real, sanitized run against a test account):