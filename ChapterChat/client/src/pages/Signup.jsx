import React, { useState } from "react";
import { auth } from "../firebase";
import { createUserWithEmailAndPassword } from "firebase/auth";
import Toast from "../components/Toast";
import { Link, useNavigate } from "react-router-dom";

function Signup() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [toastMessage, setToastMessage] = useState("");
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            // createUserWithEmailAndPassword(auth, email, password) sends email and password to Firebase, if valid firebase creates the users and returns a 'user' object. Throws an error otherwise
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            console.log("User created:", userCredential.user);
            setToastMessage("Sign up successful! 🎉");
            navigate("/dashboard"); // adds redirect
        } catch (error) {
            console.error("Signup error:", error.message);
            setToastMessage(error.message);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4">
            <Toast message={toastMessage} onClose={() => setToastMessage("")} />
            <form onSubmit={handleSignup} className="w-full max-w-sm bg-white p-6 rounded shadow">
                <h2 className="text-2xl font-bold mb-4">Sign Up</h2>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="mb-3 w-full p-2 border rounded"
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="mb-3 w-full p-2 border rounded"
                    required
                />

                <button type="submit" className="w-full bg-purple-600 text-white p-2 rounded">
                    Sign Up
                </button>
                <p className="mt-4 text-sm">
                    Have an account? <Link to="/login" className="text-purple-600 underline">Login</Link>
                </p>
            </form>
        </div>
    );
}

export default Signup;
