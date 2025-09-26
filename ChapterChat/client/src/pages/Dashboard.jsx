import React from "react";
import { auth } from "../firebase";

import { db } from "../firebase"; // adjust path if needed
import { collection, addDoc } from "firebase/firestore";


function Dashboard() {
    const testWrite = async () => {
    try {
      const docRef = await addDoc(collection(db, "testCollection"), {
        message: "Hello from Chapter Chat!",
        timestamp: new Date()
      });
      console.log("Document written with ID: ", docRef.id);
    } catch (e) {
      console.error("Error adding document: ", e);
    }
  };

    const user = auth.currentUser;

    return (
        <div className="min-h-screen bg-gradient-to-br from-pink-100 via-purple-100 to-pink-200 p-6">
            <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-6">
                <h1 className="text-3xl font-bold text-purple-700 mb-4">📚 Welcome back, {user?.email}!</h1>
                <p className="text-lg text-gray-700 mb-6">
                Here’s a quick look at your reading journey:
                </p>

                <div className="bg-purple-100 p-4 rounded-lg mb-4">
                <h2 className="text-xl font-semibold text-purple-600 mb-2">📖 Current Book</h2>
                <p><strong>Title:</strong> The Book Thief</p>
                <p><strong>Author:</strong> Markus Zusak</p>
                <p><strong>Progress:</strong> 45%</p>
                </div>

                <div className="bg-pink-100 p-4 rounded-lg">
                <h2 className="text-xl font-semibold text-pink-600 mb-2">📅 Next Meeting</h2>
                <p><strong>Date:</strong> May 25, 2025</p>
                <p><strong>Time:</strong> 7:00 PM</p>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;