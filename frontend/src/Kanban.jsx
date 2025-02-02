import React, { useState } from "react";
import { FiPlus, FiTrash } from "react-icons/fi";
import { motion } from "framer-motion";
import { FaFire } from "react-icons/fa";
import CardItem from "./CardItem";
import Modal from "./modal";

export const Kanban = () => {
  return (
    <div className="h-full w-screen bg-neutral-900 text-neutral-50">
      <Board />
    </div>
  );
};

const Board = () => {
  const [cards, setCards] = useState(DEFAULT_CARDS);
  const [modal, setModal] = useState(false)
  const [modal_id, setModal_id] = useState(null)

    const openModal = (id) => {
        setModal(true)
        setModal_id(id)
    }
    const closeModal = () => {
        setModal(false)
        setModal_id(null)
    }

  return (
    <div className="grid grid-cols-4 h-full w-full gap-3 overflow-scroll p-12">
      <Column
        title="Backlog"
        column="backlog"
        headingColor="text-neutral-500"
        cards={cards}
        setCards={setCards}
        openModal={openModal}
      />
      <Column
        title="TODO"
        column="todo"
        headingColor="text-yellow-200"
        cards={cards}
        setCards={setCards}
        openModal={openModal}
      />
      <Column
        title="In progress"
        column="doing"
        headingColor="text-blue-200"
        cards={cards}
        setCards={setCards}
        openModal={openModal}
      />
      <Column
        title="Complete"
        column="done"
        headingColor="text-emerald-200"
        cards={cards}
        setCards={setCards}
        openModal={openModal}
      />
      <Modal isOpen={modal} modal_id={modal_id} setClose={closeModal}></Modal>
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
        <span className="rounded text-sm text-neutral-400">
          {filteredCards.length}
        </span>
      </div>
      <div
        onDrop={handleDragEnd}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`h-full w-full transition-colors ${
          active ? "bg-neutral-800/50" : "bg-neutral-800/0"
        }`}
      >
        {filteredCards.map((c) => {
          return <Card setCards={setCards}key={c.id} {...c} handleDragStart={handleDragStart} openModal={openModal}/>;
        })}
        <DropIndicator beforeId={null} column={column} />
        <AddCard column={column} setCards={setCards} />
      </div>
    </div>
  );
};

const Card = ({ setCards, title, id, column,chips, handleDragStart, openModal }) => {
  return (
    <>
      <DropIndicator beforeId={id} column={column} />
      <motion.div
        layout
        layoutId={id}
        draggable="true"
        onDragStart={(e) => handleDragStart(e, { title, id, column })}
        className="cursor-grab rounded border border-neutral-700 bg-neutral-800 active:cursor-grabbing"
      >
       <CardItem cardId={id} title={title}  chips={chips} setCards={setCards} openModal={openModal}></CardItem>
      </motion.div>
    </>
  );
};

