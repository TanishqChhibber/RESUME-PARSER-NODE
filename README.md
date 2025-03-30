# Resume Parser API (Node.js)

This is a **Node.js** backend for parsing resumes using **OpenAI GPT-4**.

## 🚀 **Setup Instructions**

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/resume-parser-node.git
   cd resume-parser-node
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the server:
   ```sh
   npm start
   ```

## 🛠 **API Endpoint**
- **POST /api/resume/parse**  
  - **Body:**  
    ```json
    {
      "resumeData": "John Doe, Software Engineer, john.doe@example.com, LinkedIn: linkedin.com/in/johndoe, GitHub: github.com/johndoe"
    }
    ```
  - **Response:**  
    ```json
    {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "linkedin": "linkedin.com/in/johndoe",
      "github": "github.com/johndoe"
    }
    ```

## 📌 **Project Structure**
```
resume-parser-node/
│── server.js
│── controllers/
│   ├── resumeParser.js
│── routes/
│   ├── resumeRoutes.js
│── config/
│   ├── config.js
│── middleware/
│   ├── errorHandler.js
│── .env
│── package.json
│── README.md
```
