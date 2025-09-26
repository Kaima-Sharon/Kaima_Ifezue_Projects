import React, { useState } from "react";
import { Link } from "react-router-dom";

function BookSearch(){
    const [query, setQuery] = useState("");
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchBooks = async () => {
    
    //exit early if query empty (don’t run the rest)
    if (!query.trim()) return;

    setLoading(true);

    try {
        // Send a GET request to the Google Books API using the user's query
        // encodeURIComponent ensures spaces and special characters in the query don't break the URL
        const res = await fetch(
        `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(query)}`
        );

        // Convert the response into a usable JSON format
        const data = await res.json();

        // If there are results, update the books state with the list of books
        // If no results, set books to an empty array
        setBooks(data.items || []);
    } catch (error) {
        console.error("Error fetching books:", error);
    } finally {
        // Whether the request succeeded or failed, stop the loading state
        setLoading(false);
    }
    };


    return (
      <div className="p-6 max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold mb-4 text-purple-700">📚 Search Books</h2>
        <div className="flex mb-4">
            <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter book title or author"
            className="flex-grow p-2 border rounded-l"
            />
            <button
            onClick={fetchBooks}
            className="bg-purple-600 text-white px-4 py-2 rounded-r hover:bg-purple-700"
            >
            Find your next book
            </button>
        </div>

        {loading ? (
            <p>Loading...</p>
        ) : (
            <div className="space-y-4">
            {books.map((book) => (
                <div key={book.id} className="border rounded p-4 shadow bg-white">
                    {/* Book Cover Image */}
                    {book.volumeInfo.imageLinks?.thumbnail && (
                    <img
                        src={book.volumeInfo.imageLinks.thumbnail}
                        alt={`Cover of ${book.volumeInfo.title}`}
                        className="w-32 h-auto mb-2"
                    />
                    )}

                    {/* Book Title */}
                    <Link to={`/book/${book.id}`} className="text-purple-600 hover:underline">
                        <h3 className="text-xl font-semibold">
                            {book.volumeInfo.title}
                        </h3>
                    </Link>

                    {/* Book Authors */}
                    <p className="text-gray-700">
                        {book.volumeInfo.authors?.join(", ") || "Unknown author"}
                    </p>
                </div>
            ))}
            </div>
        )}
      </div>
    );
}

export default BookSearch;