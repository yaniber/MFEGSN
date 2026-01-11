# API Keys Configuration Guide

This guide explains how to configure API keys and tokens for enhanced MFEGSN functionality.

## Overview

MFEGSN supports optional API keys for:
- **Ngrok**: Public URL access for your local server
- **Google Drive API**: Programmatic access to Google Drive
- **GitHub Personal Access Token**: Automated pushing to GitHub

All configuration is optional. The system works without these keys, but they enable additional features.

## 🌐 Ngrok Configuration

### What is Ngrok?

Ngrok creates secure tunnels to your localhost, giving you a public URL to access your local application from anywhere.

### Use Cases
- Share your local application with others
- Test webhooks
- Access from mobile devices
- Demo to clients without deployment

### Setup Instructions

1. **Sign up** at https://ngrok.com/
2. **Get your authtoken** from https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure in MFEGSN**:

#### Option A: Environment Variable (Recommended)
Add to your `.env` file:
```bash
NGROK_AUTHTOKEN=your_token_here
USE_NGROK=true
```

#### Option B: Web Interface
1. Start MFEGSN: `./start.sh` or `python web_interface.py`
2. Open http://localhost:8000
3. Expand "Configuration" section
4. Enter your Ngrok authtoken
5. Click "Save Configuration"

#### Option C: Colab
In the API keys configuration cell:
```python
os.environ['NGROK_AUTHTOKEN'] = 'your_token_here'
```

### Starting with Ngrok

**Local:**
```bash
# Set in .env
USE_NGROK=true
NGROK_AUTHTOKEN=your_token

# Start application
python web_interface.py
```

You'll see output like:
```
============================================================
🌐 NGROK TUNNEL ACTIVE
============================================================
Public URL: https://abc123.ngrok.io
Local URL:  http://localhost:8000
============================================================
```

**Docker:**
```bash
# Add to docker-compose.yml environment
environment:
  - USE_NGROK=true
  - NGROK_AUTHTOKEN=your_token
```

## 📁 Google Drive API Key

### What is it?

Google Drive API key allows programmatic access to your Drive files without OAuth flow (for public files) or with service account (for private files).

### Use Cases
- Automated file imports
- Batch processing
- CI/CD pipelines
- Scheduled tasks

### Setup Instructions

1. **Create a Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing

2. **Enable Drive API**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

3. **Create API Key**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key

4. **Configure in MFEGSN**:

#### Option A: Environment Variable
Add to `.env`:
```bash
GOOGLE_DRIVE_API_KEY=your_api_key_here
```

#### Option B: Web Interface
1. Open configuration section
2. Enter Google Drive API Key
3. Save configuration

#### Option C: Colab
```python
os.environ['GOOGLE_DRIVE_API_KEY'] = 'your_api_key_here'
```

### Usage in Colab

With the API key configured, you can use Google Drive API methods directly in your Python code for advanced file operations.

## 🔑 GitHub Personal Access Token (PAT)

### What is it?

A Personal Access Token is an alternative to using passwords for Git over HTTPS. It provides secure, programmatic access to GitHub repositories.

### Use Cases
- Automated commits and pushes from Colab
- CI/CD pipelines
- Scripted repository operations
- No manual authentication needed

### Setup Instructions

1. **Go to GitHub Settings**
   - Visit https://github.com/settings/tokens
   - Or: Profile > Settings > Developer settings > Personal access tokens

2. **Generate New Token**
   - Click "Generate new token" > "Generate new token (classic)"
   - Give it a descriptive name: e.g., "MFEGSN Colab"
   - Set expiration (30 days, 60 days, or custom)

3. **Select Scopes**
   - **For public repos**: Check `public_repo`
   - **For private repos**: Check `repo` (full repository access)
   
4. **Generate and Copy**
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again!)

5. **Configure in MFEGSN**:

#### Option A: Environment Variable
Add to `.env`:
```bash
GITHUB_PAT=ghp_your_token_here
```

#### Option B: Web Interface
1. Open configuration section
2. Enter GitHub PAT
3. Save configuration

#### Option C: Colab (Recommended)
In the API keys configuration cell:
```python
import os
from getpass import getpass

github_pat = getpass("Enter GitHub PAT: ")
os.environ['GITHUB_PAT'] = github_pat
```

### Using PAT in Colab

With PAT configured, the GitHub push cell will automatically use it:

```python
# This happens automatically when you run the GitHub save cell
branch_name = "colab-outputs-20240115_120000"
!git push https://{os.environ['GITHUB_PAT']}@github.com/yaniber/MFEGSN.git {branch_name}
```

**Benefits:**
- ✅ No manual token entry each time
- ✅ Secure (token hidden in getpass)
- ✅ Automatic push to GitHub
- ✅ Direct PR link provided

## 🔒 Security Best Practices

### Do's ✅

- ✅ Use environment variables or `.env` file for local development
- ✅ Use `getpass()` in Colab to hide input
- ✅ Set token expiration dates
- ✅ Use minimal required scopes
- ✅ Keep tokens private
- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Revoke tokens when no longer needed

### Don'ts ❌

- ❌ Never commit tokens to Git
- ❌ Never share tokens in screenshots
- ❌ Never post tokens in issues or PRs
- ❌ Don't use tokens in public notebooks
- ❌ Don't hardcode tokens in source files
- ❌ Don't give tokens more permissions than needed

### Revoking Tokens

If you accidentally expose a token:

**GitHub PAT:**
1. Go to https://github.com/settings/tokens
2. Find the token
3. Click "Delete"

**Ngrok:**
1. Go to https://dashboard.ngrok.com/tunnels/authtokens
2. Delete the token
3. Generate a new one

**Google API Key:**
1. Go to https://console.cloud.google.com/apis/credentials
2. Find the key
3. Delete it
4. Create a new one

## 📋 Configuration Summary

| Feature | Required For | Setup URL | Scope/Permissions |
|---------|--------------|-----------|-------------------|
| Ngrok | Public URL access | https://dashboard.ngrok.com | N/A |
| Google Drive API | Drive file access | https://console.cloud.google.com | Drive API enabled |
| GitHub PAT | Automated Git push | https://github.com/settings/tokens | `repo` or `public_repo` |

## 🆘 Troubleshooting

### Ngrok Issues

**"ngrok not found"**
- Install: `pip install pyngrok`
- Verify in requirements.txt

**"Invalid authtoken"**
- Check token is correct
- Ensure no extra spaces
- Try regenerating token

**"Tunnel failed"**
- Check internet connection
- Verify firewall settings
- Try restarting application

### Google Drive Issues

**"API key invalid"**
- Verify key is correct
- Check API is enabled
- Verify project has billing enabled (if required)

**"Permission denied"**
- Check file sharing settings
- Verify API key restrictions
- Use service account for private files

### GitHub Issues

**"Authentication failed"**
- Verify PAT is correct
- Check token hasn't expired
- Ensure token has required scopes

**"Permission denied"**
- Verify you have write access to repo
- Check token scopes include `repo` or `public_repo`
- Try regenerating token with correct scopes

**"Invalid token"**
- Token may have been revoked
- Generate new token
- Update configuration

## 📚 Additional Resources

- [Ngrok Documentation](https://ngrok.com/docs)
- [Google Drive API Guide](https://developers.google.com/drive/api/v3/about-sdk)
- [GitHub PAT Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

## 💡 Tips

1. **Development**: Use environment variables for quick testing
2. **Production**: Use proper secrets management (e.g., Docker secrets, Kubernetes secrets)
3. **Colab**: Always use `getpass()` to hide sensitive input
4. **Sharing**: Remove or mask tokens before sharing notebooks/screenshots
5. **Testing**: Create separate tokens for development and production

## ⚙️ Configuration File Example

Complete `.env` file example:

```bash
# Basic Configuration
PDF_DIR=pdfs
MARKDOWN_OUTPUT_DIR=markdown_outputs
CHROMA_DB_DIR=./chroma_db
WEB_PORT=8000

# Optional: Ngrok
USE_NGROK=true
NGROK_AUTHTOKEN=2abc123def456ghi789jkl0_12mnoPQRstUVwxYZ

# Optional: Google Drive
GOOGLE_DRIVE_API_KEY=AIzaSyAbc123def456ghi789jkl0mnoPQRstuvw

# Optional: GitHub
GITHUB_PAT=ghp_abc123def456ghi789jkl0mnoPQRstuvwxyz12
```

**Remember**: Never commit this file to Git! It's already in `.gitignore`.

---

Need help? Open an issue: https://github.com/yaniber/MFEGSN/issues
