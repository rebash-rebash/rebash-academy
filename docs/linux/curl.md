---
title: "curl — Transferring Data and Testing APIs from the Command Line"
description: "Use curl for HTTP/HTTPS and API work — GET/POST requests, headers, JSON, authentication, downloads, status codes, and production troubleshooting."
difficulty: intermediate
estimated_time: "75 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 8 · Networking"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - networking
  - curl
  - http
  - api
  - rebash-linux-mastery
comments: false
status: ready
---

# curl — Transferring Data and Testing APIs from the Command Line

> **curl (Client URL)** is one of the most powerful command-line tools for transferring data using URLs. It supports numerous protocols, including HTTP, HTTPS, FTP, SFTP, and more. Linux administrators, DevOps engineers, Cloud Architects, API developers, and Site Reliability Engineers (SREs) use `curl` daily to test web servers, interact with REST APIs, download files, verify application health, and troubleshoot network services.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 9</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 75 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Networking</div>

<div markdown>**Lesson:** 9 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `curl` command
- Make HTTP and HTTPS requests
- Test REST APIs
- Download files
- Send request headers
- Send JSON data
- Authenticate requests
- Troubleshoot web services

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 – Package Management
- Module 8 Lessons 1–8

---

# Why Learn curl?

Imagine:

- Your API is returning errors.
- Kubernetes readiness probes are failing.
- You need to verify a REST endpoint.
- A website is unreachable.
- You need to download a configuration file.

The first command many engineers use is:

```bash
curl
```

---

# What is curl?

`curl` stands for:

```text
Client URL
```

It transfers data between a client and a server.

Supported protocols include:

- HTTP
- HTTPS
- FTP
- FTPS
- SFTP
- SCP
- SMTP
- LDAP
- MQTT
- File

---

# How curl Works

```text
Client
   │
   ▼
HTTP Request
   │
   ▼
Web Server
   │
   ▼
HTTP Response
   │
   ▼
Client
```

---

# Basic Request

Request a web page.

```bash
curl https://example.com
```

The response body is displayed in the terminal.

---

# View Only HTTP Headers

```bash
curl -I https://example.com
```

Example:

```text
HTTP/2 200

content-type: text/html
```

---

# Follow Redirects

Some websites redirect requests.

```bash
curl -L http://example.com
```

`-L` tells `curl` to follow redirects automatically.

---

# Download a File

Save using the remote filename.

```bash
curl -O https://example.com/file.zip
```

Save with a custom filename.

```bash
curl -o backup.zip https://example.com/file.zip
```

---

# Display Verbose Output

Useful for troubleshooting.

```bash
curl -v https://example.com
```

Shows:

- DNS lookup
- TCP connection
- TLS handshake
- Request headers
- Response headers

---

# Silent Mode

Suppress progress output.

```bash
curl -s https://example.com
```

Useful in shell scripts.

---

# Send a GET Request

```bash
curl https://api.example.com/users
```

GET is the default HTTP method.

---

# Send a POST Request

```bash
curl -X POST https://api.example.com/users
```

---

# Send JSON Data

```bash
curl -X POST https://api.example.com/users \
-H "Content-Type: application/json" \
-d '{"name":"Alice","role":"admin"}'
```

---

# Send Custom Headers

```bash
curl -H "Authorization: Bearer TOKEN" \
https://api.example.com
```

---

# Basic Authentication

```bash
curl -u username:password \
https://example.com
```

---

# Bearer Token Authentication

```bash
curl \
-H "Authorization: Bearer TOKEN" \
https://api.example.com
```

---

# Send Query Parameters

```bash
curl "https://api.example.com/users?id=100"
```

---

# View HTTP Status Code

```bash
curl -o /dev/null -s -w "%{http_code}\n" \
https://example.com
```

Example output:

```text
200
```

Common status codes:

| Code | Meaning |
|------|----------|
| 200 | OK |
| 201 | Created |
| 301 | Moved Permanently |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

# Test HTTPS Certificates

```bash
curl -v https://example.com
```

To ignore certificate verification (testing only):

```bash
curl -k https://example.com
```

> **Warning:** Avoid using `-k` in production because it disables TLS certificate verification.

---

# Common Commands

Basic request.

```bash
curl https://example.com
```

Headers only.

```bash
curl -I https://example.com
```

Verbose mode.

```bash
curl -v https://example.com
```

Download file.

```bash
curl -O https://example.com/file.zip
```

POST request.

```bash
curl -X POST https://api.example.com
```

---

# Real Production Examples

Check website availability.

```bash
curl -I https://example.com
```

Verify Kubernetes health endpoint.

```bash
curl http://localhost:8080/health
```

Call REST API.

```bash
curl https://api.example.com/users
```

Download a configuration file.

```bash
curl -O https://example.com/config.yaml
```

Verify HTTP status.

```bash
curl -o /dev/null -s -w "%{http_code}" \
https://example.com
```

---

# Production Perspective

`curl` is widely used for:

- REST API testing
- Kubernetes health checks
- Load balancer verification
- CI/CD pipelines
- Monitoring scripts
- Cloud service testing
- Authentication testing
- Application troubleshooting

