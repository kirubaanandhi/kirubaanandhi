# 🎬 FitBuddy - Demo Video Script & Presentation Guide

**Project Title:** FitBuddy: AI-Powered Personalized Workout & Nutrition Planner  
**Tech Stack:** FastAPI, Google Gemini 1.5 Pro, Google Gemini 1.5 Flash, SQLite / SQLAlchemy, Jinja2, HTML5 & CSS  
**Target Duration:** ~3 Minutes 30 Seconds  
* **Part 1 (Codebase Walkthrough):** ~10–15 Seconds per Code File (~1 Min 50 Secs Total)  
* **Part 2 (Web Dashboard & Live Demo):** ~1 to 2 Minutes (~1 Min 30 Secs Total)  

---

## ⏱️ Video Structure & Timeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FITBUDDY DEMO VIDEO TIMELINE                          │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ PART 1: CODEBASE (10-15s PER FILE)   │ PART 2: WEB DASHBOARD (1 TO 2 MINS)  │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 0:00 - 0:10 : Quick Intro (10s)      │ 2:00 - 2:20 : Home Page & Input Form │
│ 0:10 - 0:22 : main.py (12s)          │ 2:20 - 2:45 : AI Plan & Nutrition UI │
│ 0:22 - 0:34 : schemas.py (12s)       │ 2:45 - 3:10 : Dynamic Feedback Loop  │
│ 0:34 - 0:46 : database.py (12s)      │ 3:10 - 3:30 : Admin Dashboard & Docs │
│ 0:46 - 0:58 : gemini_generator (12s) │                                      │
│ 0:58 - 1:10 : gemini_flash (12s)     ├──────────────────────────────────────┤
│ 1:10 - 1:22 : updated_plan.py (12s)  │ OUTRO                                │
│ 1:22 - 1:34 : nutrition.py (12s)     ├──────────────────────────────────────┤
│ 1:34 - 1:46 : routes.py (12s)        │ 3:30 - 3:40 : Summary & Wrap-Up(10s) │
│ 1:46 - 2:00 : Templates & UI (14s)   │                                      │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

# 💻 PART 1: CODEBASE WALKTHROUGH (10 to 15s Per File)

---

### 🎙️ Video Opening (0:00 – 0:10 | 10s)
* **Screen:** VS Code showing the full project tree with the Uvicorn dev server running in the terminal.
* **Voiceover:**
  > *"Welcome to the demo of **FitBuddy** — an AI-powered fitness and nutrition companion built with FastAPI and Google Gemini models. We'll start with a fast 10-to-15-second walkthrough of each code module, followed by a live tour of the web dashboard!"*

---

### 📄 1. `app/main.py` (0:10 – 0:22 | 12s)
* **Screen:** Open [app/main.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/main.py). Highlight lines 6–25 (FastAPI initialization, static mount, router inclusion).
* **Voiceover:**
  > *"`main.py` is the application entry point. It instantiates FastAPI, mounts the static assets directory for styling, registers all web and API routes, and configures the local Uvicorn development server on port 8000."*

---

### 📄 2. `app/schemas.py` (0:22 – 0:34 | 12s)
* **Screen:** Open [app/schemas.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/schemas.py). Highlight `UserInput`, `FeedbackRequest`, and `WorkoutRequest` models.
* **Voiceover:**
  > *"`schemas.py` defines our Pydantic data schemas. It guarantees strict type validation for incoming user parameters like age, weight, fitness goals, intensity levels, and user feedback across web forms and REST endpoints."*

---

### 📄 3. `app/database.py` (0:34 – 0:46 | 12s)
* **Screen:** Open [app/database.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/database.py). Highlight the `User` and `WorkoutPlan` models, plus `save_user` and `update_plan` helper functions.
* **Voiceover:**
  > *"`database.py` handles SQLite persistence using SQLAlchemy ORM. It manages the `User` and `WorkoutPlan` tables, providing automated CRUD utilities to store initial plans, update revised routines, and fetch user records."*

---

### 📄 4. `app/gemini_generator.py` (0:46 – 0:58 | 12s)
* **Screen:** Open [app/gemini_generator.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/gemini_generator.py). Highlight `generate_workout_gemini()`.
* **Voiceover:**
  > *"`gemini_generator.py` integrates **Google Gemini 1.5 Pro**. It injects user demographics into a structured prompt to generate a full 7-day workout routine complete with daily warmups, sets, reps, and cooldowns."*

