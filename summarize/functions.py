import os
from django.conf import settings
from langchain import PromptTemplate, LLMChain
from langchain.llms import Cohere
from langchain.document_loaders import PDFMinerLoader

from .models import Submission

# Function to handle file upload from input
def handle_uploaded_files(f):
    # Ensure the upload directory exists
    upload_dir = os.path.join('summarize/static/upload/')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    # Save the file in the directory
    file_path = os.path.join(upload_dir, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path
            
## LangChain functions
def query_llm():
    os.environ["COHERE_API_KEY"] = "XPPJkZ6OHZXtRRvCL17HEgz3y6vLHcNYhkybLeHL"  # WARNING: API KEY
    llm = Cohere(model='command-xlarge')

    query = Submission.objects.last()
    paper_path = query.paper.path

    try:
        paper_object = PDFMinerLoader(file_path=paper_path)
        paper = paper_object.load()[0].page_content.strip()  # Load the full content for processing
        
        # Use the full content directly
        cleaned_text = paper

        style = """SECTION: name of a section in the text \
        SUMMARY: summary of the text under the SECTION.
        """

        template = """
        The following text delimited by triple backticks is from a \
        research paper. Each text corresponds to a certain section in the \
        research paper.

        Given this text, return a summary in the following style {style}
        ```
        {text}
        ```

        """

        prompt = PromptTemplate(template=template, input_variables=["text", "style"])

        llm_chain = LLMChain(prompt=prompt, llm=llm)

        input_variables = {
            'text': cleaned_text,
            'style': style
        }

        response = llm_chain.run(input_variables)
        return response
    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"