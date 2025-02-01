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
            "You are a professional career consultant. A candidate has provided their resume details below, "
            "and they are applying for a job with the following description.\n\n"
            "Job Description:\n"
            "{job_description}\n\n"
            "Candidate's Resume and Experience (extracted from PDF):\n"
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
            # Assume the response is a dictionary with a 'text' field.
            if "text" in response:
                return response["text"]
            else:
                logging.error(f"Invalid response from Ollama API: {response}")
                raise LLMIntegrationError("Invalid response from Ollama API: missing 'text' field.")
        except Exception as e:
            logging.error(f"Error calling Ollama API: {e}")
            raise LLMIntegrationError(f"Error calling Ollama API: {e}")

    def transform_resume(self, job_description: str, resume_pdf: Union[str, IO]) -> str:
        """
        Transforms a candidate's resume (provided as a PDF) based on the provided job description by:
        
            1. Extracting text from the PDF.
            2. Building a prompt using the job description and the extracted resume text.
            3. Sending the prompt to the LLM via the Ollama client.
            4. Returning the updated resume.
        
        Args:
            job_description (str): The job description text.
            resume_pdf (Union[str, IO]): The candidate's resume as a PDF file (file path or file-like object).
            
        Returns:
            str: The updated resume generated by the LLM.
        """
        resume_text = self.extract_text_from_pdf(resume_pdf)
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

    # For testing, ensure that 'sample_resume.pdf' exists in your working directory.
    # This PDF should contain the candidate's resume details.
    sample_resume_pdf = "Resume.pdf"

    # Initialize the LLM integration instance
    llm_integration = LLMIntegration(model="deepseek-r1:7b")  # Replace with your actual Ollama model name

    try:
        # Get the transformed resume by passing the PDF file path (or a file-like object)
        modified_resume = llm_integration.transform_resume(sample_job_description, sample_resume_pdf)
        print("Modified Resume:\n")
        print(modified_resume)
    except LLMIntegrationError as error:
        print(f"An error occurred during LLM integration: {error}")
