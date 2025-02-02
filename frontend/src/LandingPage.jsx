import React from "react";
import "./index.css";
import cracked_ice from "./cracked_ice.png";

export default function LandingPage() {
    return (
        <div className="w-screen bg-[#E3F2FD] h-fill">
            <div className="flex flex-col items-center justify-center h-screen">
                <h1 className="text-6xl font-bold font-sans">IceBreakers</h1>
                <h2 className="text-2xl font-light mt-2">Break the Ice, Land the Job</h2>
                <img src={cracked_ice} alt="cracked ice" className="w-1/5 mt-8" />
            </div>
        </div>
    );
}