---

### 📄 5. `app/gemini_flash_generator.py` (0:58 – 1:10 | 12s)
* **Screen:** Open [app/gemini_flash_generator.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/gemini_flash_generator.py). Highlight `generate_nutrition_tip_with_flash()`.
* **Voiceover:**
  > *"`gemini_flash_generator.py` leverages **Google Gemini 1.5 Flash** for rapid, low-latency inference. It generates customized nutritional strategies, hydration targets, and recovery tips tailored to the user's specific fitness goal."*

---

### 📄 6. `app/updated_plan.py` (1:10 – 1:22 | 12s)
* **Screen:** Open [app/updated_plan.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/updated_plan.py). Highlight `update_workout_plan()`.
* **Voiceover:**
  > *"`updated_plan.py` powers the adaptive feedback loop. It takes the user's existing routine alongside natural language feedback and prompts Gemini to contextually rewrite specific days while preserving the rest of the plan."*

---

### 📄 7. `app/nutrition.py` (1:22 – 1:34 | 12s)
* **Screen:** Open [app/nutrition.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/nutrition.py). Highlight `calculate_macros()`.
* **Voiceover:**
  > *"`nutrition.py` offers deterministic nutritional calculations. It computes daily caloric maintenance targets, macronutrient distributions for protein, carbs, and fats, and baseline water intake based on body weight and fitness objectives."*

---

### 📄 8. `app/routes.py` (1:34 – 1:46 | 12s)
* **Screen:** Open [app/routes.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/routes.py). Highlight `@router.post("/generate-workout")`, `@router.post("/submit-feedback")`, and REST endpoints.
* **Voiceover:**
  > *"`routes.py` is the application controller. It connects Jinja2 templates, orchestrates AI generation pipelines and database transactions, and exposes REST API endpoints for seamless external integrations."*

---

### 📄 9. Frontend Templates & CSS (1:46 – 2:00 | 14s)
* **Screen:** Quick tab switch between [templates/index.html](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/templates/index.html), [templates/result.html](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/templates/result.html), and [templates/all_users.html](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/templates/all_users.html).
* **Voiceover:**
  > *"Our frontend is rendered using Jinja2 with modern glassmorphism styling — featuring an intuitive intake form in `index.html`, interactive plan visualization in `result.html`, and a full admin management table in `all_users.html`."*

---

# 🌐 PART 2: WEB DASHBOARD WALKTHROUGH (1 to 2 Minutes Total)

---

### 🖥️ 1. Homepage & User Profile Generation (2:00 – 2:20 | 20s)
* **Screen:** Browser at `http://127.0.0.1:8000/`.
* **Action:**
  1. Showcase the responsive, modern UI with input cards.
  2. Fill in sample inputs:
     * **Full Name:** `Alex Morgan`
     * **User ID:** `101`
     * **Age:** `26`
     * **Weight:** `72.5` kg
     * **Goal:** `Muscle gain and upper body strength`
     * **Intensity:** `High`
  3. Click **[Generate Plan 🚀]**.
* **Voiceover (20s):**
  > *"Now, let's switch to the live web dashboard! On the homepage, users enter their profile details — name, ID, age, weight, target goal, and intensity level. Clicking 'Generate Plan' validates the data with FastAPI and immediately triggers our dual-AI generation pipeline."*

---

### 🖥️ 2. AI Plan Generation & Nutrition Dashboard (2:20 – 2:45 | 25s)
* **Screen:** Browser on `/generate-workout` (`result.html`).
* **Action:**
  1. Scroll through the **User Info** badges at the top.
  2. Scroll down the **7-Day Workout Routine** (show Monday–Sunday with warmups, exercises, sets/reps, cooldowns).
  3. Highlight the highlighted **AI Nutrition & Recovery Guide** box.
* **Voiceover (25s):**
  > *"Within seconds, the result dashboard displays a complete, tailored fitness blueprint. Gemini 1.5 Pro structures a periodized 7-day routine tailored for high-intensity muscle hypertrophy, while Gemini Flash provides fast nutritional advice on protein timing and recovery. The profile and workout are automatically saved to SQLite."*

---

