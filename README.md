# AI CareerPilot — Your Personal AI Career Agent

**Project Owner:** Mantasha Shaikh

**Project Type:** AI-Powered Career Guidance Web Application

**Technology Stack:** Python, Flask, SQLite, HTML, CSS, JavaScript, and AI integration.
**Tagline: Analyze. Learn. Grow.**

AI CareerPilot is an AI-powered career development web application designed to help students, fresh graduates, and job seekers analyze their resumes, identify skill gaps, prepare for interviews, and build personalized career roadmaps.

The platform compares a candidate's resume with a target job description to identify matching skills, missing skills, and areas for improvement. It provides career recommendations, interview preparation resources, and learning suggestions to support continuous professional development.

Built using Python and Flask, AI CareerPilot combines a responsive purple-themed user interface, a SQLite database, resume processing, skill-matching logic, career planning tools, and an administrative dashboard in one web application.

## Key Features

- **Resume Analysis:** Upload resumes in PDF or DOCX format and extract relevant information.
- **Skill Gap Detection:** Compare resume skills with job requirements and identify missing skills.
- **Resume Match Score:** Calculate transparent skill coverage based on detected required skills.
- **AI Career Recommendations:** Generate career guidance and resume improvement suggestions when an AI provider is configured.
- **Personalized Career Roadmap:** Organize career development into manageable learning and project-building tasks.
- **Interview Preparation:** Generate technical, HR, behavioral, and problem-solving interview questions.
- **Learning Resources:** Explore learning materials and bookmark useful resources.
- **Analysis History:** Save and review previous resume analyses.
- **PDF Reports:** Download resume analysis reports.
- **User Authentication:** Support account registration, login, profile management, and password updates.
- **Admin Dashboard:** Manage users, inspect analysis metadata, view platform statistics, and review audit logs.
- **OAuth Integration:** Optional Google and GitHub authentication.
- **Responsive UI:** Access the application through desktop and mobile web browsers.
- **Local Fallback Engine:** Perform basic skill matching and use fallback interview questions without external AI credentials.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Templates | Jinja2 |
| Database | SQLite, SQLAlchemy |
| Authentication | Flask-Login, Werkzeug, Authlib |
| Resume Processing | PyMuPDF, python-docx |
| Charts | Chart.js |
| PDF Reports | ReportLab |
| Testing | pytest |
| Configuration | python-dotenv |

## How It Works

1. **Create an account:** Register or log in to the platform.
2. **Upload a resume:** Select a PDF or DOCX resume.
3. **Enter job details:** Specify the target job title, company, experience level, and job description.
4. **Analyze skills:** The application extracts resume text, detects skills, and compares them against the job requirements.
5. **Review results:** View matching skills, missing skills, coverage score, and improvement suggestions.
6. **Build a career plan:** Explore recommended learning topics, projects, and roadmap tasks.
7. **Prepare for interviews:** Generate practice questions for your target role.
8. **Track progress:** Save analyses, bookmark resources, and update roadmap tasks.

## Installation and Setup

### Prerequisites

- Python 3.10–3.12 recommended
- Visual Studio Code or another code editor
- Internet connection for installing dependencies

### Run on Windows

Clone or download the project and open its folder in the terminal.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Configure the environment variables in `.env`, then initialize the database:

```powershell
python scripts/init_db.py
```

Start the application:

```powershell
python app.py
```

Open the local address displayed in the terminal, typically:

`http://127.0.0.1:5000`

## Configuration

The application uses environment variables for secret keys, administrator initialization, AI provider configuration, and optional OAuth integrations.

Configure the following where applicable:

- `SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- AI provider and model settings

External AI and OAuth features require appropriate credentials. Never commit `.env` or private credentials to GitHub.

## Skill Coverage Calculation

The local skill-matching engine calculates skill coverage using:

**Skill Coverage (%) = (Matched Required Skills / Total Detected Required Skills) × 100**

If no required skills are detected in the job description, the application should handle that case without dividing by zero.

The score represents skill coverage against the supplied job description. It is not a probability of getting hired and does not guarantee recruitment success.

## Security

- Password hashing
- Server-side validation
- CSRF protection
- Authenticated and role-protected routes
- Resume upload validation and size limits
- User-specific analysis access
- Environment-based secrets
- Protected report downloads

Use strong credentials and change development defaults before deploying the application publicly. Security controls should be tested before production use.

## Project Structure

```text
ai-careerpilot/
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── .env.example
├── README.md
├── models/
├── routes/
├── services/
├── templates/
├── static/
├── scripts/
├── tests/
└── instance/
```

## Testing

Run the automated test suite using:

```powershell
python -m pytest -q
```

Review the test results before claiming that all features have been verified.

## Future Enhancements

- Semantic resume-to-job matching
- More advanced AI career recommendations
- Personalized learning plans
- Integration with verified job listings
- Resume version comparison
- Career analytics and progress reports
- Deployment with a production database

## Intended Audience

AI CareerPilot is designed for college students, BCA and computer science students, fresh graduates, internship applicants, and job seekers who want to improve their resumes and prepare for technical careers.

## Project Goal

The goal of AI CareerPilot is to make career preparation more organized, personalized, and accessible by combining resume analysis, skill development, interview preparation, and career planning in a single web platform.

**AI CareerPilot — Analyze. Learn. Grow.**

*Note: Feature availability depends on the implemented project code and configuration. External AI and OAuth integrations require valid credentials. This project provides career guidance and skill comparison, not guaranteed hiring outcomes.*
