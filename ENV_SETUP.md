# Environment Configuration Guide

This document explains how to set up environment variables for the FAQ Chatbot.

## Required Environment Variables

### 1. OpenAI API Key (Required)

Your OpenAI API key for accessing GPT models.

**Variable Name**: `OPENAI_API_KEY`

**How to Get**:
1. Go to https://platform.openai.com/api/keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

**How to Set**:

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

#### Windows (CMD)
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

#### Linux/Mac (Bash)
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

#### Docker (.env file)
Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-your-key-here
```

Then run:
```bash
docker-compose up --build
```

---

## Optional Environment Variables

### AGENT_MANIFEST_FILE

Path to the agent manifest configuration file.

**Default**: `./registries/manifest.hocon`

**How to Set**:
```bash
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
```

### OPENAI_MODEL

Default LLM model to use (if not specified in agent config).

**Default**: `gpt-4o-mini`

**Options**:
- `gpt-4o` - Most capable model
- `gpt-4o-mini` - Faster, cheaper (recommended)
- `gpt-3.5-turbo` - Legacy, faster

**How to Set**:
```bash
export OPENAI_MODEL="gpt-4o-mini"
```

### PYTHONUNBUFFERED

Enable unbuffered Python output (useful for logging).

**Default**: `1`

**How to Set**:
```bash
export PYTHONUNBUFFERED=1
```

---

## Docker Compose Configuration

To pass environment variables to Docker Compose, create a `.env` file:

```bash
# .env (in project root)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
AGENT_MANIFEST_FILE=./registries/manifest.hocon
```

Then simply run:
```bash
docker-compose up --build
```

Docker Compose will automatically read the `.env` file.

---

## Verify Environment Variables

### Check if variable is set:

**Linux/Mac/PowerShell**:
```bash
echo $OPENAI_API_KEY
```

**Windows CMD**:
```cmd
echo %OPENAI_API_KEY%
```

### Make it permanent (Linux/Mac):

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export OPENAI_API_KEY="sk-your-key-here"
export OPENAI_MODEL="gpt-4o-mini"
```

Then reload:
```bash
source ~/.bashrc
```

---

## Docker Environment Variables

Environment variables are passed to containers via:

1. **`.env` file** (automatic with docker-compose)
2. **Command line**: `docker-compose up -e OPENAI_API_KEY=sk-...`
3. **docker-compose.yml** (hardcoded, not recommended)

### Example docker-compose.yml
```yaml
services:
  backend:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}  # From .env
      - AGENT_MANIFEST_FILE=/app/registries/manifest.hocon
```

---

## Troubleshooting

### Error: "OpenAI API key not provided"

**Check**:
1. Variable is set: `echo $OPENAI_API_KEY`
2. Key is valid: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
3. Key starts with `sk-`

### Error: "Agent manifest file not found"

**Check**:
1. File exists: `ls -la registries/manifest.hocon`
2. Path is correct in AGENT_MANIFEST_FILE variable

### Variables not persisting after terminal close

**Solution**: Add to shell profile:
- Linux/Mac: Add to `~/.bashrc` or `~/.zshrc`
- Windows: Set in Environment Variables → User variables

---

## Production Deployment

### Never commit secrets to Git!

Create `.gitignore` to exclude env files:
```
.env
.env.local
.env.*.local
```

### For Cloud Deployment:

1. **AWS**: Use AWS Secrets Manager or Parameter Store
2. **Azure**: Use Azure Key Vault
3. **Google Cloud**: Use Secret Manager
4. **Heroku**: Use Config Vars
5. **Docker**: Use Docker Secrets

### Example with Docker Secrets:
```bash
echo "sk-your-key" | docker secret create openai_key -
```

Then reference in docker-compose.yml:
```yaml
secrets:
  openai_key:
    external: true

services:
  backend:
    environment:
      - OPENAI_API_KEY_FILE=/run/secrets/openai_key
```

---

## Summary

| Scenario | Command |
|----------|---------|
| Quick test | `export OPENAI_API_KEY=sk-...` then `docker-compose up --build` |
| Local dev | Set in terminal + `python -m uvicorn app.main:app` |
| Docker | Create `.env` file + `docker-compose up --build` |
| Production | Use cloud secrets manager |
