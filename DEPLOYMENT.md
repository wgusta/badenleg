# Deployment Guide - BadenLEG

## Pre-Deployment Checklist

### 1. Install Dependencies

```bash
cd /path/to/badenleg
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and customize it:

```bash
cp env.example .env
```

Edit `.env` and set at minimum:

```bash
# CRITICAL: Generate a secure secret key
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Set production mode
FLASK_ENV=production
FLASK_DEBUG=False

# Set your production URL
APP_BASE_URL=https://badenleg.ch

# Enable secure cookies
SESSION_COOKIE_SECURE=True
```

### 3. Security Review

Review `SECURITY.md` and ensure all recommendations are followed.

## Deployment Options

### Option A: GitHub Actions (Recommended for Infomaniak)

This is the recommended deployment method for Infomaniak hosting. It automatically deploys when you push to the `main` branch.

#### Prerequisites

1. **Server Setup on Infomaniak**:
   ```bash
   # SSH into your Infomaniak server
   ssh user@your-server.infomaniak.ch
   
   # Navigate to your web directory
   cd ~/www
   
   # Clone the repository (if not already done)
   git clone https://github.com/wgusta/badenleg.git badenleg
   cd badenleg
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create tmp directory for Passenger restarts
   mkdir -p tmp
   
   # Set up .env file (see Pre-Deployment Checklist above)
   cp env.example .env
   # Edit .env with production values
   ```

2. **SSH Key Setup for GitHub Actions**:
   ```bash
   # On your local machine, generate an SSH key for deployment
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/infomaniak_deploy
   
   # Copy the PUBLIC key to Infomaniak server
   ssh-copy-id -i ~/.ssh/infomaniak_deploy.pub user@your-server.infomaniak.ch
   
   # Display the PRIVATE key (you'll add this to GitHub Secrets)
   cat ~/.ssh/infomaniak_deploy
   ```

3. **Configure GitHub Secrets**:
   - Go to: https://github.com/wgusta/badenleg/settings/secrets/actions
   - Click "New repository secret" and add:
     - `INFOMANIAK_HOST`: Your Infomaniak SSH hostname (e.g., `your-server.infomaniak.ch`)
     - `INFOMANIAK_USER`: Your SSH username
     - `INFOMANIAK_SSH_KEY`: The private SSH key content (from step 2)
     - `INFOMANIAK_DEPLOY_PATH`: Path on server (e.g., `~/www/badenleg`)
     - `INFOMANIAK_SSH_PORT`: SSH port (usually 22, optional)

#### Deployment Workflow

1. **Development**:
   ```bash
   # Work on feature branches
   git checkout develop
   git checkout -b feature/new-feature
   # ... make changes ...
   git commit -m "Add new feature"
   git push origin feature/new-feature
   # Create PR on GitHub: feature → develop
   ```

2. **Deploy to Production**:
   ```bash
   # Merge develop into main
   git checkout main
   git merge develop
   git push origin main
   ```
   
   GitHub Actions will automatically:
   - SSH to Infomaniak server
   - Pull latest code from main branch
   - Update dependencies
   - Restart Passenger application
   - Verify deployment

3. **Manual Trigger** (if needed):
   - Go to: https://github.com/wgusta/badenleg/actions
   - Select "Deploy to Infomaniak" workflow
   - Click "Run workflow" → Select branch `main` → Run

#### Troubleshooting

- **Deployment fails**: Check GitHub Actions logs at https://github.com/wgusta/badenleg/actions
- **SSH connection fails**: Verify SSH key is correctly added to GitHub Secrets
- **Application not updating**: Check if `tmp/restart.txt` is being touched (Passenger restart)
- **Dependencies not updating**: Check virtual environment activation in workflow

### Option B: Simple Deployment (Gunicorn)

1. **Install Gunicorn**:
```bash
pip install gunicorn
```

2. **Run the application**:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 app:app
```

