import React, { useState } from "react";
import { FiPlus, FiTrash } from "react-icons/fi";
import { motion } from "framer-motion";
import { FaFire } from "react-icons/fa";
import CardItem from "./CardItem";
import Modal from "./modal";
import AddModal from "./AddModal";
import axios from "axios";


export const Kanban = () => {
  return (
    <div className="h-full w-screen bg-white text-[#1E88E5]">
      <Board />
    </div>
  );
};

const Board = () => {
  const [cards, setCards] = useState(DEFAULT_CARDS);
  const [modal, setModal] = useState(false)
  const [modal_id, setModal_id] = useState(null)

  const [addModal, setAddModal] = useState(false)

    const openModal = (id) => {
        setModal(true)
        setModal_id(id)
    }
    const closeModal = () => {
        setModal(false)
        setModal_id(null)
    }
    const addJobAPI = (jobData) =>{
        let body= {company_name: jobData.companyName, date: jobData.date, url: jobData.jobUrl, chips: jobData.chips}
        console.log(body)
        axios.post('http://localhost:8000/add-job',body, {
            headers: {
                'Content-Type': 'application/json'
            }
        } )
        .then((response) => {
            console.log(response.data)
        }).catch((error) => {
            console.log(error)
        })
    }
    const addNewJob = (jobData) => {
        // console.log(jobData)
        addJobAPI(jobData)
        setCards((prev) => [
            {
                title: jobData.companyName,
        object_id: Math.random().toString(),
        column: "todo",
        url: jobData.jobUrl,
        date: jobData.date,
        chips: jobData.chips.map((chip) => {return {id: Math.random().toString(), label: chip, color: CHIP_COLORS[Math.floor(Math.random() * CHIP_COLORS.length)]}}),
            },
            ...prev,
        ]);
    }

return (
    <div className="grid grid-cols-4 h-full w-full gap-3 overflow-scroll p-12">
        <Column
            title="TODO"
            column="todo"
            headingColor="text-[#1E88E5]"
            cards={cards}
            setCards={setCards}
            openModal={openModal}
        />
        <Column
            title="Applied"
            column="applied"
            headingColor="text-[#1E88E5]"
            cards={cards}
            setCards={setCards}
            openModal={openModal}
        />
        <Column
            title="Interview"
            column="interview"
            headingColor="text-[#1E88E5]"
            cards={cards}
            setCards={setCards}
            openModal={openModal}
        />
        <Column
            title="Offer"
            column="offer"
            headingColor="text-[#1E88E5]"
            cards={cards}
            setCards={setCards}
            openModal={openModal}
        />
        <Modal isOpen={modal} modal_id={modal_id} setClose={closeModal}></Modal>
        <AddModal isOpen={addModal} setClose={setAddModal} addNewJob={addNewJob} />
        <button onClick={setAddModal}
            className="fixed bottom-20 right-20 p-0 w-20 h-20 rounded-full active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none !bg-[#1E88E5] hover:!bg-[#1565C0]"
        >
            <svg viewBox="0 0 20 20" enableBackground="new 0 0 20 20" className="w-6 h-6 inline-block">
                <path fill="#FFFFFF" d="M16,10c0,0.553-0.048,1-0.601,1H11v4.399C11,15.951,10.553,16,10,16c-0.553,0-1-0.049-1-0.601V11H4.601
                                                                C4.049,11,4,10.553,4,10c0-0.553,0.049-1,0.601-1H9V4.601C9,4.048,9.447,4,10,4c0.553,0,1,0.048,1,0.601V9h4.399
                                                                C15.952,9,16,9.447,16,10z" />
            </svg>
        </button>
    </div>
);
};

