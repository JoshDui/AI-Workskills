---
name: deploy-checklist
description: Use when deploying a web application and the user wants a deployment checklist, environment checks, health checks, auth flow verification, or deploy troubleshooting.
---

# Deploy Checklist

Use this skill when deploying a web application to any environment.

## Steps

1. **Confirm target environment** â€” Ask the user: local, VPS, Render, Vercel, or other?
2. **Check configuration files**:
   - Database connection strings (correct host, credentials, DB name)
   - CORS / allowed origins match the frontend URL
   - CSRF trusted origins include the frontend domain
   - Proxy rewrites (vercel.json, nginx config) point to the correct backend
3. **Check environment variables** â€” Ensure secrets are in env vars, not hardcoded
4. **Deploy** â€” Run the deployment command for the target platform
5. **Health checks** â€” After deployment:
   - Curl the API health/root endpoint
   - Curl the frontend root
   - Check for CORS headers in responses
6. **Test auth flow** â€” Login, verify session/cookie, hit a protected route
7. **Report results** â€” Show which checks passed/failed and fix any failures
8. **Loop** â€” If any check fails: read logs, diagnose, fix, redeploy, re-check

## Common Issues to Watch For
- CORS misconfiguration (missing origins, wrong protocol http vs https)
- Cookie/session not persisting across domains (SameSite, Secure flags)
- Database migrations not run on deploy
- Static files not collected/built
- Cold start timeouts on Render free tier
