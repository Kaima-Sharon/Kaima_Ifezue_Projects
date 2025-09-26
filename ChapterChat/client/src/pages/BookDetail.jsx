import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function BookDetail() {
  const { id } = useParams();
  const [book, setBook] = useState(null);

  useEffect(() => {
    const fetchBook = async () => {
      const res = await fetch(`https://www.googleapis.com/books/v1/volumes/${id}`);
      const data = await res.json();
      setBook(data);
    };
    fetchBook();
  }, [id]);

  if (!book) return <p className="text-center mt-8">Loading...</p>;

  const { title, authors, description, imageLinks } = book.volumeInfo;

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-3xl font-bold mb-2 text-purple-700">{title}</h2>
      <p className="mb-2 text-gray-700">By {authors?.join(", ")}</p>
      {imageLinks?.thumbnail && (
        <img src={imageLinks.thumbnail} alt={title} className="mb-4" />
      )}
      <p className="mb-6 text-gray-800">{description || "No description available."}</p>

      <button className="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700">
        Add to Club List
      </button>
    </div>
  );
}

export default BookDetail;
