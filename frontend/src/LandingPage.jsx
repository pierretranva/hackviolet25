import React from "react";
import "./index.css";
import cracked_ice from "./assets/cracked_ice.png";
import pengu from "./assets/pengu.png";
import Snowfall from "react-snowfall";



export default function LandingPage() {
	return (
		<div className="w-screen bg-[#E3F2FD] h-fill">
			<Snowfall
				color="#1E88E5"
                radius={[1,2]}
				// Applied to the canvas element
				// Controls the number of snowflakes that are created (default 150)
				snowflakeCount={20}

			/>
			<div className="flex flex-col items-center justify-center h-screen">
            <img src={pengu} alt="cracked ice" className="w-[12%]" />
				<h1 className="text-6xl font-bold font-sans">Pengu</h1>
				<h2 className="text-2xl font-light mt-2">Break the Ice, Land the Job</h2>

			</div>
		</div>
	);
}
