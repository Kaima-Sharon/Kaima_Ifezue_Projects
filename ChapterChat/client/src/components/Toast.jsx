import React from "react";

function Toast({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded shadow-lg z-50 animate-bounce">
      <div className="flex justify-between items-center gap-4">
        <span>{message}</span>
        <button onClick={onClose} className="font-bold">X</button>
      </div>
    </div>
  );
}

export default Toast;
