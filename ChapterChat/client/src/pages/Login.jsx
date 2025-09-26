import React, { useState } from "react";
import { auth } from "../firebase";
import { signInWithEmailAndPassword } from "firebase/auth";
import Toast from "../components/Toast";
import { Link, useNavigate } from "react-router-dom";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [toastMessage, setToastMessage] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            console.log("User logged in: ", userCredential.user);
            setToastMessage("Login successful!");
            navigate("/dashboard");
        } catch(error) {
            console.error("Login error:", error.message);
            setToastMessage(error.message);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4">
            <Toast message={toastMessage} onClose={() => setToastMessage("")} />
            <form onSubmit={handleLogin} className="w-full max-w-sm bg-white p-6 rounded shadow">
                <h2 className="text-2xl font-bold mb-4">Log In</h2>

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
                    Login 
                </button>

                <p className="mt-4 text-sm">
                    Don’t have an account? <Link to="/signup" className="text-purple-600 underline">Sign up</Link>
                </p>

            </form>
        </div>
    );
}

export default Login;