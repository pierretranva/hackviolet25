import { useState } from 'react'

import './App.css'
import { Route, Routes } from "react-router-dom";
import { Kanban } from './Kanban';
import Navbar from './Navbar';
import "./index.css"
import LandingPage from './LandingPage';

function App() {


  return (
    <div className="h-screen"> 
    <Navbar/>
    <Routes>
		<Route path="/" element={<Kanban/>} />
        <Route path="/dashboard" element={<Kanban/>} />
        <Route path="/addJob" element={<Kanban/>}/>
        <Route path="/editResume" element={<Kanban/>}/>
        <Route path="/landing" element={<LandingPage/>} />
        
    </Routes>


    </div>
  )
}

export default App
