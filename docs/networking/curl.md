---
title: "Linux curl Command"
description: "Learn Linux curl — send HTTP/HTTPS requests, test REST APIs, authenticate, download files, and troubleshoot web services from the command line."
difficulty: beginner
estimated_time: "150 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 9 · Linux Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - linux
  - curl
  - http
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `curl` Command — Transferring Data and Testing APIs

> **`curl` (Client URL)** is one of the most powerful command-line tools used to transfer data between a client and a server using various network protocols. It is widely used for **testing REST APIs, downloading data, uploading files, debugging HTTP/HTTPS requests, interacting with cloud services, Kubernetes APIs, and automating web-based workflows**. `curl` supports more than 20 protocols, including HTTP, HTTPS, FTP, SFTP, SCP, SMTP, LDAP, and more. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), Network Engineer, and Security Engineer should master the `curl` command.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 150 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `curl` command
- Send HTTP and HTTPS requests
- Test REST APIs
- Work with request headers
- Authenticate API requests
- Upload and download files
- Troubleshoot web services

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)
- [Linux `ss` Command](ss.md)
- [Linux `netstat` Command](netstat.md)
- [Linux `tcpdump` Command](packet-analysis-tcpdump-wireshark.md)
- [Linux `traceroute` Command](traceroute.md)
- [Linux `dig` Command](dig.md)
- [Linux `nslookup` Command](nslookup.md)

Basic understanding of:

- HTTP
- HTTPS
- REST APIs
- JSON

---

# Why Learn `curl`?

Suppose users report:

- API Not Responding
- Website Returns Error
- Authentication Failure
- Kubernetes API Issues
- Cloud Service Errors

Instead of opening a browser, Linux engineers use:

```bash
curl
```

to verify:

- Is the server reachable?
- What HTTP status code is returned?
- What headers are sent?
- What response body is received?
- Does authentication work?

---

# What is `curl`?

`curl` stands for:

```text
Client URL
```

It sends requests to servers and displays responses.

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
- Many others

---

# Basic Syntax

```bash
curl [options] URL
```

Example:

```bash
curl https://example.com
```

---

# Simple HTTP Request

```bash
curl http://example.com
```

Returns:

```text
HTML Response
```

---

# HTTPS Request

```bash
curl https://example.com
```

Uses Transport Layer Security (TLS) automatically.

---

# Display Response Headers

```bash
curl -I https://example.com
```

Example output:

```text
HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 1234
```

---

# Display Headers and Body

```bash
curl -i https://example.com
```

---

# Verbose Mode

```bash
curl -v https://example.com
```

Displays:

- Domain Name System (DNS) Resolution
- Transmission Control Protocol (TCP) Connection
- TLS Handshake
- HTTP Request
- HTTP Response

Useful for troubleshooting.

---

# Follow Redirects

```bash
curl -L https://example.com
```

Automatically follows HTTP redirects.

---

# Save Output to File

```bash
curl -o index.html https://example.com
```

---

# Save Using Remote Filename

```bash
curl -O https://example.com/file.txt
```

Uses the filename from the URL.

---

# Download Multiple Files

```bash
curl -O https://example.com/file1.txt \
     -O https://example.com/file2.txt
```

---

# Specify HTTP Method

GET (default):

```bash
curl https://api.example.com/users
```

POST:

```bash
curl -X POST https://api.example.com/users
```

PUT:

```bash
curl -X PUT https://api.example.com/users/1
```

DELETE:

```bash
curl -X DELETE https://api.example.com/users/1
```

---

# Send JSON Data

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"name":"Alice"}' \
https://api.example.com/users
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
curl -H "Authorization: Bearer TOKEN" \
https://api.example.com
```

Common for REST APIs and cloud platforms.

---

# Upload a File

```bash
curl -F "file=@report.pdf" \
https://example.com/upload
```

---

# Upload JSON File

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d @data.json \
https://api.example.com
```

---

# Display Only HTTP Status Code

```bash
curl -o /dev/null -s -w "%{http_code}\n" \
https://example.com
```

Useful in monitoring scripts.

---

# Ignore TLS Certificate Validation

```bash
curl -k https://example.com
```

> **Warning:** Use `-k` only for testing or trusted internal environments. Do not disable certificate validation in production.

---

# Set Request Timeout

```bash
curl --max-time 10 https://example.com
```

Stops the request after ten seconds.

---

# Test REST API

```bash
curl https://jsonplaceholder.typicode.com/posts/1
```

Returns:

```json
{
  "id": 1,
  "title": "...",
  "body": "..."
}
```

---

# Enterprise Example

Test a production API.

```bash
curl -H "Authorization: Bearer TOKEN" \
https://api.company.com/v1/users
```

Verify:

- Authentication
- Response Time
- Status Code
- Response Body

---

# Cloud Perspective

Cloud engineers use `curl` to:

- Test Cloud APIs
- Verify Load Balancers
- Check Health Endpoints
- Retrieve Metadata
- Validate Service Availability

---

# Kubernetes Perspective

Test Kubernetes API.

```bash
curl https://KUBE_API_SERVER:6443
```

Health endpoint.

```bash
curl http://SERVICE_IP/health
```

Ingress endpoint.

```bash
curl https://app.example.com
```

