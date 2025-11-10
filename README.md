# 🎯 HireIQ - Smart Recruitment Platform

AI-powered recruitment system for matching candidates with job postings, featuring intelligent resume parsing, semantic matching, and automated candidate management.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![React](https://img.shields.io/badge/react-18.0+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 📄 **Resume Upload & Parsing** - Extract text from PDF/DOCX resumes automatically
- 🎯 **Intelligent Matching** - Semantic matching with AI or keyword-based matching
- 👍 **Candidate Management** - Shortlist or reject candidates with status tracking
- 📧 **Email Notifications** - Automated emails to shortlisted candidates (optional)
- 📊 **Dashboard** - Visual analytics with application statistics
- 🎨 **Modern UI/UX** - Professional, responsive interface with smooth animations
- 💾 **SQLite Database** - Local storage for all data

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Backend runs on `http://127.0.0.1:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## 📖 Usage

1. **Upload Resumes** - Click "Upload Resume" and select PDF/DOCX files
2. **Create Job** - Enter job title and detailed description
3. **View Matches** - See all candidates ranked by match score
4. **Shortlist/Reject** - Manage candidates with action buttons
5. **Dashboard** - View statistics and top matches

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database management
- **SQLite** - Lightweight database
- **pdfminer.six** - PDF text extraction
- **python-docx** - DOCX text extraction
- **sentence-transformers** - AI semantic matching (optional)
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool & dev server
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients & animations

## 📁 Project Structure

```
hireiq_prototype/
├── backend/
│   ├── app.py              # Flask application
│   ├── models.py           # Database models
│   ├── parser.py           # Resume parsing logic
│   ├── matcher.py          # Matching algorithm
│   ├── email_service.py    # Email notifications
│   ├── requirements.txt    # Python dependencies
│   └── instance/           # SQLite database (auto-created)
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main application
│   │   ├── main.jsx        # Entry point
│   │   ├── styles.css      # Global styles
│   │   └── components/     # React components
│   ├── index.html
│   └── package.json
├── .gitignore
└── README.md
```

## 🔧 Configuration

### Email Setup (Optional)

Set environment variables for email notifications:

```bash
# PowerShell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="your-email@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
$env:FROM_EMAIL="your-email@gmail.com"

# Bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export FROM_EMAIL="your-email@gmail.com"
```

**Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload resume file |
| POST | `/job` | Create job posting |
| GET | `/match/<job_id>` | Get candidate matches |
| POST | `/application/shortlist` | Shortlist candidate |
| POST | `/application/reject` | Reject candidate |
| GET | `/dashboard/top-matches/<job_id>` | Get top matches |
| GET | `/dashboard/stats/<job_id>` | Get job statistics |

## 🎨 Features Overview

### Matching Algorithm
- **Semantic Matching** (if sentence-transformers installed): Uses AI embeddings for intelligent matching
- **Keyword Matching** (fallback): Simple keyword overlap algorithm
- **Score Calculation**: 0-100% match score for each candidate

### Status Management
- **Pending**: Initial state for all candidates
- **Shortlisted**: Candidates selected for interview
- **Rejected**: Candidates not suitable for position

### Dashboard Analytics
- Total applications count
- Shortlisted/Pending/Rejected breakdown
- Top 10 ranked candidates
- Visual statistics cards

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database issues
```bash
# Delete database to reset
rm backend/instance/database.db
# Will be recreated on next run
```

## 📝 Data Storage

All data is stored locally in SQLite database at:
```
backend/instance/database.db
```

Includes:
- Resume text (extracted from files)
- Job postings
- Application status
- Match scores

**Note:** Original PDF/DOCX files are NOT saved, only extracted text.

## 🔒 Security Notes

- Database is not encrypted (development only)
- Use environment variables for credentials
- Enable HTTPS for production
- Implement authentication for production use

## 🚀 Future Enhancements

- [ ] User authentication & multi-tenancy
- [ ] Advanced search and filtering
- [ ] Interview scheduling
- [ ] Bulk actions
- [ ] Export functionality (CSV/PDF)
- [ ] Dark mode
- [ ] Mobile app

## 📄 License

MIT License - feel free to use for personal or commercial projects

## 👥 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built with Flask and React
- Uses sentence-transformers for AI matching
- Inspired by modern ATS systems

---

**Made with ❤️ for better recruitment**