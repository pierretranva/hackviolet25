import { Trash2, Star, MessageCircle, Share2 } from "lucide-react"



export default function CardItem({ title, cardId, content, setCards, chips, openModal }) {
  return (
    <div className="bg-neutral-800 rounded-lg shadow-md p-6 relative flex flex-col">
      <button
        onClick={() => setCards((prev) => prev.filter((card) => card.id !== cardId))}
        className="absolute bottom-2 right-2 text-gray-400 hover:text-red-500 transition-colors"
        aria-label="Delete card"
      >
        <Trash2 size={10} />
      </button>
      <h3 onClick={() =>{  openModal(cardId)   }} className="text-l font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 mb-4 flex-grow">{content}</p>
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

