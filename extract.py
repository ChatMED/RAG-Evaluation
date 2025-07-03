from pydantic import BaseModel, Field
from typing import Optional
import json
import re
import os
from pathlib import Path
import fitz  # PyMuPDF

class DocumentInfo(BaseModel):
    """
    Pydantic model for extracting document information.
    Required fields: document, Introduction, Thoughts, Answers
    Optional fields: Hallmarks, Further_Reading, Images, Further_Development, 
    Thoughts_I, Answers_I, Answers_II, Further_Thoughts, Ependymoma
    """
    
    # Obligatory fields
    document: str = Field(..., description="Document title or identifier")
    Introduction: str = Field(..., description="Introduction or summary of the document")
    Thoughts: str = Field(..., description="Main thoughts or key insights from the document")
    Answers: str = Field(..., description="Key answers or conclusions from the document")
    
    # Optional fields
    Hallmarks: Optional[str] = Field(None, description="Key hallmarks or characteristics")
    Further_Reading: Optional[str] = Field(None, description="Recommended further reading")
    Images: Optional[str] = Field(None, description="Description of relevant images or figures")
    Further_Development: Optional[str] = Field(None, description="Areas for further development")
    Thoughts_I: Optional[str] = Field(None, description="Additional thoughts - Part I")
    Answers_I: Optional[str] = Field(None, description="Additional answers - Part I")
    Answers_II: Optional[str] = Field(None, description="Additional answers - Part II")
    Further_Thoughts: Optional[str] = Field(None, description="Further thoughts and considerations")
    Ependymoma: Optional[str] = Field(None, description="Ependymoma-related information")

def read_pdf_file(file_path: str) -> str:
    """
    Step 1: Read PDF file using PyMuPDF and extract raw text
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    print(f"📄 Reading PDF: {file_path}")
    
    try:
        doc = fitz.open(file_path)
        text = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text() + "\n"
        
        doc.close()
        
        if not text.strip():
            raise ValueError("Could not extract text from PDF file")
        
        print(f"✅ Extracted {len(text)} characters from PDF")
        return text
        
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        raise

def clean_pdf_text(raw_text: str) -> str:
    """
    Step 2: Clean and process the extracted PDF text
    """
    print("🧹 Cleaning PDF text...")
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', raw_text)
    
    # Remove page numbers and headers/footers
    text = re.sub(r'\n\d+\n', '\n', text)
    
    # Remove URLs and email addresses
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    
    # Clean up extra newlines
    text = re.sub(r'\n+', '\n', text)
    
    print(f"✅ Cleaned text: {len(text)} characters")
    return text.strip()

def extract_title(text: str) -> str:
    """
    Extract document title from text
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for title in first 20 lines
    for line in lines[:20]:
        # Skip common header elements
        if any(skip in line.lower() for skip in ['issn', 'doi', '©', 'page', 'volume']):
            continue
        # Title is usually longer than 10 characters
        if len(line) > 10:
            return line
    
    return "Document title not found"

def extract_section_by_pattern(text: str, patterns: list, max_chars: int = 2000) -> str:
    """
    Extract text section based on patterns/keywords
    """
    text_lower = text.lower()
    
    for pattern in patterns:
        # Find pattern in text
        pattern_match = re.search(pattern, text_lower)
        if pattern_match:
            start_pos = pattern_match.end()
            
            # Find next section or end of relevant content
            end_patterns = [r'\n[A-Z][A-Z\s]+\n', r'\nreferences\n', r'\nconclusion\n', r'\ndiscussion\n']
            end_pos = len(text)
            
            for end_pattern in end_patterns:
                end_match = re.search(end_pattern, text_lower[start_pos:])
                if end_match:
                    end_pos = start_pos + end_match.start()
                    break
            
            # Extract and clean section
            section = text[start_pos:end_pos].strip()
            return section[:max_chars] if section else None
    
    return None

def extract_references(text: str) -> str:
    """
    Extract references/citations from text
    """
    # Look for references section
    ref_patterns = [r'\nreferences\n', r'\nbibliography\n', r'\ncitations\n']
    ref_text = extract_section_by_pattern(text, ref_patterns, max_chars=1500)
    
    if ref_text:
        # Clean up reference list
        refs = []
        for line in ref_text.split('\n'):
            line = line.strip()
            if len(line) > 20 and not line.isdigit():  # Skip short lines and page numbers
                refs.append(line)
        
        return '; '.join(refs[:5])  # Return first 5 references
    
    return None

def extract_figures_and_images(text: str) -> str:
    """
    Extract information about figures, tables, and images
    """
    figure_info = []
    
    # Find figure and table mentions
    figure_patterns = [
        r'Figure \d+[:.][^\.]*\.',
        r'Fig\. \d+[:.][^\.]*\.',
        r'Table \d+[:.][^\.]*\.',
        r'Image \d+[:.][^\.]*\.'
    ]
    
    for pattern in figure_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        figure_info.extend(matches)
    
    return '; '.join(figure_info[:10]) if figure_info else None

