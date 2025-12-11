---
description: How to deploy the full-stack VibeSnack application to Vercel
---

# Deploy VibeSnack to Vercel

This workflow guides you through deploying your React Frontend + FastAPI Backend application to Vercel.

## Prerequisites

1.  A [Vercel Account](https://vercel.com).
2.  A [GitHub Account](https://github.com).
3.  A MongoDB Atlas Database (for the backend).

## Preparation (Already Done by Agent)

The following configurations have been applied to your project:
- `vercel.json`: Configures routing for `/api` to the backend and everything else to the frontend.
- `api/index.py`: Serverless entry point for FastAPI.
- `package.json`: Root build script to trigger frontend build.
- `requirements.txt`: Combined Python dependencies.
- `frontend/src/App.jsx`: Configured to use `/api` path in production.
- `backend/main.py`: Configured to handle `/api` root path on Vercel.

## Step 1: Push to GitHub

1.  Create a new repository on GitHub.
2.  Push your code to the repository.

```bash
git init
git add .
git commit -m "Prepare for Vercel deployment"
# Replace <your-repo-url> with your actual repository URL
# git remote add origin <your-repo-url>
# git push -u origin main
```

## Step 2: Deploy on Vercel

1.  Log in to your Vercel Dashboard.
2.  Click **"Add New..."** -> **"Project"**.
3.  Import your GitHub repository.
4.  **Configure Project**:
    *   **Framework Preset**: Vite (should be detected automatically).
    *   **Root Directory**: Keep it as `./` (Root).
    *   **Build Command**: `cd frontend && npm install && npm run build` (Should be detected from root package.json if present, otherwise enter manually).
    *   **Output Directory**: `frontend/dist` (IMPORTANT: You might need to override this in the settings).
5.  **Environment Variables**:
    *   Add `MONGODB_URI` with your connection string.
    *   Add `VERCEL=1` (Vercel adds this automatically, but good to double check if needed for logic).
6.  Click **Deploy**.

## Step 3: Verify

1.  Once deployed, visit your Vercel URL.
2.  The frontend should load.
3.  Try to generate a recommendation. This will call `/api/predict`.
4.  If successful, the backend is working!

## Troubleshooting

-   **404 on API**: Check `vercel.json` rewrites and `api/index.py`.
-   **500 on API**: Check Function Logs in Vercel Dashboard > Logs. Often due to missing env vars (MONGODB_URI) or missing dependencies in `requirements.txt`.
