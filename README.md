# ERISA Recovery Dev Challenge

## 🛠️ Tech Stack
- **Backend:** Django v4+ (Python) 🐍
- **Database:** SQLite 🗄️
- **Frontend:** HTML/CSS (+ Tailwind CSS ) + HTMX 🎨
- **Client-Side:** Alpine.js (JavaScript) ⚡️


## 📋 Challenge Overview
This project is a lightweight web application that mimics insurance claim analysis at ERISA Recovery. So far, the application supports:
- [x] 📥 Data ingestion from CSV
- [x] 📄 Claims list and detail views
- [x] ⚡️ HTMX-powered dynamic detail loading
- [x] 🚩 Flagging claims for review
- [x] 📝 Adding custom notes/annotations
- [x] 🔍 Search and filter by status or insurer
- [x] (Bonus) CSV re-upload


## 🌟 Core Features (Implemented)
- **Data Ingestion:** 📥 Load claims and claim details from CSV via management command
- **Claims List View:** 📄 See all claims with ID, patient, billed/paid, status, insurer, discharge date
- **HTMX Detail View:** ⚡️ View claim details (CPT codes, denial reasons, custom notes) without full page reload
- **Flag & Annotate:** 🚩📝 Flag claims for review and add custom notes, stored in the database and dynamically updated in frontend
- **Search & Filter:** 🔍 Search by claim status or insurer name


### 🎁 Bonus Features (Some Implemented)
- [] **Admin Dashboard:** 📊 Stats like total flagged claims, average underpayment
- [x] **CSV Re-upload:** 🔄 Overwrite or append logic for data
- [] **User Authentication:** 🔐 Login system with user-specific annotations


## ⚙️ Setup Instructions

1. **Clone the Repository** 🌀
   ```sh
   git clone <your-repo-url>
   cd ERISA-Recovery-Dev-Challenge
   ```

2. **Create and Activate a Virtual Environment** 🐍
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies** 📦
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables** 🔑
   Create a `.env` file in the project root:
   ```
   DJANGO_SETTINGS_SECRET_KEY=your-secret-key-here
   ```

5. **Apply Migrations** 🗄️
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Load Claims Data** 📥
   ```sh
   python manage.py load_claims claim_list.csv
   python manage.py load_claims claim_details.csv
   ```

7. **Run the Development Server** 🚀
   ```sh
   python manage.py runserver
   ```

8. **Access the Application** 🌐
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.


## 📝 Notes
- ❗️ Do not commit your `.env` file or any real secrets to version control.
- ⚠️ For production, set `DEBUG = False` and configure `ALLOWED_HOSTS` in `settings.py`.
- 👤 Use Django admin to manage users and data: `python manage.py createsuperuser`
- ✅ For best results, use Firefox or Chrome.


## 📡 API
- The project exposes API endpoints for claims and claim details (see code for details).

## 🙏 Acknowledgements & Reflections

Thank you to ERISA for hosting this development challenge and providing a real-world scenario to grow both my technical and problem-solving skills. Through this project, I learned how to:

- Build a Django backend from scratch and design models for real data
- Use management commands to ingest and validate data from CSV files
- Create dynamic, interactive UIs using HTMX and Alpine.js (I came from a background in React)
- Implement search, filtering, and sorting logic both in the frontend and backend
- Handle user actions like flagging and annotating records in a seamless, user-friendly way
- Write clean, maintainable code and document the project for others

This challenge deepened my understanding of full-stack web development, Django’s ORM, and advanced my modern frontend techniques. I appreciate the opportunity to work on a project that simulates real insurance claim workflows and look forward to applying these skills in future projects!