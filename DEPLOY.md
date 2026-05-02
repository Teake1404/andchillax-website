# 🚀 Deployment Guide — And Chillax Website

**Goal:** Get this website live at `andchillax.co.uk`, off Wix, on free hosting, with a CMS Eva can use to publish blog posts.

**Time required:** 60-90 minutes (one-off setup). Then maintenance is the same as Wix.

**Cost:** £0/month forever. (Saves £10-25/month vs. Wix.)

---

## 📋 What you'll have when this is done

- ✅ Site live at `https://www.andchillax.co.uk` (same domain Eva already owns)
- ✅ Auto-deploys whenever any file changes (no FTP, no fuss)
- ✅ Decap CMS at `andchillax.co.uk/admin` so Eva can publish blog posts via a web UI
- ✅ Bookwhen booking embedded on every course page
- ✅ Schema markup for the 5★ Google reviews badge
- ✅ Free SSL certificate (the green padlock)
- ✅ Page loads in <1 second (vs Wix's 3-5 seconds — major SEO win)
- ✅ Wix subscription cancelled

---

## 🛠 Prerequisites — what you need to know before starting

1. **GitHub account** (free) — sign up at github.com if you don't have one
2. **Netlify account** (free) — sign up at netlify.com (use the same email as GitHub for simplicity)
3. **Domain access** — you need to be able to update DNS records for `andchillax.co.uk`. This is wherever Eva registered the domain (could be Wix itself, GoDaddy, 123-Reg, etc.)
4. **A Bookwhen account** — sign up at bookwhen.com (free) before launch so the booking embeds work

---

## Phase 1: Push the site to GitHub (15 mins)

### Step 1.1 — Create a GitHub repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `andchillax-website`
3. **Public** (Decap CMS works with public repos for free; private requires a paid Netlify plan)
4. Don't initialise with README/license — we already have files
5. Click **Create repository**

### Step 1.2 — Push these files to GitHub

Open Terminal (on Mac) or Git Bash (on Windows). Run these commands one at a time, replacing `YOUR_USERNAME` with your actual GitHub username:

```bash
# Navigate to the website folder
cd /Users/shuqingke/Documents/ewa_project/website

# Initialise git
git init -b main

# Configure your identity (only needed once per machine)
git config user.email "your@email.com"
git config user.name "Your Name"

# Stage and commit all files
git add .
git commit -m "Initial site upload"

# Connect to GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/andchillax-website.git
git push -u origin main
```

If git asks for a password, use a **Personal Access Token** (Settings → Developer Settings → Personal Access Tokens → Generate new token, classic, with `repo` scope).

### Step 1.3 — Verify

Refresh `github.com/YOUR_USERNAME/andchillax-website` — you should see all the files.

---

## Phase 2: Deploy to Netlify (10 mins)

### Step 2.1 — Create a Netlify site from the GitHub repo

1. Go to [app.netlify.com](https://app.netlify.com) and sign in
2. Click **Add new site → Import an existing project**
3. Choose **GitHub** as the Git provider (authorise Netlify if asked)
4. Select your `andchillax-website` repo
5. Build settings — leave defaults (publish directory: `.`, no build command needed). The `netlify.toml` file already configures everything.
6. Click **Deploy site**

Wait ~30 seconds. You'll see "Site is live" with a temporary URL like `random-name-123.netlify.app`. **Open that URL — the site should work end-to-end.** Click around, check the homepage, check a course page, check the blog. Everything should look pixel-identical to the local mockup.

### Step 2.2 — Rename the Netlify site (optional but tidy)

Site Settings → Site information → **Change site name** → set to `andchillax` (so the temporary URL becomes `andchillax.netlify.app`).

---

## Phase 3: Connect the andchillax.co.uk domain (15-30 mins)

### Step 3.1 — Add the custom domain in Netlify

1. In Netlify: **Domain settings → Custom domains → Add a domain**
2. Enter `andchillax.co.uk`
3. Netlify will show DNS records you need to set

### Step 3.2 — Update DNS at her registrar

Wherever Eva's domain is registered (check by running `whois andchillax.co.uk` or asking her), log in and change DNS records:

**For root domain (`andchillax.co.uk`):**
- Type: A record · Name: `@` · Value: `75.2.60.5` (Netlify's load balancer)

**For www subdomain (`www.andchillax.co.uk`):**
- Type: CNAME · Name: `www` · Value: `andchillax.netlify.app`

> 💡 **Wix DNS notice:** If the domain is registered through Wix Premium, you'll need to either (a) keep paying Wix just for the domain at ~£10/year (cheapest option), or (b) transfer it out to a registrar like Cloudflare (free), Namecheap (~£8/year), or 123-Reg. Transferring takes 5-7 days. For first launch, just point DNS — transfer later if you want to fully exit Wix.

### Step 3.3 — Wait for DNS to propagate

Usually 10-30 mins, can take up to 48 hours. Check status with `dig andchillax.co.uk` or [whatsmydns.net](https://www.whatsmydns.net). When DNS resolves to Netlify, the site goes live at the real domain.

### Step 3.4 — Enable HTTPS (Netlify does this automatically)

Netlify will auto-provision a free SSL certificate via Let's Encrypt within minutes of DNS propagating. **Force HTTPS** in Netlify Domain Settings (toggle).

---

## Phase 4: Set up the CMS so Eva can edit blog posts (15 mins)

### Step 4.1 — Enable Netlify Identity

1. Netlify Site → **Site settings → Identity → Enable Identity**
2. Set **Registration preferences** to **Invite only** (so randos can't create accounts)
3. **Services → Git Gateway → Enable Git Gateway** (this lets the CMS commit to GitHub)

### Step 4.2 — Invite Eva as an admin

1. Netlify Identity → **Invite users** → enter `eva@andchillax.co.uk`
2. She'll get an email with a "Set your password" link
3. After she sets her password, she can log in at `https://www.andchillax.co.uk/admin`

### Step 4.3 — Test the CMS

1. Log in to `andchillax.co.uk/admin` yourself first to verify it works
2. Click **Blog → New Blog Post**
3. Fill in title, body, etc., publish
4. Wait ~30 seconds — the post appears live on `/blog/`

If everything works, hand the credentials to Eva.

---

## Phase 5: Set up Bookwhen embedding (15 mins)

### Step 5.1 — Sign up at bookwhen.com (if not done already)

1. [bookwhen.com](https://bookwhen.com) → free account
2. Account name: `andchillax` (so the URL is `bookwhen.com/andchillax`)
3. Connect Stripe for payments

### Step 5.2 — Create one schedule per course

In Bookwhen, create a "Schedule" for each:

- 12-Hour Paediatric Blended (open courses)
- 6-Hour Paediatric First Aid (open courses)
- 2-Hour Parent First Aid (private + group)
- Online 1-Hour Parent First Aid
- 1-Day EFAW (open courses)
- Anaphylaxis (open courses)

For 2-Day FAW, 3-Day FAW, and First Aid for Schools — use **Bookings on Request** mode (no fixed dates, prospects request a quote).

### Step 5.3 — Replace the embed placeholders

Each course page has a placeholder block like this:

```html
<div class="bookwhen-embed__placeholder">
  <strong>Bookwhen calendar embeds here</strong>
  ...
</div>
```

Replace it with the iframe from your Bookwhen Embed tab:

```html
<iframe src="https://bookwhen.com/andchillax?embed=true"
        width="100%" height="800" frameborder="0"></iframe>
```

For schedule-specific filtering, use:
```html
<iframe src="https://bookwhen.com/andchillax?embed=true&ical_filter=parent-first-aid"
        width="100%" height="800" frameborder="0"></iframe>
```

Edit the relevant HTML files in the GitHub repo (you can do this via GitHub's web UI — no Terminal needed) and Netlify auto-redeploys within 30 seconds.

---

## Phase 6: SEO + analytics setup (15 mins)

### Step 6.1 — Submit sitemap to Google Search Console

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add property: `https://www.andchillax.co.uk`
3. Verify via DNS or HTML file (Netlify makes the latter trivial)
4. **Sitemaps → Add new sitemap → `sitemap.xml`** (this file is already in your repo at the root)

### Step 6.2 — Set up Google Analytics 4

1. [analytics.google.com](https://analytics.google.com) → Create property
2. Get the `G-XXXXXXX` measurement ID
3. Add to Netlify Custom Code (or paste the GA4 snippet inside `<head>` in your HTML files)

### Step 6.3 — Set up Bing Webmaster Tools (worth doing)

1. [bing.com/webmasters](https://www.bing.com/webmasters) → import from GSC (one click)
2. Submit sitemap

---

## Phase 7: Cancel Wix (after launch is verified)

**Don't cancel Wix until everything works at andchillax.co.uk for at least 48 hours.**

Once site is verified:
1. Wix Dashboard → Account & Billing
2. Cancel any premium subscriptions
3. **Don't delete the Wix site** for at least 30 days — keep it as backup

---

## 🔁 Ongoing maintenance — how Eva updates the site

### Adding a new blog post (Eva, 30 mins)
1. Go to `andchillax.co.uk/admin`
2. Log in
3. Blog → New Post
4. Type the post, add image, set category, choose related course CTA
5. Save & Publish
6. Live within 30 seconds

### Editing course prices or page text (Shuqing or freelancer, 10 mins)
1. GitHub → andchillax-website → find the relevant `.html` file
2. Click the pencil icon (web editor)
3. Edit the price or text
4. Commit changes
5. Live within 30 seconds

### Adding photos
1. Bookwhen handles course photos automatically
2. Site photos: upload via the CMS admin, or via GitHub → `assets/uploads/`

---

## 🚨 Troubleshooting

**Site shows "Page not found" at andchillax.co.uk:**
DNS hasn't propagated yet. Wait 30 mins. Check with [whatsmydns.net](https://www.whatsmydns.net).

**Site shows certificate warning:**
Wait 10-15 mins after DNS propagation. Netlify auto-provisions Let's Encrypt cert.

**CMS shows "401" or won't log in:**
Re-check Netlify Identity → Git Gateway is enabled. Re-invite the user.

**Blog post saved in CMS but not appearing on site:**
Check Netlify deploy log — usually a typo in frontmatter. Roll back to last good commit.

**Old Wix URLs returning errors:**
The `_redirects` file already handles common ones. Add new redirects to that file for any URL that 404s.

---

## ✅ Launch checklist (use this on launch day)

- [ ] All HTML pages load at `andchillax.netlify.app/*`
- [ ] DNS propagated — site loads at `andchillax.co.uk`
- [ ] HTTPS working (green padlock)
- [ ] CMS works at `/admin` — Eva can log in
- [ ] Bookwhen iframes embedded on at least 3 flagship courses
- [ ] Sitemap submitted to Google Search Console
- [ ] Google Analytics installed
- [ ] Email forwarding for `eva@andchillax.co.uk` still working (test by sending one)
- [ ] Old Wix URLs redirect (test 3-4 of them)
- [ ] LocalBusiness schema validates ([Google Rich Results Test](https://search.google.com/test/rich-results))
- [ ] Wix subscription cancelled (only after 48 hrs of verified live operation)

---

## 📊 What changes for Eva after launch

| Task | Wix today | New site |
|---|---|---|
| Edit blog post | Wix dashboard | `/admin` (similar UI) |
| Add new blog post | Wix dashboard | `/admin` |
| Edit course price | Wix editor (visual) | Email Shuqing (or self-edit on GitHub) |
| Add new course page | Wix editor (full rebuild) | Copy template + email Shuqing |
| Update photos | Wix media manager | `/admin` upload OR GitHub |
| See visitor stats | Wix Analytics | Google Analytics 4 |
| Take bookings | Manual email (broken) | Bookwhen embedded — automated |
| Speed | 3-5 seconds | Under 1 second |
| Monthly cost | £10-25 | **£0** |

---

## 🎁 What this whole thing costs to maintain (forever)

| Item | Cost |
|---|---|
| Domain (andchillax.co.uk) | She already pays this — typically £10-15/year |
| Netlify hosting | £0 (free tier covers ~100GB bandwidth/month — way more than she needs) |
| GitHub | £0 |
| Bookwhen | £0 (free tier: up to 50 bookings/month) |
| Decap CMS | £0 |
| Netlify Identity | £0 (free up to 1,000 users) |
| SSL certificate | £0 (auto-provisioned) |
| Google Analytics + Search Console | £0 |
| **TOTAL** | **£0/month + ~£12/year for domain** |

---

*Last updated: 2 May 2026*
