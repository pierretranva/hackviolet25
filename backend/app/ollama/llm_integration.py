# llm_integration.py

import logging
from typing import Union, IO
import PyPDF2
# Import the Ollama API client.
# Make sure you have installed the official Ollama client (if available).
import ollama

# Custom exception for LLM Integration errors
class LLMIntegrationError(Exception):
    pass

class LLMIntegration:
    """
    A class to handle integration with the local LLM using the Ollama API/client.
    
    Attributes:
        model (str): The model identifier to be used.
        timeout (int): Timeout (in seconds) for API calls (if applicable in client usage).
    """

    def __init__(self, model: str = "default-model", timeout: int = 30):
        """
        Initialize the LLMIntegration instance.
        
        Args:
            model (str): Model name or identifier.
            timeout (int): Request timeout in seconds.
        """
        self.model = model
        self.timeout = timeout  # Currently unused in this example; add client-specific timeout if available.

    @staticmethod
    def read_text_file(file_path: str) -> str:
        """
        Reads text from a file.
        
        Args:
            file_path (str): Path to the text file.
            
        Returns:
            str: The content of the text file.
        """
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error reading text file: {e}")
            raise LLMIntegrationError(f"Error reading text file: {e}")

    @staticmethod
    def extract_text_from_pdf(pdf_input: Union[str, IO]) -> str:
        """
        Extracts text from a PDF file.
        
        Args:
            pdf_input (Union[str, IO]): The PDF file path (if str) or a file-like object (if IO).
            
        Returns:
            str: The extracted text from the PDF.
        """
        text = ""
        try:
            if isinstance(pdf_input, str):
                with open(pdf_input, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            else:
                # Assume pdf_input is a file-like object (e.g., from FastAPI's UploadFile.file)
                pdf_reader = PyPDF2.PdfReader(pdf_input)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {e}")
            raise LLMIntegrationError(f"Error extracting text from PDF: {e}")
        return text

    def build_prompt(self, job_description: str, resume_text: str) -> str:
        """
        Constructs a prompt for the LLM based on job details and the candidate's extracted resume text.
        
        The prompt instructs the LLM to generate an updated version of the resume that
        better aligns with the job requirements.
        
        Args:
            job_description (str): The job description text.
            resume_text (str): The candidate's resume text extracted from the PDF.
            
        Returns:
            str: A formatted prompt string.
        """
        prompt_template = (
            "You are a professional resume editor. A candidate has provided their resume details below, "
            "and they are applying for a job with the following description.\n\n"
            "Job Description:\n"
            "{job_description}\n\n"
            "Candidate's Resume and Experience:\n"
            "{resume_text}\n\n"
            "Please provide an updated version of the candidate's resume that better aligns with the job requirements, "
            "emphasizing relevant skills and experiences. The resume should remain professional and formatted clearly."
        )
        prompt = prompt_template.format(job_description=job_description, resume_text=resume_text)
        return prompt

    def call_llm(self, prompt: str) -> str:
        """
        Sends the constructed prompt to the LLM via the Ollama API/client and returns the generated response.
        
        Args:
            prompt (str): The prompt string to be sent to the LLM.
            
        Returns:
            str: The generated text from the LLM, which is expected to be the modified resume.
            
        Raises:
            LLMIntegrationError: If the API call fails or the response is invalid.
        """
        try:
            # Using the Ollama client to generate a response.
            # The following function call is based on an assumed API for the Ollama client.
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
            )
            # The Ollama API response contains the generated text in the 'response' field
            if hasattr(response, 'response'):
                return response.response
            else:
                logging.error(f"Invalid response from Ollama API: {response}")
                raise LLMIntegrationError("Invalid response from Ollama API: missing 'response' field.")
        except Exception as e:
            logging.error(f"Error calling Ollama API: {e}")
            raise LLMIntegrationError(f"Error calling Ollama API: {e}")

    def transform_resume(self, job_description: str, experience_file: str) -> str:
        """
        Transforms a candidate's resume based on the provided job description by:
        
            1. Reading experience from text file.
            2. Building a prompt using the job description and the experience text.
            3. Sending the prompt to the LLM via the Ollama client.
            4. Returning the updated resume.
        
        Args:
            job_description (str): The job description text.
            experience_file (str): Path to the text file containing experience.
            
        Returns:
            str: The updated resume generated by the LLM.
        """
        resume_text = self.read_text_file(experience_file)
        prompt = self.build_prompt(job_description, resume_text)
        updated_resume = self.call_llm(prompt)
        return updated_resume

# Example usage for testing purposes
if __name__ == "__main__":
    # Sample job description
    sample_job_description = (
        "We are looking for a seasoned software engineer with expertise in backend development, "
        "experience with Python, FastAPI, and cloud services. The candidate should have a strong understanding "
        "of microservices architecture and scalable system design."
    )

    # Initialize the LLM integration instance
    llm_integration = LLMIntegration(model="deepseek-r1:7b")  # Replace with your actual Ollama model name

    try:
        # Get the transformed resume by passing the experience text file
        modified_resume = llm_integration.transform_resume(sample_job_description, "experience.txt")
        print("Modified Resume:\n")
        print(modified_resume)
    except LLMIntegrationError as error:
        print(f"An error occurred during LLM integration: {error}")
