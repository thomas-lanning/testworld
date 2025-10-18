# Security Guide

## ⚠️ Important: Exposed Credentials

Your Supabase credentials were previously committed to git. Follow these steps to secure your project:

## Immediate Actions Required

### 1. Rotate Your Supabase Keys (Recommended)

Go to your Supabase dashboard and regenerate your anon key:
1. Visit https://supabase.com/dashboard/project/pfrwbbcssuxcjayhsulj/settings/api
2. Click "Reset" on the anon/public key
3. Update your local `.env` file with the new key
4. Update `.env.local` with the new key

### 2. Remove from Git History

The `.env` files have been removed from git tracking, but they still exist in your git history. To completely remove them:

```bash
# WARNING: This rewrites git history - coordinate with collaborators first!

# Install git-filter-repo (if not installed)
# brew install git-filter-repo  # on Mac
# or pip install git-filter-repo

# Remove .env files from all history
git filter-repo --path .env --invert-paths
git filter-repo --path python_api/.env --invert-paths
git filter-repo --path supabase/functions/generate-entity/.env --invert-paths

# Force push to GitHub (WARNING: This is destructive!)
git push origin main --force
```

**Alternative (simpler but nuclear):**
If this is a new project with no important history, consider:
1. Delete the GitHub repo
2. Create a new repo
3. Push fresh code without sensitive files

### 3. Enable Row Level Security (RLS) Policies

Your database currently allows public access! Fix this:

```sql
-- Go to Supabase SQL Editor and run:

-- Revoke public access
DROP POLICY IF EXISTS "Allow public read on companies" ON public.companies;
DROP POLICY IF EXISTS "Allow public insert on companies" ON public.companies;
DROP POLICY IF EXISTS "Allow public update on companies" ON public.companies;
DROP POLICY IF EXISTS "Allow public delete on companies" ON public.companies;

DROP POLICY IF EXISTS "Allow public read on relationships" ON public.relationships;
DROP POLICY IF EXISTS "Allow public insert on relationships" ON public.relationships;
DROP POLICY IF EXISTS "Allow public update on relationships" ON public.relationships;
DROP POLICY IF EXISTS "Allow public delete on relationships" ON public.relationships;

DROP POLICY IF EXISTS "Allow public read on projects" ON public.projects;
DROP POLICY IF EXISTS "Allow public insert on projects" ON public.projects;
DROP POLICY IF EXISTS "Allow public update on projects" ON public.projects;
DROP POLICY IF EXISTS "Allow public delete on projects" ON public.projects;

-- Add authenticated-only policies (or customize as needed)
CREATE POLICY "Authenticated users can read companies" ON public.companies
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can insert companies" ON public.companies
    FOR INSERT WITH CHECK (true);

-- Repeat for relationships and projects...
```

## What Was Exposed

### Public Information (Safe)
- ✅ Supabase anon/publishable key - Designed to be public
- ✅ Supabase URL - Also meant to be public
- ✅ Project ID - Public by design

### Security Issue
- ❌ **Your database has NO authentication**
  - Anyone with your URL can read all data
  - Anyone can create, modify, or delete records
  - No user-level permissions

## Best Practices Going Forward

### 1. Never Commit Secrets

**Never commit:**
- `.env` files
- API keys (especially service_role keys!)
- Database passwords
- OAuth secrets
- Private keys

**Always use:**
- `.env.example` as templates
- `.gitignore` to exclude sensitive files
- Environment variables for secrets

### 2. File Checklist

Before committing, check for:
- [ ] No `.env` files
- [ ] No hardcoded API keys in code
- [ ] No passwords or tokens in comments
- [ ] `.gitignore` is up to date

### 3. GitHub Scanning

GitHub has secret scanning. Check:
- Your repository's Security tab
- Enable Dependabot alerts
- Review any security warnings

## Environment Variable Structure

### Local Development
Use `.env.local` (not tracked by git):
```env
VITE_SUPABASE_URL=http://127.0.0.1:54321
VITE_SUPABASE_PUBLISHABLE_KEY=local-dev-key
```

### Production
Use environment variables in your hosting platform:
- Vercel: Project Settings → Environment Variables
- Netlify: Site Settings → Environment Variables
- Never commit production keys!

## Risk Assessment

### Current Risk: MEDIUM

**Why not HIGH?**
- The exposed key is the "anon" key (designed for frontend)
- You're not storing sensitive user data yet
- Project appears to be in development phase

**Why MEDIUM?**
- Database has no authentication (anyone can write/delete)
- Could be spammed or abused
- Data is publicly modifiable

### After Fixes: LOW
Once you:
1. ✅ Add proper RLS policies
2. ✅ Rotate keys (optional but recommended)
3. ✅ Remove from git history
4. ✅ Never commit .env again

## Need Help?

- [Supabase RLS Documentation](https://supabase.com/docs/guides/auth/row-level-security)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Git Filter Repo](https://github.com/newren/git-filter-repo)

## Summary

✅ **Immediate fixes applied:**
- Added `.env` to `.gitignore`
- Removed `.env` files from git tracking
- Created `.env.example` template
- Created this security guide

⚠️ **You still need to:**
- Consider rotating your Supabase keys
- Remove `.env` from git history (optional but recommended)
- Add proper authentication/RLS policies to your database
- Never commit `.env` files again!
