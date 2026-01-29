---
name: debug
description: Debug với root cause analysis (5 Whys). Auto-trigger khi user báo lỗi: error, bug, crash, không hoạt động, unexpected behavior, hoặc cần investigate issue.
---

# TLSync Debug - Root Cause Analysis

## 5 Whys Method

Khi gặp lỗi, đặt câu hỏi "Why?" 5 lần để tìm root cause:

### Ví dụ: Message không forward

- Why #1: Message không forward từ user group
- Why #2: Handler không match điều kiện reply_to
- Why #3: reply_to_msg_id không bằng topic_id trong config
- Why #4: Topic ID trong config sai
- Why #5: Config được set manual sai từ đầu

**Root Cause**: Process set topic ID thiếu validation

## Log Format

`[component] description | key=value key2=value2`

Ví dụ:

- `[EVENT] Chat ID | actual=123 expected=456`
- `[CONFIG] Load | path=data.json status=success`
- `[API] PUT /api/config | status=200`
