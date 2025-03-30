const axios = require('axios');

const parseResume = async (req, res) => {
    try {
        const { resumeData } = req.body;
        if (!resumeData) return res.status(400).json({ error: 'Resume data is required' });

        const extractionTemplate = {
            name: 'Full name',
            email: 'Email address',
            linkedin: 'LinkedIn profile URL',
            phone: 'Phone number',
            github: 'GitHub profile URL',
            behance: 'Behance profile URL',
            skills: ['list', 'of', 'skills'],
            experience: ['Position details'],
            education: ['Degree details']
        };

        const response = await axios.post(
            'https://openrouter.ai/api/v1/chat/completions',
            {
                model: 'openai/gpt-4',
                messages: [
                    { role: 'system', content: 'You are an ATS parser. Return ONLY valid JSON. Do not include explanations.' },
                    { role: 'user', content: `${JSON.stringify(extractionTemplate)}\n\nResume data:\n${resumeData}` }
                ],
                temperature: 0.1,
                max_tokens: 2000
            },
            {
                headers: {
                    'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
                    'HTTP-Referer': 'YOUR_SITE_URL',
                    'X-Title': 'ATS Parser'
                }
            }
        );

        return res.json(response.data);
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

module.exports = { parseResume };
