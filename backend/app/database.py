# database.py
import os
from pymongo import MongoClient
from webscrape import WebScrape  # Ensure webscrape.py is accessible in the same directory or Python path

def main():
    # --- Setup MongoDB Connection ---
    # Use an environment variable for your MongoDB URI, or default to localhost for testing.
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://hackviolet:hackviolet@cluster0.akrxj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    client = MongoClient(MONGODB_URI)
    # Use a dedicated test database to avoid interfering with production data.
    db = client["jobapp_test_db"]
    collection = db["job_postings"]

    # --- Setup the Web Scraper ---
    # Replace this with a valid LinkedIn job posting URL for your test.
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

    # --- Prepare data to insert ---
    # In a real-world application, the following fields would come from your frontend.
    document = {
        "job_url": job_url,
        "job_details": job_details,
        "name": "Test Job Name",               # Example string for job name
        "date": "2025-02-01",                   # Example date string (you might format this as needed)
        "chips": ["Python(bg-blue-500), FastAPI(bg-green-500)"]  # Example chips as a string
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
