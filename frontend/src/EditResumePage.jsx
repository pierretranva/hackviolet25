import { useEffect, useState } from "react";
import axios from "axios";

const UploadPDF = () => {
	const [file, setFile] = useState(null);
	const [fileId, setFileId] = useState(null); // Store uploaded file ID
    const [desc, setDesc] = useState("");

    useEffect(() => {
        axios.get("http://localhost:8000/get-description").then((response) => {
            setDesc(response.data.description);
        });
    }, []);
	// Handle file selection
	const handleFileChange = (e) => {
		setFile(e.target.files[0]);
	};

    const saveDesc = async () => {
        // console.log(desc);
        try {
            const response = await axios.post("http://localhost:8000/upload-description", 
                {description: desc}
            , {
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.status === 200) {
                alert("Description saved successfully!");
            } else {
                alert("Error: " + response.data.error);
            }
        } catch (error) {
            console.error("Error saving description:", error);
            alert("Failed to save description.");
        }
    };
	// Handle file upload
    const handleUpload = async () => {
        if (!file) {
            alert("Please select a PDF file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://localhost:8000/upload-pdf", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            alert("File uploaded successfully!");
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("Failed to upload file.");
        }
    };
	// Handle file download
	const handleDownload = async () => {
		if (!fileId) {
			alert("No file available for download.");
			return;
		}

		window.open(`http://localhost:8000/download/${fileId}`, "_blank");
	};

    return (
        <div className="w-screen h-screen flex flex-row items-center justify-center top-[-200px] min-h-screen bg-gray-100">
            <div className="flex flex-row space-x-4 w-full max-w-4xl">
                <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
                    <div className="flex flex-col items-center justify-center">
                        <input
                            type="file"
                            accept="application/pdf"
                            onChange={handleFileChange}
                            className="mb-4 p-2 border border-gray-300 rounded"
                        />
                        <button
                            onClick={handleUpload}
                            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
                        >
                            Upload PDF
                        </button>
                        {fileId && (
                            <button
                                onClick={handleDownload}
                                className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200 mt-4"
                            >
                                Download PDF
                            </button>
                        )}
                    </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
                    <div className="flex flex-col items-center justify-center">
                        <textarea
                            className="mb-4 p-2 border border-gray-300 rounded h-48 w-full"
                            value={desc}
                            onChange={(e) => setDesc(e.target.value)}
                        />

                        <button
                            onClick={saveDesc}
                            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
                        >
                            Save Desc
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UploadPDF;
