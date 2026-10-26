# 1. Cloud-Based File Storage System | Secure Google Drive Clone

> **Objective:** Build a secure cloud storage app similar to Google Drive using AWS S3.

This project was built as per the guidelines: AWS S3 for storage, OAuth 2.0 authentication, file versioning, and file sharing options.

## 📌 Project Overview

This is a fully functional, secure cloud file storage system that allows users to upload, download, delete, version, and share files. It replicates core Google Drive functionality using serverless AWS architecture. The entire backend is serverless and highly scalable.

**Guidelines Implemented:**
1. ✅ **Storage:** AWS S3 for file storage
2. ✅ **Authentication:** OAuth 2.0 (Google Sign-In) + AWS Cognito
3. ✅ **File Versioning & Sharing:** S3 Versioning + Presigned Shareable URLs

## ✨ Key Features

### 1. Secure Authentication (OAuth 2.0)
- User login via Google OAuth 2.0 integrated with AWS Cognito Identity Pool
- Each user gets a private folder: `s3://bucket/private/{user_email}/`
- No unauthorized access to other users' files

### 2. File Operations (CRUD)
- **Upload:** Direct upload to S3 via Lambda Presigned POST
- **List:** Fetches all files with metadata (size, date, type) from DynamoDB
- **Download:** Secure download using S3 Presigned URL (expires in 60 mins)
- **Delete:** Deletes file from S3 and metadata from DynamoDB

### 3. File Versioning
- S3 Bucket Versioning enabled
- If user uploads `report.pdf` again with same name, old version is preserved
- User can list and restore previous versions: `s3:ListObjectVersions`
- Implementation: Lambda `list_versions.py` shows VersionId history

### 4. File Sharing Options
- **Private Share:** Generates a Presigned URL with expiry (e.g., 1 hour, 24 hours) that anyone with link can download
- **Public Share:** Option to make file public-read for team sharing
- Share link copied to clipboard: `https://bucket.s3.amazonaws.com/file?X-Amz-Signature=...`
