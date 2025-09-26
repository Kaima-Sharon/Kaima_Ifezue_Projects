import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Discussion from "./pages/Discussion";
import BookSearch from "./components/BookSearch";
import BookDetail from "./pages/BookDetail";
import "./index.css";

function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-pink-100 via-purple-100 to-pink-200 p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 max-w-xl w-full text-center">
        <h1 className="text-4xl font-extrabold text-purple-600 mb-4">📚 Welcome to Chapter Chat</h1>
        <p className="text-lg text-gray-700 mb-6">
          Your cozy online book club. Discuss, share, and track your reads with friends.
        </p>
        <Link to="/signup">
          <button className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-6 rounded-full transition">
            Get Started
          </button>
        </Link>
      </div>
    </main>
  );
}

function App() {
  return (
    <Router>
      <Navbar />
      <div className="pt-16"> {/* 👈 pushes content below the fixed navbar */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/discussion" element={<Discussion />} />
        <Route path="/search" element={<BookSearch />} />
        <Route path="/book/:id" element={<BookDetail />} />
      </Routes>
      </div>
    </Router>
  );
}

export default App;

