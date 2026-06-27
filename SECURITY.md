# Security Policy

RedactAI takes the security of our users and their data seriously. We appreciate your help in keeping RedactAI secure.

## Supported Versions

Security updates are provided for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| 0.x.x   | :x:                |

*(Note: Prior to a 1.0.0 release, the `main` branch and the latest `0.x` tag are considered supported for security patching.)*

## Reporting a Vulnerability

Please do **NOT** report security vulnerabilities via public GitHub issues, discussions, or pull requests. 

Instead, please report them by emailing **pss317@uowmail.edu.au** or **snahadhar18@users.noreply.github.com** directly. 

You should receive a response within 48 hours. If the vulnerability is confirmed, we will release a patch as soon as possible and provide credit to the reporter in our security advisory and release notes.

### What to include in your report:
- A description of the vulnerability and its impact.
- Steps to reproduce the issue.
- Any potential workarounds or fixes you have identified.
- Your name/handle for attribution (if desired).

## Threat Model
RedactAI is designed to operate as a middleware layer. 
- The **Engine** operates locally and does not phone home.
- The **Gateway API** is designed to be deployed behind a secure, private network boundary (e.g., inside an enterprise VPC). It does **not** include built-in authentication or rate-limiting by default, as those concerns are deferred to an API gateway (like Kong or Nginx) or a service mesh.

Vulnerabilities regarding remote code execution (RCE) via payloads, regex denial of service (ReDoS) in default detectors, or memory exhaustion (OOM crashes) during normal operation are considered high priority.
