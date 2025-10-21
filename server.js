require('dotenv').config();
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const { spawn } = require('child_process'); // Import to run Python scripts

const app = express();
const PORT = process.env.PORT || 5001;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from public directory
app.use(express.static('public'));

// Multer Storage Configuration
const storage = multer.diskStorage({
    destination: "uploads/",
    filename: (req, file, cb) => {
        cb(null, Date.now() + "-" + file.originalname);
    }
});

const upload = multer({ 
    storage: storage,
    limits: { fileSize: 5 * 1024 * 1024 }, // 5MB max file size
});

// ✅ Upload & Parse Resume
app.post("/api/resume/parse", upload.single("resume"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "Resume file is required!" });
    }

    const filePath = path.join(__dirname, "uploads", req.file.filename);

    // 🟢 Call Python Script to Extract Data
    const pythonProcess = spawn('/Users/tanishq/Documents/GitHub/RESUME-PARSER-NODE/.venv/bin/python', ['resume_parser.py', filePath]);

    let output = "";

    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on('data', (error) => {
        console.error("❌ Python Error:", error.toString());
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).json({ error: "Failed to process resume" });
        }
        res.json({
            message: "Resume parsed successfully!",
            filename: req.file.filename,
            filePath: filePath,
            extractedData: JSON.parse(output)
        });
    });
});

// Start Server
app.listen(PORT, () => {
    console.log(`🚀 Server running on: http://localhost:${PORT}`);
});