def extract_document_structure(clean_text: str) -> dict:
    """
    Step 3: Extract structured information from clean text
    """
    print("📊 Extracting document structure...")
    
    extracted_data = {}
    
    # Required fields
    extracted_data["document"] = extract_title(clean_text)
    
    # Extract Introduction
    intro_patterns = [r'\nintroduction\n', r'\nabstract\n', r'\nsummary\n', r'\nbackground\n']
    intro = extract_section_by_pattern(clean_text, intro_patterns, max_chars=1500)
    extracted_data["Introduction"] = intro if intro else "Introduction section not found in document"
    
    # Extract Thoughts (Methods/Discussion)
    thought_patterns = [r'\nmethods\n', r'\nmethodology\n', r'\napproach\n', r'\ndiscussion\n']
    thoughts = extract_section_by_pattern(clean_text, thought_patterns, max_chars=1500)
    extracted_data["Thoughts"] = thoughts if thoughts else "Methods/Discussion section not found in document"
    
    # Extract Answers (Results/Conclusions)
    answer_patterns = [r'\nresults\n', r'\nfindings\n', r'\nconclusion\n', r'\noutcome\n']
    answers = extract_section_by_pattern(clean_text, answer_patterns, max_chars=1500)
    extracted_data["Answers"] = answers if answers else "Results/Conclusions section not found in document"
    
    # Optional fields
    extracted_data["Further_Reading"] = extract_references(clean_text)
    extracted_data["Images"] = extract_figures_and_images(clean_text)
    
    # Look for specific optional content
    limitation_patterns = [r'\nlimitations\n', r'\nfuture work\n', r'\nfuture research\n']
    limitations = extract_section_by_pattern(clean_text, limitation_patterns, max_chars=1000)
    extracted_data["Further_Development"] = limitations
    
    print("✅ Document structure extracted")
    return extracted_data

def create_document_info(extracted_data: dict) -> DocumentInfo:
    """
    Step 4: Create and validate DocumentInfo using Pydantic
    """
    print("🔍 Creating DocumentInfo with Pydantic validation...")
    
    try:
        # Create DocumentInfo object with Pydantic validation
        doc_info = DocumentInfo(**extracted_data)
        print("✅ Pydantic validation successful")
        return doc_info
        
    except Exception as e:
        print(f"❌ Pydantic validation error: {e}")
        raise

def create_llm_prompt(clean_text: str) -> str:
    """
    Create prompt for LLM when basic extraction needs enhancement
    """
    prompt = f"""
Analyze this document and extract information in JSON format. Return ONLY valid JSON.

Required fields:
- document: Document title
- Introduction: Introduction or summary  
- Thoughts: Main thoughts, insights, methodology
- Answers: Key findings, results, conclusions

Optional fields (use null if not found):
- Hallmarks: Key characteristics
- Further_Reading: References or recommended reading
- Images: Description of figures/tables/images
- Further_Development: Future work, limitations, next steps
- Thoughts_I: Additional thoughts part I
- Answers_I: Additional answers part I  
- Answers_II: Additional answers part II
- Further_Thoughts: Further considerations
- Ependymoma: Any ependymoma-related content

Document text:
{clean_text}

Return only the JSON object:
"""
    return prompt

def enhance_with_llm(extracted_data: dict, clean_text: str, llm_function=None) -> dict:
    """
    Enhance extraction using LLM when basic extraction is insufficient
    """
    if not llm_function:
        print("⚠️ No LLM function provided, using basic extraction only")
        return extracted_data
    
    print("🤖 Enhancing extraction with LLM...")
    
    try:
        # Create LLM prompt
        prompt = create_llm_prompt(clean_text)
        
        # Call LLM
        llm_response = llm_function(prompt)
        
        # Parse LLM response
        if isinstance(llm_response, str):
            # Clean response (remove any non-JSON content)
            json_start = llm_response.find('{')
            json_end = llm_response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_content = llm_response[json_start:json_end]
                llm_data = json.loads(json_content)
            else:
                raise ValueError("No valid JSON found in LLM response")
        else:
            llm_data = llm_response
        
        # Merge LLM data with basic extraction (LLM takes priority)
        enhanced_data = extracted_data.copy()
        for key, value in llm_data.items():
            if value and value != "null":  # Only use non-empty LLM values
                enhanced_data[key] = value
        
        print("✅ LLM enhancement completed")
        return enhanced_data
        
    except Exception as e:
        print(f"⚠️ LLM enhancement failed: {e}")
        print("Falling back to basic extraction")
        return extracted_data

# LLM Integration Examples
def openai_llm_function(prompt: str, api_key: str, model: str = "gpt-4") -> dict:
    """
    OpenAI integration function
    """
    try:
        import openai
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a document analysis expert. Extract information and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        raise ImportError("OpenAI package required: pip install openai")
    except Exception as e:
        raise Exception(f"OpenAI API error: {e}")