const Column = ({ title, headingColor, cards, column, setCards, openModal }) => {
  const [active, setActive] = useState(false);

  const handleDragStart = (e, card) => {
    e.dataTransfer.setData("cardId", card.id);
  };

  const handleDragEnd = (e) => {
    const cardId = e.dataTransfer.getData("cardId");

    setActive(false);
    clearHighlights();

    const indicators = getIndicators();
    const { element } = getNearestIndicator(e, indicators);

    const before = element.dataset.before || "-1";

    if (before !== cardId) {
      let copy = [...cards];

      let cardToTransfer = copy.find((c) => c.id === cardId);
      if (!cardToTransfer) return;
      cardToTransfer = { ...cardToTransfer, column };

      copy = copy.filter((c) => c.id !== cardId);

      const moveToBack = before === "-1";

      if (moveToBack) {
        copy.push(cardToTransfer);
      } else {
        const insertAtIndex = copy.findIndex((el) => el.id === before);
        if (insertAtIndex === undefined) return;

        copy.splice(insertAtIndex, 0, cardToTransfer);
      }

      setCards(copy);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    highlightIndicator(e);

    setActive(true);
  };

  const clearHighlights = (els) => {
    const indicators = els || getIndicators();

    indicators.forEach((i) => {
      i.style.opacity = "0";
    });
  };

  const highlightIndicator = (e) => {
    const indicators = getIndicators();

    clearHighlights(indicators);

    const el = getNearestIndicator(e, indicators);

    el.element.style.opacity = "1";
  };

  const getNearestIndicator = (e, indicators) => {
    const DISTANCE_OFFSET = 50;

    const el = indicators.reduce(
      (closest, child) => {
        const box = child.getBoundingClientRect();

        const offset = e.clientY - (box.top + DISTANCE_OFFSET);

        if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child };
        } else {
          return closest;
        }
      },
      {
        offset: Number.NEGATIVE_INFINITY,
        element: indicators[indicators.length - 1],
      }
    );

    return el;
  };

  const getIndicators = () => {
    return Array.from(document.querySelectorAll(`[data-column="${column}"]`));
  };

  const handleDragLeave = () => {
    clearHighlights();
    setActive(false);
  };

  const filteredCards = cards.filter((c) => c.column === column);

  return (
    <div className="shrink-0">
      <div className="mb-3 flex items-center justify-between">
        <h3 className={`font-medium ${headingColor}`}>{title}</h3>
        <span className="rounded text-sm text-[#90CAF9]">
          {filteredCards.length}
        </span>
      </div>
      <div
        onDrop={handleDragEnd}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`h-full w-full transition-colors ${
          active ? "bg-[#E3F2FD]/50" : "bg-[#E3F2FD]/0"
        }`}
      >
        {filteredCards.map((c) => {
          return <Card setCards={setCards}key={c.id} {...c} handleDragStart={handleDragStart} openModal={openModal}/>;
        })}
        <DropIndicator beforeId={null} column={column} />
        {/* <AddCard column={column} setCards={setCards} /> */}
      </div>
    </div>
  );
};

const Card = ({ setCards, date,title, id, column,chips, handleDragStart, openModal }) => {
  return (
    <>
      <DropIndicator beforeId={id} column={column} />
      <motion.div
        layout
        layoutId={id}
        draggable="true"
        onDragStart={(e) => handleDragStart(e, { title, id, column })}
        className="cursor-grab rounded border border-[#90CAF9] bg-white shadow-sm active:cursor-grabbing"
      >
       <CardItem cardId={id} title={title} date={date} chips={chips} setCards={setCards} openModal={openModal}></CardItem>
      </motion.div>
    </>
  );
};

const DropIndicator = ({ beforeId, column }) => {
  return (
    <div
      data-before={beforeId || "-1"}
      data-column={column}
      className="my-0.5 h-0.5 w-full bg-[#1E88E5] opacity-0"
    />
  );
};

const BurnBarrel = ({ setCards }) => {
  const [active, setActive] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setActive(true);
  };

  const handleDragLeave = () => {
    setActive(false);
  };

  const handleDragEnd = (e) => {
    const cardId = e.dataTransfer.getData("cardId");

    setCards((pv) => pv.filter((c) => c.id !== cardId));

    setActive(false);
  };

  return (
    <div
      onDrop={handleDragEnd}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      className={`mt-10 grid h-56 w-56 shrink-0 place-content-center rounded border text-3xl ${
        active
          ? "border-red-400 bg-red-50 text-red-500"
          : "border-[#90CAF9] bg-[#E3F2FD] text-[#1E88E5]"
      }`}
    >
      {active ? <FaFire className="animate-bounce" /> : <FiTrash />}
    </div>
  );
};


