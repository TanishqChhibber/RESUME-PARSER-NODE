# Resume Parser API (Node.js)

This project provides a **Node.js** backend for parsing resumes using **OpenRouter AI GPT-4**. It extracts structured data such as name, email, phone, skills, experience, and more from uploaded resumes.

---

## 🚀 **Getting Started**

### Prerequisites
- **Node.js** (v14 or higher)
- **npm** (v6 or higher)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/resume-parser-node.git
   cd resume-parser-node
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up your API key:
   - Open `config.yaml` and replace `REPLACE_WITH_ENV_VARIABLE` with your OpenRouter API key.
   - Alternatively, use environment variables to securely store your API key.

4. Start the server:
   ```bash
   npm start
   ```

---

## 🛠 **API Usage**

### Endpoint: **POST /api/resume/parse**
- **Description**: Upload a resume file to extract structured data.
- **Request Body**:
  - Key: `resume`
  - Value: File (PDF, DOCX, or image formats supported)
- **Response**:
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "123-456-7890",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "skills": ["JavaScript", "Node.js", "React"],
    "experience": [
      {
        "company": "Tech Corp",
        "role": "Software Engineer",
        "duration": "Jan 2020 - Present",
        "details": ["Developed scalable web applications."]
      }
    ],
    "projects": [
      {
        "title": "Resume Parser",
        "duration": "2023",
        "details": ["Built a resume parsing tool using GPT-4."]
      }
    ],
    "education": ["B.Sc. in Computer Science"]
  }
  ```

---

## 📂 **Project Structure**
```
resume-parser-node/
│── server.js          # Entry point for the server
│── controllers/       # Business logic for parsing resumes
│   ├── resumeParser.js
│── routes/            # API route definitions
│   ├── resumeRoutes.js
│── config/            # Configuration files
│   ├── config.js
│── middleware/        # Error handling middleware
│   ├── errorHandler.js
│── uploads/           # Directory for uploaded resumes
│── .env               # Environment variables (not tracked in Git)
│── package.json       # Project metadata and dependencies
│── README.md          # Project documentation
```

---

## ⚠️ **Important Notes**
- Ensure your API key is securely stored and not hardcoded in the repository.
- Add `config.yaml` and `.env` to `.gitignore` to prevent accidental commits.

---

## 🤝 **Contributing**
Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.
