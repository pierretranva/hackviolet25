import { useState, useRef } from 'react';

export default function AddModal({ isOpen, setClose, addNewJob }) {
    if (!isOpen) return null;
    const [jobData, setJobData] = useState({});
    const companyNameRef = useRef(null);
    const dateRef = useRef(null);
    const jobUrlRef = useRef(null);
    const chipsRef = useRef(null);

    const handleAddJob = () => {
        const companyName = companyNameRef.current.value;
        const date = dateRef.current.value;
        const jobUrl = jobUrlRef.current.value;
        const chips = chipsRef.current.value;

        if (companyName && date && jobUrl && chips) {
            setJobData({
                companyName,
                date,
                jobUrl,
                chips: chips.split(',').map(chip => chip.trim()),
            });
            console.log({
                companyName,
                date,
                jobUrl,
                chips: chips.split(',').map(chip => chip.trim()),
            })
            addNewJob({
                companyName,
                date,
                jobUrl,
                chips: chips.split(',').map(chip => chip.trim()),
            });
            setClose(false);
        } else {
            alert('Please fill out all fields.');
        }
    };

    return (
        <div className="fixed inset-0 bg-[#1E88E5]/10 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl w-[60%] h-[58%] mx-auto shadow-xl relative">
                <div className="p-6 flex flex-col items-center">
                    <form className="w-full max-w-lg">
                        <div className="flex flex-wrap -mx-3 mb-6">
                            <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                                <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" htmlFor="grid-first-name">
                                    Company Name
                                </label>
                                <input
                                    className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
                                    id="grid-first-name"
                                    type="text"
                                    placeholder="Company Name"
                                    required
                                    ref={companyNameRef}
                                />
                            </div>
                            <div className="w-full md:w-1/2 px-3">
                                <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" htmlFor="grid-last-name">
                                    Date
                                </label>
                                <input
                                    className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                                    id="grid-last-name"
                                    type="date"
                                    placeholder="Doe"
                                    required
                                    ref={dateRef}
                                />
                            </div>
                        </div>
                        <div className="flex flex-wrap -mx-3 mb-6">
                            <div className="w-full px-3">
                                <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" htmlFor="grid-password">
                                    Job Posting Url
                                </label>
                                <input
                                    className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                                    id="grid-password"
                                    type="url"
                                    required
                                    ref={jobUrlRef}
                                />
                            </div>
                        </div>
                        <div className="flex flex-wrap -mx-3 mb-6">
                            <div className="w-full px-3">
                                <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" htmlFor="grid-chips">
                                    Chips
                                </label>
                                <input
                                    className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                                    id="grid-chips"
                                    type="text"
                                    required
                                    ref={chipsRef}
                                />
                                <p className="text-grey text-xs italic">Put the chips in this format "chip1, chip2"</p>
                            </div>
                        </div>
                    </form>
                </div>
                <div className="p-0 flex flex-col items-center">
                    <div className="flex gap-4 w-[90%]">
                        <button
                            onClick={() => setClose(false)}
                            className="flex-1 px-4 py-2.5 border border-[#90CAF9] text-[#1E88E5] rounded-lg hover:bg-[#E3F2FD] font-medium transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleAddJob}
                            className="flex-1 px-4 py-2.5 bg-[#1E88E5] text-white rounded-lg hover:bg-[#1976D2] font-medium transition-colors"
                        >
                            Add Job
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
