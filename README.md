# 💪 Fitness Quest Tracker

A real Django web app for logging your daily fitness quest, tracking weekly points, and following your Month 1 plan + diet guide — built to run on a genuinely free hosting setup.

## 🧠 Quick concept check

**GitHub stores your code for free. It does not run your app.**
To make this a live website with a real URL, you push the code to GitHub, then connect a **hosting platform** (also free at this scale) to that GitHub repo. GitHub and the host are two separate, both-free services working together — see the deploy section below.

## ⚙️ What's inside

- ✅ Daily quest logging — walk, strength, mobility, sleep, water, protein
- ⭐ Automatic points scoring (matches the quest's points system)
- 📈 History page with pagination
- 🗓️ Built-in reference pages for the Month 1 plan and the diet guide
- 🔑 Sign up / log in — each user gets their own private log
- 🛠️ Django admin for viewing/editing data directly
- 🎨 A custom design (not default Bootstrap styling)

**Stack:** Django 6, SQLite by default, Whitenoise (serves static files in production), Gunicorn (production server), `dj-database-url` (so you can swap in a free Postgres later by setting one environment variable — no code changes).

---

## 1️⃣ Get it running locally

```bash
# unzip the project, then inside the folder:
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env            # your local settings; .env is git-ignored

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/ access
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — sign up, log today's quest, check the dashboard.

## 2️⃣ Put it on GitHub (free)

```bash
git init
git add .
git commit -m "Initial commit — fitness quest tracker"
```

Then on github.com: **New repository** → don't initialize with a README (you already have one) → copy the two commands it gives you:

```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

Your code is now on GitHub. The app itself still only runs on your own computer — that's what the next step fixes.

## 3️⃣ Deploy it for free — Render

[Render](https://render.com) offers a genuinely free tier for exactly this: connect a GitHub repo, and it builds and runs your Django app for you.

1. Sign up at render.com (no card needed for the free tier) and connect your GitHub account.
2. **New → Web Service** → pick your repo.
3. Settings:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `gunicorn fitquest.wsgi`
   - **Instance Type:** Free
4. Add environment variables (Render's **Environment** tab):
   | Key | Value |
   |---|---|
   | `SECRET_KEY` | any long random string |
   | `DEBUG` | `False` |
5. Click **Create Web Service**. First build takes a few minutes — you'll get a URL like `https://your-app.onrender.com`.

**Know before you go (free tier, honestly):**
- 🕒 The free service **sleeps after 15 minutes** with no traffic, and the next visit takes ~30–60 seconds to wake up. Normal — not a bug.
- 💾 The free tier has **no persistent disk**, so the SQLite file resets on every redeploy. Fine while you're testing solo. If you want your logs to survive redeploys, create a free permanent Postgres database at [neon.tech](https://neon.tech) or [supabase.com](https://supabase.com), then add one more environment variable on Render: `DATABASE_URL` = the connection string they give you. No code change needed — `dj-database-url` in `settings.py` already reads it.
- 🔁 Every `git push` to `main` auto-redeploys, once you connect the repo.

**Alternative:** [PythonAnywhere](https://www.pythonanywhere.com) has a Python-specific free tier with no sleep/cold-start behavior, but deployment is a manual upload/pull rather than auto-deploy from GitHub, and outbound requests are restricted on the free tier. Worth knowing about if Render's sleep behavior bothers you.

---

## 🗂️ Project layout

```
fitquest/
├── fitquest/          # project settings, root urls
├── quest/              # the app: models, views, forms, templates
│   └── templates/quest/
├── templates/registration/   # login/signup pages
├── static/css/style.css
├── requirements.txt
├── Procfile
└── manage.py
```

## 🔧 Extending it

Natural next additions, if you want to keep building: editing past log entries, a Level 2 exercise set once Month 1 is done, weight/waist tracking on the Profile model, or a small chart of points over time.
