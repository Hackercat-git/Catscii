# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅        |

## Reporting a vulnerability

If you find a security vulnerability in Catscii, **please do not open a public issue**.

Instead, open a [GitHub Security Advisory](https://github.com/Hackercat-git/Catscii/security/advisories/new)
or email the maintainer directly (see the GitHub profile for contact details).

Please include:

- A description of the vulnerability
- Steps to reproduce it
- Any potential impact you can identify

You can expect an acknowledgment within 48 hours and a fix or mitigation plan within 7 days for confirmed issues.

## Scope

Catscii is a local CLI tool and browser demo. It does not run a server, handle authentication, or store user data. The main risk surface is **image parsing** (Pillow); if you find a way to craft a malicious image file that causes unexpected behavior, that is in scope.