### 🖥️ 3. Natural Language Feedback & Plan Refinement (2:45 – 3:10 | 25s)
* **Screen:** Scroll down to the **Share Your Feedback** section on `result.html`.
* **Action:**
  1. In the feedback input box, type:  
     `"Please add 15 minutes of core yoga on Day 4, and swap barbell curls for neutral-grip dumbbells due to wrist strain."`
  2. Click **[Submit Feedback & Update Plan ⚡]**.
  3. Point out the green banner: `✅ Your plan has been updated based on your feedback!`.
  4. Scroll down to show the modified workout routine showing the new exercises.
* **Voiceover (25s):**
  > *"FitBuddy is conversational and adaptive. If the user has constraints or preferences — like adding yoga on Day 4 or modifying an exercise due to wrist discomfort — they simply submit their feedback. Gemini 1.5 Pro dynamically recalculates and updates the schedule in real-time while updating the database record."*

---

### 🖥️ 4. Admin Dashboard & Swagger API Docs (3:10 – 3:30 | 20s)
* **Screen:**
  1. Click **[👥 Admin Dashboard]** in navigation (`/view-all-users`).
  2. Show user row `Alex Morgan` with both **Original Plan** and **Updated Plan** side-by-side.
  3. Open a new browser tab to `http://127.0.0.1:8000/docs` (FastAPI Swagger UI).
* **Voiceover (20s):**
  > *"From the Admin Dashboard, we can inspect all registered members and compare their Original and AI-Updated workout plans side-by-side. Additionally, FastAPI automatically provides interactive Swagger API documentation at `/docs`, enabling simple mobile and microservice integrations."*

---

### 🎯 Outro & Wrap-Up (3:30 – 3:40 | 10s)
* **Screen:** FitBuddy homepage or summary slide.
* **Voiceover (10s):**
  > *"FitBuddy combines FastAPI, Google Gemini 1.5 Pro, and Flash into an intuitive, AI-driven fitness coaching platform. Thank you for watching!"*

---

## 📋 Presenter Cue Card & Timing Table

| Timestamp | Section | Key Screen / File | Duration |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:10** | Intro | IDE File Tree | 10s |
| **0:10 - 0:22** | Code: `main.py` | [app/main.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/main.py) | 12s |
| **0:22 - 0:34** | Code: `schemas.py` | [app/schemas.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/schemas.py) | 12s |
| **0:34 - 0:46** | Code: `database.py` | [app/database.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/database.py) | 12s |
| **0:46 - 0:58** | Code: `gemini_generator.py` | [app/gemini_generator.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/gemini_generator.py) | 12s |
| **0:58 - 1:10** | Code: `gemini_flash_generator.py` | [app/gemini_flash_generator.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/gemini_flash_generator.py) | 12s |
| **1:10 - 1:22** | Code: `updated_plan.py` | [app/updated_plan.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/updated_plan.py) | 12s |
| **1:22 - 1:34** | Code: `nutrition.py` | [app/nutrition.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/nutrition.py) | 12s |
| **1:34 - 1:46** | Code: `routes.py` | [app/routes.py](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/app/routes.py) | 12s |
| **1:46 - 2:00** | Code: Templates & UI | [templates/](file:///c:/Users/SURYA/OneDrive/Desktop/fitbuddy/templates) | 14s |
| **2:00 - 2:20** | Web: Home & Input Form | `http://127.0.0.1:8000/` | 20s |
| **2:20 - 2:45** | Web: 7-Day Plan & Nutrition | `http://127.0.0.1:8000/generate-workout` | 25s |
| **2:45 - 3:10** | Web: Feedback Refinement | `/submit-feedback` | 25s |
| **3:10 - 3:30** | Web: Admin & Swagger API | `/view-all-users` & `/docs` | 20s |
| **3:30 - 3:40** | Outro | Summary Slide / Home | 10s |

---

## 🎥 Recording & Presentation Tips

1. **Resolution & Zoom:** Set VS Code editor font size to `16px` or `18px` and browser zoom to `110%` for crisp readability on video recordings.
2. **Pre-populate Data:** Have the demo values (`Alex Morgan`, `101`, `26`, `72.5`, etc.) copied or ready so form entry takes less than 5 seconds.
3. **Pacing:** Speak clearly at a moderate pace (~130-140 words per minute) to match the 10-15s per-file allocations.
4. **Tabs Pre-opened:** Keep tabs for `index.html`, `result.html`, `all_users.html`, and `http://127.0.0.1:8000/docs` ready in your browser.
