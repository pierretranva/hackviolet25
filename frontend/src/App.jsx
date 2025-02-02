import { useState } from 'react'

import './App.css'
import { Route, Routes } from "react-router-dom";
import { Kanban } from './Kanban';
import Navbar from './Navbar';
import "./index.css"
import LandingPage from './LandingPage';
import EditResumePage from './EditResumePage';

function App() {


  return (
    <div className="h-screen"> 
    <Navbar/>
    <Routes>
		<Route path="/" element={<LandingPage/>} />
        <Route path="/dashboard" element={<Kanban/>} />
        <Route path="/editResume" element={<EditResumePage/>}/>
        <Route path="/home" element={<LandingPage/>} />
        
    </Routes>


    </div>
  )
}

export default App
