// const express = require('express');
// const router = express.Router();
// const { GoogleGenerativeAI } = require('@google/generative-ai');
// require('dotenv').config();

// const API_KEY = process.env.GEMINI_API_KEY;
// const genAI = new GoogleGenerativeAI(API_KEY);

// router.post('/', async (req, res) => {
//   const { destination, dateRange, purpose, weather } = req.body;

//   const prompt = `
//     Create a categorized travel packing checklist for a ${purpose} trip to ${destination} from ${dateRange}.
//     Weather: ${weather}.
//     Categories: Clothing, Essentials, Toiletries, Tech.
//     Return as plain text.
//   `;

//   try {
//     const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
//     const result = await model.generateContent(prompt);
//     const text = result.response.text();
//     res.json({ checklist: text });
//   } catch (err) {
//     console.error("Gemini Error:", err.response?.data || err.message);
//     res.status(500).json({ error: "Gemini API failed" });
//   }
// });

// module.exports = router;

const express = require('express');
const router = express.Router();
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const API_KEY = process.env.GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(API_KEY);

router.post('/', async (req, res) => {
  const { destination, dateRange, purpose, weather } = req.body;

  const prompt = `
    Create a categorized travel packing checklist for a ${purpose} trip to ${destination} from ${dateRange}.
    Weather: ${weather}.
    Categories: Clothing, Essentials, Toiletries, Tech.
    Return as plain text.
  `;

  try {
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
    const result = await model.generateContent(prompt);
    const text = result.response.text();

    res.json({ checklist: text });
  } catch (err) {
    console.error("Gemini API Error:", err.response?.data || err.message);
    res.status(500).json({ error: "Gemini API failed" });
  }
});

module.exports = router;

