# Document Information Extractor

A Python tool for extracting structured information from PDF documents using PyMuPDF, OpenAI, and Pydantic validation.

## 🚀 Features

- **AI-Powered Extraction**: Uses OpenAI GPT-4 for intelligent document analysis
- **Reliable PDF Reading**: PyMuPDF for robust text extraction from PDF documents
- **Smart Fallback**: Basic pattern matching when AI is unavailable
- **Structured Data Output**: Pydantic models ensure data validation and type safety
- **JSON Export**: Clean, structured output ready for further processing
- **Medical Document Support**: Optimized for scientific and medical papers

## 📋 Extracted Fields

### Required Fields
- `document`: Document title or identifier
- `Introduction`: Brief introduction or summary
- `Thoughts`: Main thoughts, insights, or key points
- `Answers`: Key answers, conclusions, or findings

### Optional Fields
- `Hallmarks`: Key characteristics or distinguishing features
- `Further_Reading`: Recommended additional reading
- `Images`: Description of relevant images, figures, or diagrams
- `Further_Development`: Areas suggested for further research/development
- `Thoughts_I`: Additional thoughts - Part I
- `Answers_I`: Additional answers - Part I
- `Answers_II`: Additional answers - Part II
- `Further_Thoughts`: Further thoughts and considerations
- `Ependymoma`: Ependymoma-related information

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies

```bash
# Create virtual environment
python3 -m venv document_extractor_env
source document_extractor_env/bin/activate  # On macOS/Linux
# document_extractor_env\Scripts\activate  # On Windows

# Install required packages
pip install PyMuPDF pydantic openai
```

### OpenAI API Setup

1. **Get OpenAI API Key**:
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy your API key (starts with `sk-`)

2. **Set API Key** (choose one method):

   **Option A: Environment Variable (Recommended)**
   ```bash
   export OPENAI_API_KEY="sk-your-actual-api-key-here"
   ```

   **Option B: Edit Code Directly**
   ```python
   # In extract.py, replace:
   openai_api_key = "sk-your-actual-api-key-here"
   ```

   **Option C: .env File**
   ```bash
   echo "OPENAI_API_KEY=sk-your-actual-api-key-here" > .env
   pip install python-dotenv
   ```

## 📖 Usage

### Basic Usage

1. **Set up OpenAI API key** (see installation section)

2. **Update the PDF path** in `extract.py`:
```python
pdf_path = "path/to/your/document.pdf"
```

3. **Run the extraction**:
```bash
python3 extract.py
```

4. **Check the output**: 
   - Console output with extraction summary
   - `extracted_document.json` with structured data

### Extraction Modes

**AI-Enhanced Extraction (Default)**
```python
# Uses OpenAI GPT-4 for intelligent analysis
doc_info = extract_with_openai(pdf_path, api_key)
```

**Basic Extraction (Fallback)**
```python
# Pattern-based extraction without AI
doc_info = extract_document_info(pdf_path, use_llm=False)
```

### Programmatic Usage

```python
from extract import extract_with_openai, DocumentInfo

# Extract with OpenAI
doc_info = extract_with_openai("document.pdf", "your-api-key")

# Access structured data
print(doc_info.document)
print(doc_info.Introduction)
print(doc_info.Thoughts)

# Export to JSON
with open("output.json", "w") as f:
    f.write(doc_info.model_dump_json(indent=2))
```

## 📁 Project Structure

