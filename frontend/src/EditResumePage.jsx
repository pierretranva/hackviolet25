import { useState } from "react";

const UploadPDF = () => {
	const [file, setFile] = useState(null);
	const [fileId, setFileId] = useState(null); // Store uploaded file ID

	// Handle file selection
	const handleFileChange = (e) => {
		setFile(e.target.files[0]);
	};

    const saveDesc = async () => {
        const desc = document.querySelector("textarea").value;
        console.log(desc);
        try {
            const response = await fetch("http://localhost:8000/saveDesc", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ desc }),
            });

            const result = await response.json();

            if (response.ok) {
                alert("Description saved successfully!");
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Error saving description:", error);
            alert("Failed to save description.");
        }
    }
	// Handle file upload
	const handleUpload = async () => {
		if (!file) {
			alert("Please select a PDF file.");
			return;
		}

		const formData = new FormData();
		formData.append("file", file);

		try {
			const response = await fetch("http://localhost:8000/upload", {
				method: "POST",
				body: formData,
			});

			const result = await response.json();

			if (response.ok) {
				setFileId(result.file_id); // Save file ID for download
				alert("File uploaded successfully!");
			} else {
				alert("Error: " + result.error);
			}
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