3. **Set up as a systemd service** (`/etc/systemd/system/badenleg.service`):
```ini
[Unit]
Description=BadenLEG Web Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/badenleg
Environment="PATH=/path/to/badenleg/venv/bin"
ExecStart=/path/to/badenleg/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Start the service**:
```bash
sudo systemctl daemon-reload
sudo systemctl start badenleg
sudo systemctl enable badenleg
```

### Option C: Docker Deployment

1. **Create Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 badenleg && chown -R badenleg:badenleg /app
USER badenleg

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "120", "app:app"]
```

2. **Create docker-compose.yml** (with Redis):
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - redis
    restart: always
    volumes:
      - ./badenleg_security.log:/app/badenleg_security.log

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

3. **Deploy**:
```bash
docker-compose up -d
```

## Branch Protection and Workflow

### GitHub Branch Protection Rules

To ensure code quality and prevent accidental deployments, configure branch protection:

1. **Go to**: https://github.com/wgusta/badenleg/settings/branches
2. **Add rule for `main` branch**:
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 1 (or more)
   - ✅ Require status checks to pass (optional: add CI checks)
   - ✅ Require branches to be up to date before merging
   - ✅ Do not allow bypassing the above settings
   - ✅ Include administrators

3. **Optional: Add rule for `develop` branch**:
   - ✅ Require pull request reviews (can be less strict than main)
   - ⚠️ Allow force pushes (for development flexibility)

### Branch Workflow

**Development Flow:**
```
feature/xyz → develop → main → production (auto-deploy)
```

1. **Feature Development**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   # Make changes, commit, push
   git push origin feature/your-feature-name
   # Create PR on GitHub: feature → develop
   ```

2. **Merge to Develop**:
   - After PR review and approval
   - Merge PR on GitHub
   - `develop` branch is updated

3. **Deploy to Production**:
   ```bash
   git checkout main
   git pull origin main
   git merge develop
   git push origin main
   # GitHub Actions automatically deploys
   ```

### Manual Deployment Fallback

If GitHub Actions is unavailable, you can deploy manually:

```bash
# SSH into Infomaniak server
ssh user@your-server.infomaniak.ch

# Navigate to project directory
cd ~/www/badenleg

# Pull latest code
git fetch origin
git checkout main
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart application
touch tmp/restart.txt

