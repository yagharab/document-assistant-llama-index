# Smart Document Assistant

A document analysis tool built with LlamaIndex that helps you understand and interact with your PDF documents using AI.

## Features
- PDF document processing
- Natural language querying
- Document summarization
- Interactive web interface

## Setup
1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Project Structure
- `app.py`: Main Streamlit application
- `document_processor.py`: Core document processing logic
- `data/`: Directory for storing uploaded documents 