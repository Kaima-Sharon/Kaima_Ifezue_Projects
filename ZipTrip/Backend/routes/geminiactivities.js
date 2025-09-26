const express = require('express');
const router = express.Router();
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const API_KEY = process.env.GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(API_KEY);

router.post('/', async (req, res) => {
  const { destination } = req.body;

  const prompt = `
List 5 unique travel activities in ${destination}. Format each like:

Activity Name: A one-sentence description (at least 15 words) that explains what the activity is and why it’s worth doing.

Only include activities that are relevant to the destination.
`;


  try {
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
    const result = await model.generateContent(prompt);
    const text = result.response.text();
    res.json({ suggestions: text });
  } catch (err) {
    console.error("Gemini Activity API Error:", err.response?.data || err.message);
    res.status(500).json({ error: "Failed to generate activity suggestions." });
  }
});

module.exports = router;