It is one of the most frequently used networking tools in DevOps and SRE environments.

---

# Hands-on Lab

## Task 1

Request a web page.

```bash
curl https://example.com
```

---

## Task 2

Display only response headers.

```bash
curl -I https://example.com
```

---

## Task 3

Display verbose output.

```bash
curl -v https://example.com
```

---

## Task 4

Download a file.

```bash
curl -O https://example.com/index.html
```

---

## Task 5

Check the HTTP status code.

```bash
curl -o /dev/null -s -w "%{http_code}\n" \
https://example.com
```

---

## Task 6

Request a REST API.

```bash
curl https://jsonplaceholder.typicode.com/posts/1
```

---

## Task 7

Send JSON data.

```bash
curl -X POST \
https://httpbin.org/post \
-H "Content-Type: application/json" \
-d '{"message":"Hello Linux"}'
```

---

## Task 8

Follow redirects.

```bash
curl -L http://example.com
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `curl URL` | GET request | API testing |
| `curl -I` | Headers only | Server verification |
| `curl -O` | Download file | Configuration download |
| `curl -o` | Save with filename | Backup downloads |
| `curl -v` | Verbose output | Troubleshooting |
| `curl -L` | Follow redirects | Website testing |
| `curl -H` | Send custom headers | API authentication |
| `curl -X POST` | POST request | REST API testing |

---

# Common curl Errors

| Error | Possible Cause |
|--------|----------------|
| `Could not resolve host` | DNS failure |
| `Connection refused` | Service not running or port closed |
| `Connection timed out` | Network or firewall issue |
| `SSL certificate problem` | Invalid or untrusted certificate |
| `404 Not Found` | Resource does not exist |
| `401 Unauthorized` | Authentication required |

---

# curl vs wget

| Feature | curl | wget |
|----------|------|------|
| API Requests | ✅ Excellent | Limited |
| Download Files | ✅ | ✅ Excellent |
| Upload Data | ✅ | Limited |
| HTTP Methods | Multiple | Mostly GET |
| Custom Headers | ✅ | ✅ |
| Resume Downloads | Basic | Excellent |

Use **curl** for APIs and web services.

Use **wget** primarily for downloading files and websites.

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A Kubernetes application fails its readiness probe.

Investigation:

Check the health endpoint.

```bash
curl -v http://localhost:8080/health
```

Response:

```text
HTTP/1.1 500 Internal Server Error
```

Check application logs.

```bash
journalctl -u myapp
```

The application cannot connect to its database.

After fixing the database connection:

```bash
curl http://localhost:8080/health
```

Response:

```text
OK
```

The readiness probe now succeeds, and the application becomes available.

---

# Best Practices

- Use `-I` to verify HTTP headers quickly.
- Use `-v` when troubleshooting connection problems.
- Use `-s` in automation scripts to suppress unnecessary output.
- Verify HTTP status codes when testing APIs.
- Protect authentication credentials and tokens.
- Avoid using `-k` except in controlled testing environments.

---

# Common Mistakes

❌ Forgetting to follow redirects with `-L`.

✅ Remember to to follow redirects with `-L`.

---

❌ Exposing authentication tokens in shared scripts.

✅ Avoid this mistake: exposing authentication tokens in shared scripts.

---

❌ Ignoring HTTP status codes.

✅ Always review HTTP status codes.

---

❌ Using `-k` in production environments.

✅ Avoid using `-k` in production environments when a safer approach exists.

---

# Interview Questions
## Beginner

1. What is `curl` used for?
2. Which command displays only HTTP headers?
3. How do you download a file?
4. Which option enables verbose output?

---

## Intermediate

1. How do you send a POST request with JSON?
2. What does the `-H` option do?
3. How do you follow redirects?
4. How do you retrieve only the HTTP status code?

---

## Architect Level

1. How would you use `curl` to troubleshoot a failing REST API?
2. Why is `curl` commonly used in CI/CD pipelines?
3. How would you securely authenticate API requests using `curl`?

---

# Summary

In this lesson, you learned:

- The `curl` command
- HTTP and HTTPS requests
- REST API testing
- File downloads
- Authentication
- HTTP headers
- Status codes
- Production troubleshooting

`curl` is one of the most versatile networking tools available on Linux. It is indispensable for interacting with web servers, testing APIs, downloading files, and diagnosing application connectivity issues in modern production environments.

---

## Key Takeaways

- `curl` is the standard command-line tool for transferring data using URLs.
- Use `curl -I` to view HTTP headers.
- Use `curl -v` for detailed troubleshooting.
- Use `curl -H` to send custom request headers.
- Use `curl -X` to specify HTTP methods such as POST, PUT, or DELETE.
- `curl` is an essential tool for API testing, automation, and DevOps workflows.

---

## What's Next?

**[wget — Downloading Files from the Command Line](wget.md)**

You'll explore:

- Downloading files from the Internet
- Recursive downloads
- Resuming interrupted downloads
- Background downloads
- Mirroring websites
- Authentication
- Production download automation

While `curl` excels at interacting with APIs and web services, `wget` is optimized for downloading files and website content efficiently.
