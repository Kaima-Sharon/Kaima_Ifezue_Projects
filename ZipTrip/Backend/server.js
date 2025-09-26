const express = require('express');
const cors = require('cors');
require('dotenv').config();

const geminiRoute = require('./routes/geminiservice');

const app = express();

// ✅ Allow frontend (adjust origin if deployed)
app.use(cors({
    origin: ['http://localhost:5173', 'https://zip-trip-main.vercel.app'],
    credentials: true,
  }));

app.use(express.json());
app.use('/api/gemini', geminiRoute);

const PORT = process.env.PORT || 8989;
app.listen(PORT, () => console.log(`✅ Server running at http://localhost:${PORT}`));

const geminiActivities = require('./routes/geminiactivities');
app.use('/api/gemini-activities', geminiActivities);