const DEFAULT_CARDS = [
    // BACKLOG
    {
        title: "Apple",
        object_id: "1",
        column: "todo",
        date: "2023-10-01",
        url: "https://www.apple.com",
        chips: [
            { id: 1, label: "High Priority", color: "bg-red-100 text-red-800" },
            { id: 2, label: "Backend", color: "bg-blue-100 text-blue-800" },
            { id: 3, label: "Sprint 2", color: "bg-green-100 text-green-800" },
        ],
    },
    {
        title: "Microsoft",
        object_id: "2",
        column: "interview",
        date: "2023-10-02",
        url: "https://www.microsoft.com",
        chips: [
            { id: 4, label: "Low Priority", color: "bg-yellow-100 text-yellow-800" },
            { id: 5, label: "Frontend", color: "bg-purple-100 text-purple-800" },
        ],
    },
    {
        title: "IBM",
        object_id: "3",
        column: "offer",
        date: "2023-10-03",
        url: "https://www.ibm.com",
        chips: [
            { id: 6, label: "Medium Priority", color: "bg-orange-100 text-orange-800" },
            { id: 7, label: "DevOps", color: "bg-teal-100 text-teal-800" },
        ],
    },
    {
        title: "Oracle",
        id: "4",
        column: "interview",
        date: "2023-10-04",
        url: "https://www.oracle.com",
        chips: [
            { id: 8, label: "Documentation", color: "bg-gray-100 text-gray-800" },
        ],
    },
    // TODO
    {
        title: "Salesforce",
        id: "5",
        column: "todo",
        date: "2023-10-05",
        url: "https://www.salesforce.com",
        chips: [
            { id: 9, label: "Research", color: "bg-pink-100 text-pink-800" },
            { id: 10, label: "Database", color: "bg-indigo-100 text-indigo-800" },
        ],
    },
    {
        title: "SAP",
        object_id: "6",
        column: "todo",
        date: "2023-10-06",
        url: "https://www.sap.com",
        chips: [
            { id: 11, label: "Postmortem", color: "bg-red-100 text-red-800" },
            { id: 12, label: "Incident", color: "bg-black-100 text-black-800" },
        ],
    },
    {
        title: "Adobe",
        object_id: "7",
        column: "todo",
        date: "2023-10-07",
        url: "https://www.adobe.com",
        chips: [
            { id: 13, label: "Meeting", color: "bg-blue-100 text-blue-800" },
            { id: 14, label: "Roadmap", color: "bg-green-100 text-green-800" },
        ],
    },
    // DOING
    {
        title: "Intel",
        object_id: "8",
        column: "applied",
        date: "2023-10-08",
        url: "https://www.intel.com",
        chips: [
            { id: 15, label: "Refactor", color: "bg-yellow-100 text-yellow-800" },
            { id: 16, label: "State Management", color: "bg-purple-100 text-purple-800" },
        ],
    },
    {
        title: "Cisco",
        output_id: "9",
        column: "doing",
        date: "2023-10-09",
        url: "https://www.cisco.com",
        chips: [
            { id: 17, label: "Logging", color: "bg-orange-100 text-orange-800" },
            { id: 18, label: "CRON", color: "bg-teal-100 text-teal-800" },
        ],
    },
    // DONE
    {
        title: "Nvidia",
        output_id: "10",
        column: "done",
        date: "2023-10-10",
        url: "https://www.nvidia.com",
        chips: [
            { id: 19, label: "Dashboard", color: "bg-gray-100 text-gray-800" },
            { id: 20, label: "Lambda", color: "bg-pink-100 text-pink-800" },
        ],
    },
];
const CHIP_COLORS = [
    "bg-red-100 text-red-800",
    "bg-yellow-100 text-yellow-800",
    "bg-green-100 text-green-800",
    "bg-blue-100 text-blue-800",
    "bg-indigo-100 text-indigo-800",
    "bg-purple-100 text-purple-800",
    "bg-pink-100 text-pink-800",
    "bg-black-100 text-black-800",
    "bg-gray-100 text-gray-800",
    "bg-orange-100 text-orange-800",
    "bg-teal-100 text-teal-800",
];
