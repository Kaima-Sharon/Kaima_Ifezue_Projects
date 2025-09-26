import React, { useState } from "react";
import { AiOutlineClose, AiOutlineMenu, AiOutlineSearch } from "react-icons/ai";
import logo from "../assets/logo.png";
import { Link } from "react-router-dom";

const Navbar = () => {
    //state to manage the navbar's visibility
    const [nav, setNav] = useState(false);

    // Toggle function to handle the navbar's display
    const handleNav = () => {
        setNav(!nav);
    }

    // Array containing navigation items
    const navItems = [
        { id: 1, text: "Home", path: "/"},
        { id: 2, text: "Dashboard", path: "/dashboard"},
        { id: 3, text: "Discussion", path: "/discussion"},
        { id: 4, text: "Account", path: "/account"},
    ];

    return (
        <div className="flex justify-between items-center h-16 bg-white px-4 shadow-md fixed top-0 w-full z-50">
            <Link to="/" className="flex items-center space-x-2">
                <img src={logo} alt="Chapter Chat Logo" className="h-8 w-8" />
                <span className="text-2xl font-bold text-purple-600">Chapter Chat</span>
            </Link>

            {/* Desktop nav */}
            <ul className="hidden md:flex space-x-6">
                {navItems.map((item) => (
                <li key={item.id}>
                    <Link to={item.path} className="hover:text-purple-600 font-medium">
                    {item.text}
                    </Link>
                </li>
                ))}
            </ul>

            {/* Right-side icons */}
            <div className="flex items-center space-x-4">
                <Link to="/search" className="text-purple-600 hover:text-purple-800">
                <AiOutlineSearch size={24} />
                </Link>
                {/* Menu icon only on mobile */}
                <div onClick={handleNav} className="md:hidden cursor-pointer">
                {nav ? <AiOutlineClose size={24} /> : <AiOutlineMenu size={24} />}
                </div>
            </div>

            {/* Mobile menu */}
            <ul
                className={`absolute top-16 left-0 w-full bg-white p-4 space-y-4 shadow-md md:hidden transition-transform duration-300 ${
                nav ? "translate-y-0" : "-translate-y-[200%]"
                }`}
            >
                {navItems.map((item) => (
                <li key={item.id}>
                    <Link
                    to={item.path}
                    onClick={handleNav}
                    className="block text-lg hover:text-purple-600"
                    >
                    {item.text}
                    </Link>
                </li>
                ))}
            </ul>
        </div>
    )
}

export default Navbar;