def anthropic_llm_function(prompt: str, api_key: str, model: str = "claude-3-sonnet-20240229") -> dict:
    """
    Anthropic Claude integration function
    """
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
        
    except ImportError:
        raise ImportError("Anthropic package required: pip install anthropic")
    except Exception as e:
        raise Exception(f"Anthropic API error: {e}")

def extract_document_info(pdf_path: str, use_llm: bool = False, llm_function=None) -> DocumentInfo:
    """
    Complete extraction pipeline: PDF → Text → Structure → LLM (optional) → Pydantic
    """
    print("🚀 Starting document extraction pipeline...")
    
    # Step 1: Read PDF
    raw_text = read_pdf_file(pdf_path)
    
    # Step 2: Clean text
    clean_text = clean_pdf_text(raw_text)
    
    # Step 3: Extract basic structure
    extracted_data = extract_document_structure(clean_text)
    
    # Step 4: Enhance with LLM if requested
    if use_llm and llm_function:
        extracted_data = enhance_with_llm(extracted_data, clean_text, llm_function)
    elif use_llm and not llm_function:
        print("⚠️ LLM requested but no LLM function provided")
    
    # Step 5: Create and validate with Pydantic
    doc_info = create_document_info(extracted_data)
    
    print("🎉 Extraction pipeline completed successfully!")
    return doc_info

# Convenience functions for different LLM providers
def extract_with_openai(pdf_path: str, api_key: str, model: str = "gpt-4") -> DocumentInfo:
    """
    Extract document info using OpenAI
    """
    def llm_func(prompt):
        return openai_llm_function(prompt, api_key, model)
    
    return extract_document_info(pdf_path, use_llm=True, llm_function=llm_func)

def extract_with_anthropic(pdf_path: str, api_key: str, model: str = "claude-3-sonnet-20240229") -> DocumentInfo:
    """
    Extract document info using Anthropic Claude
    """
    def llm_func(prompt):
        return anthropic_llm_function(prompt, api_key, model)
    
    return extract_document_info(pdf_path, use_llm=True, llm_function=llm_func)

def save_extracted_data(doc_info: DocumentInfo, filename: str = "extracted_document.json") -> bool:
    """
    Save extracted and validated data to JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(doc_info.model_dump(), f, indent=2, ensure_ascii=False)
        
        print(f"💾 Data saved to {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        return False

def display_extraction_results(doc_info: DocumentInfo):
    """
    Display extraction results in a readable format
    """
    print("\n" + "="*60)
    print("📋 EXTRACTION RESULTS")
    print("="*60)
    
    print(f"\n📄 Document: {doc_info.document}")
    print(f"\n📖 Introduction: {doc_info.Introduction[:200]}{'...' if len(doc_info.Introduction) > 200 else ''}")
    print(f"\n💭 Thoughts: {doc_info.Thoughts[:200]}{'...' if len(doc_info.Thoughts) > 200 else ''}")
    print(f"\n💡 Answers: {doc_info.Answers[:200]}{'...' if len(doc_info.Answers) > 200 else ''}")
    
    # Optional fields
    if doc_info.Further_Reading:
        print(f"\n📚 Further Reading: {doc_info.Further_Reading[:150]}{'...' if len(doc_info.Further_Reading) > 150 else ''}")
    
    if doc_info.Images:
        print(f"\n🖼️ Images: {doc_info.Images[:150]}{'...' if len(doc_info.Images) > 150 else ''}")
    
    if doc_info.Further_Development:
        print(f"\n🔮 Further Development: {doc_info.Further_Development[:150]}{'...' if len(doc_info.Further_Development) > 150 else ''}")

# Main execution
if __name__ == "__main__":
    print("Document Information Extraction: PDF → Text → OpenAI → Pydantic")
    print("=" * 70)
    
    # PDF file path - UPDATE THIS PATH
    pdf_path = "/Users/jovanadobreva/Documents/Dataset/usecase generator/papers/usecase_pubmed.pdf"
    
    # OpenAI API Key - ADD YOUR API KEY HERE OR SET OPENAI_API_KEY ENVIRONMENT VARIABLE
    openai_api_key =  os.getenv("OPENAI_API_KEY") or "or add your api here"
    
    if Path(pdf_path).exists():
        try:

                
            print("🤖 Using OpenAI for enhanced extraction...")
            doc_info = extract_with_openai(pdf_path, openai_api_key)
            
            display_extraction_results(doc_info)
            save_extracted_data(doc_info)
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            print("Falling back to basic extraction...")
            
            try:
                doc_info = extract_document_info(pdf_path, use_llm=False)
                display_extraction_results(doc_info)
                save_extracted_data(doc_info)
            except Exception as fallback_error:
                print(f"❌ Basic extraction also failed: {fallback_error}")
            
    else:
        print(f"❌ PDF file not found: {pdf_path}")
        print("Please update the pdf_path variable with the correct path to your PDF file")