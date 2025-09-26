import { GoogleGenAI } from "@google/genai";

// Replace with your actual API key or load from .env using dotenv (if you'd like, I can show that too)
const ai = new GoogleGenAI({ apiKey: "AIzaSyAD-aEwXjEU1dAqtvJrE5kI5fHTpCRr_tA" });

async function main() {
  const model = ai.getGenerativeModel({ model: "gemini-2.0-flash" });

  const result = await model.generateContent("Explain how AI works in a few words");

  const response = await result.response;
  const text = response.text();

  console.log(text);
}

main().catch(console.error);