const DropIndicator = ({ beforeId, column }) => {
  return (
    <div
      data-before={beforeId || "-1"}
      data-column={column}
      className="my-0.5 h-0.5 w-full bg-violet-400 opacity-0"
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
          ? "border-red-800 bg-red-800/20 text-red-500"
          : "border-neutral-500 bg-neutral-500/20 text-neutral-500"
      }`}
    >
      {active ? <FaFire className="animate-bounce" /> : <FiTrash />}
    </div>
  );
};

const AddCard = ({ column, setCards }) => {
  const [text, setText] = useState("");
  const [adding, setAdding] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!text.trim().length) return;

    const newCard = {
      column,
      title: text.trim(),
      id: Math.random().toString(),
    };

    setCards((pv) => [...pv, newCard]);

    setAdding(false);
  };

  return (
    <>
      {adding ? (
        <motion.form layout onSubmit={handleSubmit}>
          <textarea
            onChange={(e) => setText(e.target.value)}
            autoFocus
            placeholder="Add new task..."
            className="w-full rounded border border-violet-400 bg-violet-400/20 p-3 text-sm text-neutral-50 placeholder-violet-300 focus:outline-0"
          />
          <div className="mt-1.5 flex items-center justify-end gap-1.5">
            <button
              onClick={() => setAdding(false)}
              className="px-3 py-1.5 text-xs text-neutral-400 transition-colors hover:text-neutral-50"
            >
              Close
            </button>
            <button
              type="submit"
              className="flex items-center gap-1.5 rounded bg-neutral-50 px-3 py-1.5 text-xs text-neutral-950 transition-colors hover:bg-neutral-300"
            >
              <span>Add</span>
              <FiPlus />
            </button>
          </div>
        </motion.form>
      ) : (
        <motion.button
          layout
          onClick={() => setAdding(true)}
          className="flex w-full items-center gap-1.5 px-3 py-1.5 text-xs text-neutral-400 transition-colors hover:text-neutral-50"
        >
          <span>Add card</span>
          <FiPlus />
        </motion.button>
      )}
    </>
  );
};
const DEFAULT_CARDS = [
    // BACKLOG
    {
        title: "Apple",
        id: "1",
        column: "backlog",
        content: "2023-10-01",
        chips: [
            { id: 1, label: "High Priority", color: "bg-red-100 text-red-800" },
            { id: 2, label: "Backend", color: "bg-blue-100 text-blue-800" },
            { id: 3, label: "Sprint 2", color: "bg-green-100 text-green-800" },
        ],
    },
    {
        title: "Microsoft",
        id: "2",
        column: "backlog",
        content: "2023-10-02",
        chips: [
            { id: 4, label: "Low Priority", color: "bg-yellow-100 text-yellow-800" },
            { id: 5, label: "Frontend", color: "bg-purple-100 text-purple-800" },
        ],
    },
    {
        title: "IBM",
        id: "3",
        column: "backlog",
        content: "2023-10-03",
        chips: [
            { id: 6, label: "Medium Priority", color: "bg-orange-100 text-orange-800" },
            { id: 7, label: "DevOps", color: "bg-teal-100 text-teal-800" },
        ],
    },
    {
        title: "Oracle",
        id: "4",
        column: "backlog",
        content: "2023-10-04",
        chips: [
            { id: 8, label: "Documentation", color: "bg-gray-100 text-gray-800" },
        ],
    },
    // TODO
    {
        title: "Salesforce",
        id: "5",
        column: "todo",
        content: "2023-10-05",
        chips: [
            { id: 9, label: "Research", color: "bg-pink-100 text-pink-800" },
            { id: 10, label: "Database", color: "bg-indigo-100 text-indigo-800" },
        ],
    },
    {
        title: "SAP",
        id: "6",
        column: "todo",
        content: "2023-10-06",
        chips: [
            { id: 11, label: "Postmortem", color: "bg-red-100 text-red-800" },
            { id: 12, label: "Incident", color: "bg-black-100 text-black-800" },
        ],
    },
    {
        title: "Adobe",
        id: "7",
        column: "todo",
        content: "2023-10-07",
        chips: [
            { id: 13, label: "Meeting", color: "bg-blue-100 text-blue-800" },
            { id: 14, label: "Roadmap", color: "bg-green-100 text-green-800" },
        ],
    },
    // DOING
    {
        title: "Intel",
        id: "8",
        column: "doing",
        content: "2023-10-08",
        chips: [
            { id: 15, label: "Refactor", color: "bg-yellow-100 text-yellow-800" },
            { id: 16, label: "State Management", color: "bg-purple-100 text-purple-800" },
        ],
    },
    {
        title: "Cisco",
        id: "9",
        column: "doing",
        content: "2023-10-09",
        chips: [
            { id: 17, label: "Logging", color: "bg-orange-100 text-orange-800" },
            { id: 18, label: "CRON", color: "bg-teal-100 text-teal-800" },
        ],
    },
    // DONE
    {
        title: "Nvidia",
        id: "10",
        column: "done",
        content: "2023-10-10",
        chips: [
            { id: 19, label: "Dashboard", color: "bg-gray-100 text-gray-800" },
            { id: 20, label: "Lambda", color: "bg-pink-100 text-pink-800" },
        ],
    },
];