# Verify deployment
curl https://badenleg.ch/health
```

## Nginx Configuration

Create `/etc/nginx/sites-available/badenleg`:

```nginx
server {
    listen 80;
    server_name badenleg.ch www.badenleg.ch;
    
    # Redirect to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name badenleg.ch www.badenleg.ch;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/badenleg.ch/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/badenleg.ch/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers (additional layer)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/badenleg_access.log;
    error_log /var/log/nginx/badenleg_error.log;
    
    # Max upload size
    client_max_body_size 2M;
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
        
        # Timeouts for long ML operations
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
    
    # Static files (if you add them)
    location /static/ {
        alias /path/to/badenleg/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Deny access to sensitive files
    location ~ /\. {
        deny all;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/badenleg /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d badenleg.ch -d www.badenleg.ch

# Auto-renewal
sudo systemctl enable certbot.timer
```

## Monitoring Setup

### 1. Log Monitoring

Set up log rotation (`/etc/logrotate.d/badenleg`):

```bash
/path/to/badenleg/badenleg_security.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
}
```

### 2. System Monitoring

Monitor the application:

```bash
# Check if service is running
sudo systemctl status badenleg

# View logs
sudo journalctl -u badenleg -f

# Check resource usage
htop
```

### 3. Security Monitoring

Monitor security log for suspicious activity:

```bash
# Watch security log
tail -f /path/to/badenleg/badenleg_security.log

# Check for rate limit violations
grep "RATE_LIMIT" badenleg_security.log

# Check for invalid inputs
grep "INVALID" badenleg_security.log | tail -20
```

## Backup Strategy

### What to Backup

Currently using in-memory storage, but if you add a database:

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/badenleg"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database (if using SQLite)
cp /path/to/badenleg/database.db $BACKUP_DIR/database_$DATE.db

# Backup environment config (without secrets)
grep -v "SECRET\|PASSWORD" /path/to/badenleg/.env > $BACKUP_DIR/env_$DATE.txt

# Backup logs
cp /path/to/badenleg/badenleg_security.log $BACKUP_DIR/security_$DATE.log

# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete
```

Run daily via cron:
```bash
0 2 * * * /path/to/backup.sh
```

## Health Checks

Create a health check endpoint (add to app.py):

```python
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    })
```

Monitor with:
```bash
curl https://badenleg.ch/health
```

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Add Nginx load balancing
2. **Multiple Instances**: Run multiple Gunicorn instances
3. **Redis**: Required for shared rate limiting
4. **Database**: Move to PostgreSQL for persistent storage

Example load balancer config:

```nginx
upstream badenleg_app {
    least_conn;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    # ... SSL config ...
    
    location / {
        proxy_pass http://badenleg_app;
        # ... proxy settings ...
    }
}
```

## Troubleshooting

### Common Issues

1. **Application won't start**:
```bash
# Check logs
sudo journalctl -u badenleg -n 50

# Check permissions
ls -la /path/to/badenleg

# Test manually
source venv/bin/activate
python app.py
```

2. **502 Bad Gateway**:
```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Check Gunicorn logs
sudo journalctl -u badenleg -f

# Test Gunicorn directly
curl http://127.0.0.1:8000
```

3. **Rate Limiting Issues**:
```bash
# Check Redis connection
redis-cli ping

# Monitor Redis
redis-cli monitor
```

4. **Memory Issues**:
```bash
# Check memory usage
free -h

# Monitor per-process
ps aux --sort=-%mem | head

# Restart if needed
sudo systemctl restart badenleg
```

## Post-Deployment Testing

### Checklist

- [ ] Visit https://badenleg.ch (HTTPS works)
- [ ] Test address autocomplete
- [ ] Test registration flow
- [ ] Test email confirmation (check logs)
- [ ] Test unsubscribe
- [ ] Verify rate limiting (make 60+ requests quickly)
- [ ] Check security headers: https://securityheaders.com/
- [ ] Check SSL configuration: https://www.ssllabs.com/ssltest/
- [ ] Verify GDPR compliance pages (/impressum, /datenschutz)
- [ ] Monitor logs for errors
- [ ] Test from mobile devices
- [ ] Verify map functionality

### Security Testing

```bash
# Test rate limiting
for i in {1..100}; do curl https://badenleg.ch/api/suggest_addresses?q=Baden; done

# Test invalid inputs
curl -X POST https://badenleg.ch/api/check_potential \
  -H "Content-Type: application/json" \
  -d '{"address":"<script>alert(1)</script>"}'

# Test security headers
curl -I https://badenleg.ch
```

## Rollback Plan

If issues arise:

1. **Quick rollback**:
```bash
sudo systemctl stop badenleg
# Deploy previous version
sudo systemctl start badenleg
```

2. **With Docker**:
```bash
docker-compose down
# Switch to previous image/tag
docker-compose up -d
```

3. **Database rollback** (if using persistent storage):
```bash
# Restore from backup
cp /backups/badenleg/database_TIMESTAMP.db /path/to/badenleg/database.db
sudo systemctl restart badenleg
```

## Maintenance

### Regular Tasks

- **Daily**: Monitor logs for errors
- **Weekly**: Review security log for suspicious activity
- **Monthly**: Review and update dependencies
- **Quarterly**: Security audit
- **Yearly**: Review and update SSL certificates (automated with Let's Encrypt)

### Updates

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Test in staging first!
# Then deploy to production

# Restart service
sudo systemctl restart badenleg
```

## Support

For deployment support:
- Email: hallo@badenleg.ch
- Check SECURITY.md for security issues
- Review logs in `/path/to/badenleg/badenleg_security.log`

---

Last updated: November 2024

