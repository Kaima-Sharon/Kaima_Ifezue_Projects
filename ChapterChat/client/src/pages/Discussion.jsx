import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./Dashboard";

function Discussion () {
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!newComment.trim()) return;

        const comment = {
            id: Date.now(),
            text: newComment,
        };

        setComments([comment, ...comments]);
        setNewComment("");
    };

    return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-4 text-purple-700">📖 Discussion</h2>

      <form onSubmit={handleSubmit} className="mb-6">
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Share your thoughts on the book..."
          className="w-full p-3 border rounded mb-2"
          rows={4}
        />
        <button
          type="submit"
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Post Comment
        </button>
      </form>

      <ul className="space-y-4">
        {comments.map((comment) => (
          <li key={comment.id} className="bg-gray-100 p-3 rounded shadow">
            {comment.text}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Discussion;