`curl` is widely used to verify:

- Services
- Ingress
- API Gateways
- Health Checks

---

# Linux Perspective

Basic request.

```bash
curl https://example.com
```

Verbose mode.

```bash
curl -v https://example.com
```

Download file.

```bash
curl -O https://example.com/file.txt
```

POST request.

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"test":"value"}' \
https://api.example.com
```

---

# Common HTTP Status Codes

| Status Code | Meaning |
|-------------|----------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 301 | Permanent Redirect |
| 302 | Temporary Redirect |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

# Common `curl` Commands

| Command | Purpose |
|----------|----------|
| `curl URL` | GET request |
| `curl -I URL` | Headers only |
| `curl -i URL` | Headers and body |
| `curl -v URL` | Verbose output |
| `curl -O URL` | Download using remote filename |
| `curl -o file URL` | Save with custom filename |
| `curl -X POST` | POST request |
| `curl -H` | Add headers |
| `curl -d` | Send request body |
| `curl -u` | Basic authentication |

---

# Hands-on Lab

## Task 1

Retrieve a web page.

```bash
curl https://example.com
```

---

## Task 2

Display response headers.

```bash
curl -I https://example.com
```

---

## Task 3

Use verbose mode.

```bash
curl -v https://example.com
```

---

## Task 4

Download a file.

```bash
curl -O https://example.com/file.txt
```

---

## Task 5

Send a POST request.

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"message":"Hello"}' \
https://httpbin.org/post
```

---

## Task 6

Retrieve only the HTTP status code.

```bash
curl -o /dev/null -s -w "%{http_code}\n" \
https://example.com
```

---

## Task 7

Test a REST API endpoint with a custom Authorization header.

---

## Task 8

Use `curl` to test a Kubernetes Ingress or application health endpoint and verify the HTTP response.

---

# Production Troubleshooting

Problem:

```text
API

Returns

500 Error
```

Check:

```bash
curl -v \
https://api.company.com
```

↓

Inspect:

- DNS Resolution
- TLS Handshake
- HTTP Status
- Response Headers
- Response Body

↓

Identify:

- Authentication Failure
- Server Error
- Timeout
- Redirect
- Certificate Issue

---

# curl vs wget

| curl | wget |
|------|------|
| API Testing | File Download |
| Supports Many Protocols | Optimized for Downloads |
| Sends Custom Requests | Recursive Downloads |
| REST API Automation | Website Mirroring |
| Preferred for HTTP Debugging | Preferred for Bulk Downloads |

---

# Common Mistakes

❌ Forgetting quotes around JSON.

✅ Always quote JSON payloads.

---

❌ Using the wrong HTTP method.

✅ Verify the API documentation.

---

❌ Ignoring response headers.

✅ Inspect headers during troubleshooting.

---

❌ Disabling TLS validation in production.

✅ Use valid certificates instead of `-k`.

---

❌ Forgetting authentication headers.

✅ Include required credentials or tokens.

---

# Best Practices

- Use verbose mode when troubleshooting.
- Check HTTP status codes before parsing responses.
- Protect API tokens and credentials.
- Validate TLS certificates in production.
- Use `-L` when redirects are expected.
- Format JSON responses using tools like `jq` when available.
- Automate health checks with `curl`.

---

# Interview Questions

## Beginner

1. What is `curl`?
2. How do you display HTTP headers?
3. How do you download a file?
4. What does `curl -v` do?

---

## Intermediate

1. How do you send a POST request?
2. How do you authenticate using a Bearer token?
3. Explain common HTTP status codes.
4. How do you troubleshoot an API using `curl`?

---

## Architect Level

1. Design an API health-check workflow using `curl`.
2. Explain how you would debug intermittent API failures.
3. How would you automate production endpoint monitoring with `curl`?

---

# Summary

In this lesson, you learned:

- The `curl` command
- HTTP and HTTPS Requests
- REST API Testing
- Authentication
- Request Headers
- File Downloads
- HTTP Status Codes
- Enterprise API Troubleshooting

`curl` is one of the most versatile networking tools available on Linux. It enables engineers to interact with web servers, APIs, cloud services, and Kubernetes applications directly from the command line. Mastering `curl` is essential for testing APIs, automating HTTP requests, validating service health, and troubleshooting modern web-based infrastructure.

---

## Key Takeaways

- `curl` is the **standard command-line tool** for HTTP and API communication.
- It supports **GET, POST, PUT, DELETE**, and many other request methods.
- Use **`-H`** to send custom headers and **`-d`** to send request data.
- Use **`-v`** for detailed troubleshooting and **`-I`** to inspect response headers.
- `curl` is widely used for **REST APIs, Kubernetes, cloud services, automation, and monitoring**.
- Understanding HTTP status codes is essential for diagnosing application issues.

---

## What's Next?

**[wget](wget.md)**

In the next lesson, you'll learn about **`wget`**.

You'll explore:

- What `wget` is
- Downloading Files
- Recursive Downloads
- Resume Interrupted Downloads
- Background Downloads
- Website Mirroring
- Automation with `wget`

By the end of the lesson, you'll understand how to efficiently download files, mirror websites, automate file retrieval, and use `wget` for system administration, DevOps workflows, and software distribution.
