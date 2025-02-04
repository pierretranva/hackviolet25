import { Trash2, Star, MessageCircle, Share2 } from "lucide-react"
import './bear.css'
import { useState } from 'react'
import { FaCloudDownloadAlt } from "react-icons/fa";
import axios from "axios";



export default function CardItem({ title, cardId, date, setCards, chips, openModal }) {
     const [loading, setLoading] = useState(false)

     const downloadMarkdown = () => {
        setLoading(true)
        console.log(cardId)
        cardId = "hi"
        axios.post("http://localhost:8000/edit-resume", { job_mongo_id: cardId }).then((res) => {
            setLoading(false)
            console.log(res)
        }).catch((err) => {
            setLoading(false)
            console.log(err)
        })

     }
return (
    <div className="bg-white rounded-lg shadow-sm p-6 relative flex flex-col">
        <button
            onClick={() => setCards((prev) => prev.filter((card) => card.id !== cardId))}
            className="absolute bottom-2 right-2 text-[#90CAF9] hover:text-red-400 transition-colors"
            aria-label="Delete card"
        >
            <Trash2 size={10} />
        </button>
        <div className="flex justify-between w-full">
            <div className="flex flex-col">
                <h3 onClick={() => openModal(cardId)} className="text-l font-semibold mb-2 text-[#1E88E5] cursor-pointer hover:text-[#1976D2]">{title}</h3>
                <p className="text-[#90CAF9] mb-4 flex-grow">{date}</p>
            </div>
            <div>
                {loading ? <div className="loader"></div>: <button onClick={() => downloadMarkdown()} ><FaCloudDownloadAlt /></button>}
            </div>
        </div>
        <div className="flex flex-wrap gap-2 mt-4">
            {chips.map((chip) => (
                <span key={chip.id} className={`px-2 py-1 rounded-full text-xs font-semibold ${chip.color}`}>
                    {chip.label}
                </span>
            ))}
        </div>
    </div>
)
}
