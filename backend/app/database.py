# database.py
import os
import gridfs
from pymongo import MongoClient
from webscrape import WebScrape  # Ensure webscrape.py is accessible in the same directory or Python path
from ollama.llm_integration import LLMIntegration
def main():
    # --- Setup MongoDB Connection ---
    # Use an environment variable for your MongoDB URI, or default to localhost for testing.
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://hackviolet:hackviolet@cluster0.akrxj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    client = MongoClient(MONGODB_URI)
    # Use a dedicated test database to avoid interfering with production data.
    db = client["jobapp_test_db"]
    collection = db["job_postings"]

    # Setup GridFS for storing binary files (PDF in this case)
    fs = gridfs.GridFS(db)


    # --- Setup the Web Scraper ---
    job_url = "https://www.linkedin.com/jobs/view/4134536792/?alternateChannel=search&refId=QrhnPUM74Lh50t7qdwpcBw%3D%3D&trackingId=V3DXFsM%2Bb9qQTdJ65AscTw%3D%3D"  # Change to a real URL for testing
    scraper = WebScrape(job_url)

    print("Starting the scraping process...")
    scraper.scrape()  # This launches the browser, logs in, navigates to the job posting, and scrapes details.
    
    job_details = scraper.get_details()
    if not job_details:
        print("No job details were scraped. Please verify the job URL or the scraper logic.")
        return

    print("Scraped Job Details:")
    print(job_details)      
    markdown_file_path = os.path.join("ollama", "UpdatedResume.md")
    markdown_file_content = None
    if os.path.exists(markdown_file_path):
        try:
            with open(markdown_file_path, "rb") as md_file:
                md_data = md_file.read()
                # Store the Markdown file in GridFS; the file id is returned.
                markdown_file_id = fs.put(md_data, filename="UpdatedResume.md", contentType="text/markdown")
                print(f"Markdown file stored in MongoDB with file id: {markdown_file_id}")
        except Exception as e:
            print("Error reading or storing the Markdown file:", e)
    else:
        print(f"Markdown file '{markdown_file_path}' not found.")

    # --- Read and store the PDF file using GridFS ---
    pdf_file_path = os.path.join("ollama", "Resume.pdf")  
    pdf_file_id = None
    if os.path.exists(pdf_file_path):
        try:
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                # Store the PDF file in GridFS; the file id is returned.
                pdf_file_id = fs.put(pdf_data, filename="Resume.pdf", contentType="application/pdf")
                print(f"PDF file stored in MongoDB with file id: {pdf_file_id}")
        except Exception as e:
            print("Error reading or storing the PDF file:", e)
    else:
        print(f"PDF file '{pdf_file_path}' not found.")

    # --- Prepare data to insert ---
    # In a real-world application, the following fields would come from your frontend.
    document = {
        "job_url": job_url,
        "job_details": job_details,
        "name": "Test Job Name",               
        "date": "2025-02-01",                   
        "chips": ["Python(bg-blue-500), FastAPI(bg-green-500)"], 
        "markdown_file": markdown_file_content,
        "pdf_file_id": pdf_file_id
    }

    # --- Insert the scraped data into MongoDB ---
    insert_result = collection.insert_one(document)
    print(f"Document inserted with _id: {insert_result.inserted_id}")

    # --- Retrieve and print the inserted document to verify the data ---
    retrieved_doc = collection.find_one({"_id": insert_result.inserted_id})
    print("Retrieved Document from MongoDB:")
    print(retrieved_doc)

if __name__ == "__main__":
    main()
