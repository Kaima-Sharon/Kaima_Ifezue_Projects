import React, { useState } from "react";

function ToDoList (){
    const [items, setItems] = useState([]);
    const [newItem, setNewItem] = useState("");

    const addItem = () => {
        if (newItem.trim() === "") return;
        setItems([...items, {text: newItem, done: false}]);
        setNewItem("");
    }

    const toggleItem = (index) => {
        const updateItems = [...items];
        updateItems[index].done = !updateItems[index].done;
        setItems(updatedItems);
    };

    return(
        <div className="flex flex-col bg-yellow-900 min-h-screen justify-center">
            <h1 className="text-3xl fontbold">To-Do List</h1>

            <input
                placeholder="Add Item"
                value={newItem}
                onChange={(e) => setNewItem(e.target.value)}
            />

            <button onClick={addItem} className="w-full bg-yellow-300 text-white rounded">
                Add item
            </button>

            <ul>
                {items.map((item, index) => (
                    <li key={index} className="flex items-center gap-2 text-white">
                        <input
                            type="checkbox"
                            checked={item.done}
                            onChange={() => toggleItem(index)}
                        />
                        <span className={item.done ? "line-through": ""}>{item.text}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ToDoList;