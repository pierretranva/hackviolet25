import { useState } from 'react'

import './App.css'
import { Route, Routes } from "react-router-dom";
import { Kanban } from './Kanban';
import Navbar from './Navbar';
import "./index.css"

function App() {


  return (
    <div className="h-screen"> 
    <Navbar/>
    <Routes>
		<Route path="/" element={<Kanban/>} />
		{/* <Route path="/edit" element={<EditProfile/>} /> */}

    </Routes>


    </div>
  )
}

export default App
