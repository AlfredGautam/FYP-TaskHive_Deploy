# TaskHive — Railway Deployment Guide

## What was fixed before deploying

- **Google OAuth redirect URI** (`core/views/auth.py`): Was hardcoded to `http://127.0.0.1:8000/...`. Now reads from `SITE_URL` env var so it works correctly on Railway.
- **`railway.json`**: Updated start command to include `migrate` + `collectstatic` before starting Daphne (matches `railway.toml`).

---

## Step 1 — Push your code to GitHub

Make sure your latest code is committed and pushed. Railway deploys from GitHub.

```bash
cd FYP-TaskHive
git add .
git commit -m "fix: Google OAuth redirect URI + railway config"
git push
```

---

## Step 2 — Create a Railway project

1. Go to [railway.app](https://railway.app) and sign in.
2. Click **New Project → Deploy from GitHub repo**.
3. Select your repository.
4. Railway will auto-detect the `railway.toml` and start building.

---

## Step 3 — Add PostgreSQL

1. In your Railway project dashboard, click **+ New Service → Database → PostgreSQL**.
2. Railway automatically injects `DATABASE_URL` into your app — you do **not** need to set it manually.

---

## Step 4 — Set Environment Variables

In your Railway service, go to **Variables** and add every variable below.

| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random string — generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.up.railway.app` |
| `SITE_URL` | `https://your-app-name.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app-name.up.railway.app` |
| `EMAIL_HOST_USER` | Your Gmail address |
| `EMAIL_HOST_PASSWORD` | Your 16-char Gmail App Password (not your login password) |
| `GOOGLE_CLIENT_ID` | From Google Cloud Console (see Step 5) |
| `GOOGLE_CLIENT_SECRET` | From Google Cloud Console (see Step 5) |

> **Tip:** You'll know your Railway domain after the first deploy. It looks like `taskhive-production-xxxx.up.railway.app`. Update `ALLOWED_HOSTS`, `SITE_URL`, and `CSRF_TRUSTED_ORIGINS` once you see it.

---

## Step 5 — Update Google Cloud Console

This is required for Google OAuth to work in production.

1. Go to [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials).
2. Click your existing **OAuth 2.0 Client ID**.
3. Under **Authorized JavaScript origins**, add:
   ```
   https://your-app-name.up.railway.app
   ```
4. Under **Authorized redirect URIs**, add:
   ```
   https://your-app-name.up.railway.app/auth/google/callback/
   ```
5. Click **Save**.

> Keep the existing `http://127.0.0.1:8000/auth/google/callback/` entry so local dev still works.

---

## Step 6 — Gmail App Password (for OTP emails)

If you haven't already:

1. Go to your Google Account → Security → **2-Step Verification** (must be on).
2. Then go to **App passwords**.
3. Create a new app password for "Mail / Other (TaskHive)".
4. Use that 16-character password as `EMAIL_HOST_PASSWORD` in Railway.

---

## Step 7 — Verify deployment

After Railway finishes deploying:

1. Visit `https://your-app-name.up.railway.app/api/health/` — should return `{"status": "ok"}`.
2. Visit `https://your-app-name.up.railway.app/` — landing page should load.
3. Try registering with email — OTP email should arrive.
4. Try "Continue with Google" — should redirect to Google and come back logged in.

---

## Media files note

Railway's filesystem is ephemeral — uploaded files (profile photos, task attachments) will be **lost on redeploy**. For a production app you'd add Cloudinary or AWS S3. For a final year project demo this is acceptable as long as you don't redeploy mid-demo.

---

## Quick checklist

- [ ] Code pushed to GitHub
- [ ] PostgreSQL service added in Railway
- [ ] All 9 env vars set in Railway Variables
- [ ] Google Cloud Console redirect URI updated
- [ ] Gmail App Password set
- [ ] `/api/health/` returns OK
- [ ] Google login works end-to-end