```
document-extractor/
├── extract.py              # Main extraction script
├── extracted_document.json # Output file (generated)
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Extraction Pipeline
The extractor follows this pipeline:
1. **PDF Reading**: Extract raw text using PyMuPDF
2. **Text Cleaning**: Remove headers, footers, normalize whitespace
3. **Basic Structure**: Pattern-based section identification
4. **AI Enhancement**: OpenAI GPT-4 analysis and improvement
5. **Pydantic Validation**: Ensure data structure integrity

### OpenAI Settings
```python
# Default model: GPT-4
# Temperature: 0.1 (focused, deterministic)
# Max tokens: 4000
# Fallback: Basic extraction if API fails
```

### Customization
- **Model Selection**: Change GPT model in `openai_llm_function()`
- **Extraction Logic**: Modify `extract_document_structure()`
- **Field Mapping**: Update `DocumentInfo` Pydantic model
- **API Settings**: Adjust temperature, max_tokens in LLM functions

## 📊 Example Output

```json
{
  {
  "document": "First report of tumor treating fields use in combination with bevacizumab in a pediatric patient: a case report",
  "Introduction": "This document reports the first case of a pediatric patient with glioblastoma (GBM; WHO grade IV astrocytoma) successfully treated with tumor treating fields (TTF). The patient was diagnosed with GBM when 13 years of age and progressed through surgical resection, radiotherapy and chemotherapy.",
  "Thoughts": "The patient was monitored for 6 months with subsequent stable disease observed radiographically and clinically for 7 months while adherent to Optune® (TTF). TTF thereby played a role in forestalling recurrent GBM growth in this young woman for 7 months without significant adverse effects.",
  "Answers": "The authors propose that TTF therapy is a potential valuable treatment in this small, but sick, patient population.",
  "Hallmarks": "The patient was diagnosed with GBM when 13 years of age and progressed through surgical resection, radiotherapy and chemotherapy. TTF therapy played a role in forestalling recurrent GBM growth in this young woman for 7 months without significant adverse effects.",
  "Further_Reading": null,
  "Images": "The document includes MRI brain images at the time of tumor diagnosis, postoperative MRI brain images shortly after starting bevacizumab and tumor treating fields, and postoperative MRI brain images at the time of tumor progression.",
  "Further_Development": "The authors suggest that TTF should undergo further evaluation in clinical trials to confirm their benefit in children as observed in adult high-grade glioma.",
  "Thoughts_I": "The use of TTF in cases of pediatric high-grade glioma remains a novel suggestion with no clinical trials currently in progress.",
  "Answers_I": "The authors suggest that TTF are a potential valuable treatment in this very small, but acutely sick, patient population.",
  "Answers_II": null,
  "Further_Thoughts": "The authors state that they have obtained appropriate institutional review board approval or have followed the principles outlined in the Declaration of Helsinki for all human or animal experimental investigations.",
  "Ependymoma": null
}
}
```

## 🧪 Testing

Test with the included medical case report:
```bash
# Ensure your PDF path and OpenAI API key are set
python3 extract.py
```

Expected output:
- ✅ PDF reading with character count
- ✅ Text cleaning and processing  
- ✅ Basic structure extraction
- ✅ OpenAI enhancement (if API key provided)
- ✅ Pydantic validation
- ✅ JSON file generation

### Sample Console Output
```
📄 Reading PDF: your_document.pdf
✅ Extracted 28433 characters from PDF
🧹 Cleaning PDF text...
✅ Cleaned text: 27883 characters
📊 Extracting document structure...
✅ Document structure extracted
🤖 Enhancing extraction with LLM...
✅ LLM enhancement completed
🔍 Creating DocumentInfo with Pydantic validation...
✅ Pydantic validation successful
🎉 Extraction pipeline completed successfully!
```

## 🔍 Troubleshooting

### Common Issues

**1. OpenAI API Issues**
```bash
# API key not set
export OPENAI_API_KEY="sk-your-actual-key"

# API quota exceeded
# Check usage at https://platform.openai.com/usage

# Network issues
# Check internet connection and OpenAI status
```

**2. PyMuPDF Installation Problems**
```bash
# Try alternative installation methods
pip install --upgrade PyMuPDF
pip install pymupdf  # Alternative package name
```

**3. PDF Reading Errors**
- Ensure PDF file exists and is readable
- Check file path is correct
- Verify PDF is not corrupted or password-protected

**4. Extraction Quality Issues**
- Basic extraction used instead of AI (check API key)
- PDF contains mostly images (try OCR preprocessing)
- Complex layout (AI extraction should handle better)

### Error Messages
- `OpenAI API error`: Check API key and internet connection
- `FileNotFoundError`: Check PDF file path
- `Could not extract text`: Verify PDF contains extractable text
- `Pydantic validation error`: Check extracted data structure

## 🚀 Advanced Usage

### Custom OpenAI Settings
```python
# Use different model
doc_info = extract_with_openai(pdf_path, api_key, model="gpt-3.5-turbo")

# Custom extraction with specific parameters
def custom_openai(prompt, api_key):
    # Your custom OpenAI configuration
    return openai_llm_function(prompt, api_key, model="gpt-4")

doc_info = extract_document_info(pdf_path, use_llm=True, llm_function=custom_openai)
```

### Batch Processing
```python
import glob

pdf_files = glob.glob("pdfs/*.pdf")
results = []

for pdf_file in pdf_files:
    try:
        doc_info = extract_with_openai(pdf_file, api_key)
        results.append(doc_info.model_dump())
    except Exception as e:
        print(f"Failed to process {pdf_file}: {e}")

# Save all results
with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Integration with Other LLMs
```python
# Example with Anthropic Claude
def claude_llm_function(prompt):
    # Your Anthropic integration
    return anthropic_api_call(prompt)

doc_info = extract_document_info(pdf_path, use_llm=True, llm_function=claude_llm_function)
```



## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


### Common Setup Issues
- **API Key**: Make sure your OpenAI API key is valid and has credits
- **Dependencies**: Install all required packages: `pip install PyMuPDF pydantic openai`
- **PDF Format**: Ensure your PDF contains extractable text (not just images)
- **Network**: Check internet connection for OpenAI API calls

