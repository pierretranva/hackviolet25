import logging
import re
from typing import Union, IO
import PyPDF2
# Make sure you have installed the official Ollama client (if available).
import ollama

class LLMIntegrationError(Exception):
    pass

class LLMIntegration:
    #A class to handle integration with the local LLM using the Ollama API/client.
    def __init__(self, model: str = "default-model", timeout: int = 30):
        # Initialize the LLMIntegration instance.
        self.model = model
        self.timeout = timeout  


    @staticmethod
    def extract_text_from_pdf(pdf_input: Union[str, IO]) -> str:
        #Extracts text from a PDF file.
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
        #Constructs a prompt for the LLM based on job details and the candidate's extracted resume text.
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
        #Sends the constructed prompt to the LLM via the Ollama API/client and returns the generated response.
        try:
            # Check if 'generate' exists in the ollama module
            generate_fn = getattr(ollama, "generate", None)
            if not callable(generate_fn):
                # For testing purposes, simulate a response.
                simulated_response = {"response": "Simulated response based on prompt: " + prompt[:50] + "..."}
                return simulated_response["response"]
            # Using the Ollama client to generate a response.
            # The following function call is based on an assumed API for the Ollama client.
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
            )
            # The Ollama API response contains the generated text in the 'response' field
            if hasattr(response, "response"):
                return response.response
            # if isinstance(response, dict) and 'response' in response:
            #     return response['response']
            else:
                logging.error(f"Invalid response from Ollama API: {response}")
                raise LLMIntegrationError("Invalid response from Ollama API: missing 'response' field.")
        except Exception as e:
            logging.error(f"Error calling Ollama API: {e}")
            raise LLMIntegrationError(f"Error calling Ollama API: {e}")

    def transform_resume(self, job_description: str,  resume_pdf: Union[str, IO]) -> str:
        #Transforms a candidate's resume based on the provided job description by:
        resume_text = self.extract_text_from_pdf(resume_pdf)
        prompt = self.build_prompt(job_description, resume_text)
        updated_resume = self.call_llm(prompt)
        return updated_resume
    
    def string_to_markdown(self, resume_as_string: str, output_path: str = "UpdatedResume.md") -> str:
        #Converts a resume string into markdown format using the LLM, writes the markdown to a file, 
        #and returns the markdown string.
        # prompt = (
        #     "{resume_string}\n\n"
        #     "Please convert the resume to markdown format only. "
        #     "Do not provide any additional information or formatting."
        #     "Surround the markdown code resume with (<RESUME>) to indicate code block."
        # )
        prompt = (
"Convert the following resume into Markdown format. Return only the Markdown code, without any explanations or additional text. Wrap the output strictly between the delimiters `[[START_MARKDOWN]]` and `[[END_MARKDOWN]]`."
"Resume:"
"{resume_string}"

         "Resume:"
        "{resume_string}"
        )
        prompt = prompt.format(resume_string=resume_as_string)
        markdown_resume = self.call_llm(prompt)
        markdown_resume = re.sub(r"<think>.*?</think>", "", markdown_resume, flags=re.DOTALL)
        
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_resume)
            logging.info(f"Markdown resume written to {output_path}")
        except Exception as e:
            logging.error(f"Error writing markdown file: {e}")
            raise LLMIntegrationError(f"Error writing markdown file: {e}")
            
        return markdown_resume
    

    # def short_job_description(self, job_description: str) -> str:
    #     #Constructs a prompt for the LLM based on job details and the candidate's extracted resume text.
    #     prompt_template = (
    #         "You are a proffessional job description shortener.\n You have to shorten this job description into, "
    #         "5 key bullet points without altering any of the details of the listing.\n Do not have the 5 bullet points "
    #         "have sub bullet points. Don't go over more than 5 sentences."
    #         "{job_description}\n\n"
    #     )
    #     prompt = prompt_template.format(job_description=job_description)
    #     return prompt



if __name__ == "__main__":
    # Sample job description
    sample_job_description = (
        "We are looking for a seasoned software engineer with expertise in backend development, "
        "experience with Python, FastAPI, and cloud services. The candidate should have a strong understanding "
        "of microservices architecture and scalable system design."
    )
    # Specify the path to the candidate's resume PDF
    sample_resume_pdf = "Resume1.pdf"
    # Specify the output markdown file path
    output_markdown_file = "UpdatedResume.md"
    
    # Initialize the LLM integration instance
    llm_integration = LLMIntegration(model="deepseek-r1:7b")  # Replace with your actual Ollama model name

    try:
         # Get the updated resume from the PDF based on the job description
         modified_resume = llm_integration.transform_resume(sample_job_description, sample_resume_pdf)
         print("Modified Resume:\n")
         print(modified_resume)
        
         # Convert the updated resume to markdown format and write to file
         markdown_resume = llm_integration.string_to_markdown(modified_resume, output_markdown_file)
         print(f"Markdown resume written to: {output_markdown_file}")
    except LLMIntegrationError as error:
         print(f"An error occurred during LLM integration: {error}")

    # ----- Test for short_job_description -----
    # try:
    #     # print("\n=== Testing short_job_description ===")
    #     # Generate the prompt for the short job description
    #     # short_desc_prompt = llm_integration.short_job_description(sample_job_description)
        
    #     # Optionally, call the LLM to get the shortened job description
    #     # shortened_job_description = llm_integration.call_llm(short_desc_prompt)
    #     # print("\nShortened Job Description Output:")
    #     # print(shortened_job_description)
        
    # except LLMIntegrationError as error:
    #     print(f"An error occurred during the short job description test: {error}")
    # except LLMIntegrationError as error:
    #     print(f"An error occurred during the short job description test: {error}")