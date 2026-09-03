# AWS Free-Tier Guardian

A command-line tool that scans your AWS account for running EC2 instances and S3 buckets that risk breaking Free Tier limits — built with Python and boto3.

---

## Problem Statement

AWS's Free Tier only covers small, specific resources (e.g., `t2.micro`/`t3.micro` EC2 instances, 5GB of S3 storage). It's easy to accidentally launch something slightly bigger, or leave a bucket growing quietly, and get hit with an unexpected bill weeks later with no warning.

**AWS Free-Tier Guardian** solves this by scanning your account on demand (or on a schedule) and flagging anything that falls outside Free Tier limits *before* it costs you money.

---

## Features

-  Scans all running EC2 instances and flags any that aren't Free-Tier-eligible instance types
- Scans all S3 buckets and flags any exceeding the 5GB Free Tier storage allowance
-  Prints a clear, color-coded terminal report with a final risk summary
-  Uses a dedicated, read-only IAM identity — this tool can never modify or delete your AWS resources
-  Exits with a non-zero status code when risk is found, so it can be wired into automated checks later

---

## Setup

> **TODO (Phase 1 & 2):** This section will be finalized once the local environment and AWS credentials are configured. Placeholder steps below will be tested and confirmed as part of Issue #24.

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/aws-free-tier-guardian.git
   cd aws-free-tier-guardian
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure AWS credentials for the dedicated read-only IAM user (see Phase 2 of the project blueprint for how to create one securely):
   ```bash
   aws configure
   ```

---

## Usage

> **TODO (Phase 5):** Exact command and flags will be confirmed once the CLI interface is built.

```bash
python main.py --region us-east-1
```

**Example output:**
```
TODO: paste a real (sanitized) terminal output screenshot/text block here
once Phase 5 (CLI & Output Formatting) is complete.
```

---

## Demo Video

> **TODO (Phase 9):** Link will be added here once the demo video is recorded and uploaded.

[Watch the demo on YouTube](TODO-add-link-here)

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.