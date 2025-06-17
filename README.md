# RAGCare-QA: A Benchmark Dataset for Evaluating Retrieval-Augmented Generation Pipelines in Theoretical Medical Knowledge

## Overview

RAGCare-QA is a comprehensive dataset comprising 420 theoretical medical knowledge questions designed for evaluating Retrieval-Augmented Generation (RAG) pipelines in medical education and assessment contexts. Each question is carefully annotated with its optimal RAG pipeline type, making this dataset uniquely valuable for developing and benchmarking medical AI systems.

## Dataset Statistics

- **Total Questions**: 420
- **Medical Specialties**: 6 (Cardiology, Endocrinology, Family Medicine, Gastroenterology, Neurology, Oncology)
- **Complexity Levels**: 3 (Basic, Intermediate, Advanced)
- **RAG Pipeline Types**: 3 (Basic RAG, Multi-vector RAG, Graph-enhanced RAG)
- **Languages**: English (with some Slovenian source materials)
- **Format**: Multiple-choice questions (5 options: a-e)

## Dataset Composition

### By Complexity Level
| Complexity Level | Questions | Percentage |
|-----------------|-----------|------------|
| Basic | 150 | 35.7% |
| Intermediate | 181 | 43.1% |
| Advanced | 89 | 21.2% |

### By Medical Specialty
| Specialty | Basic | Intermediate | Advanced | Total |
|-----------|-------|--------------|----------|-------|
| Cardiology | 32 | 36 | 19 | 87 |
| Endocrinology | 28 | 32 | 14 | 74 |
| Family Medicine | 26 | 41 | 14 | 81 |
| Gastroenterology | 20 | 22 | 12 | 54 |
| Neurology | 20 | 22 | 15 | 57 |
| Oncology | 24 | 28 | 15 | 67 |

### By RAG Architecture Type
| RAG Architecture | Questions | Percentage | Description |
|-----------------|-----------|------------|-------------|
| Basic RAG | 315 | 75.0% | Direct factual queries with explicit terminology |
| Multi-vector RAG | 82 | 19.5% | Questions requiring diverse knowledge sources |
| Graph-enhanced RAG | 23 | 5.5% | Complex relationship-based queries |

## Data Structure

Each question entry contains the following fields:

```json
{
  "Type": "medical_specialty_category",
  "Complexity": "basic|intermediate|advanced",
  "Question": "multiple_choice_question_text",
  "Answer": "a|b|c|d|e",
  "Text Answer": "textual answer",
  "Reference": "citation_information",
  "Page": "integer_page_reference",
  "Context": "supporting_text_from_source",
  "RAG pipeline": "basic|multi-vector|graph-enhanced"
}
```

## File Formats

The dataset is provided in multiple formats:

- **`RAGCare-QA.xlsx`**: Primary dataset organized by complexity level (3 worksheets)


## Reference Sources

The dataset draws from diverse authoritative medical sources:

- **Medical Textbooks (63%)**: Primarily "Interna medicina" (6th edition, 2022) and "Harrison's Principles of Internal Medicine"
- **Peer-reviewed Journals (30%)**: Including Nature, The New England Journal of Medicine, Endocrine Reviews, Molecular and Cellular Biology
- **Other Medical Sources (7%)**: Specialized medical resources and databases

Publication years range from 1985 to 2024, ensuring both foundational knowledge and current research representation.

## RAG Architecture Classification

Questions are classified based on their optimal RAG pipeline requirements:

### Basic RAG
- **Characteristics**: Direct factual queries, explicit terminology, straightforward retrieval
- **Example**: Definition-based questions, simple medical facts
- **Use Case**: Standard document retrieval systems

### Multi-vector RAG
- **Characteristics**: Requires diverse knowledge sources, multiple perspectives
- **Example**: Questions integrating multiple medical concepts or treatment approaches
- **Use Case**: Systems needing comprehensive knowledge coverage

### Graph-enhanced RAG
- **Characteristics**: Complex medical relationships, hierarchical knowledge structures
- **Example**: Pathophysiological mechanism queries with interconnected pathways
- **Use Case**: Advanced reasoning requiring entity relationship modeling

## Usage Examples

### Loading the Dataset (Python)

```python
import pandas as pd
import json

# Load from Excel
basic_questions = pd.read_excel('RAGCare-QA.xlsx', sheet_name='basic questions')
intermediate_questions = pd.read_excel('RAGCare-QA.xlsx', sheet_name='intermediate questions')
advanced_questions = pd.read_excel('RAGCare-QA.xlsx', sheet_name='advanced questions')

```

## Applications

This dataset is designed for:

- **RAG System Evaluation**: Benchmark different retrieval architectures
- **Medical Education AI**: Develop adaptive learning systems
- **Knowledge Assessment**: Create intelligent tutoring systems
- **Research**: Study retrieval strategies for medical knowledge
- **Model Training**: Fine-tune medical language models


## Citation

If you use this dataset in your research, please cite:

```bibtex
in process
```

## Funding

This work was funded by the European Union under Horizon Europe (project ChatMED grant agreement ID: 101159214).

## Authors

- **Jovana Dobreva** (Corresponding Author) - Faculty of Computer Science and Engineering, Ss. Cyril and Methodius University
- **Ivana Karasmanakis** - Department of Intelligent Systemst, Jožef Stefan Institute
- **Filip Ivanišević** - Department of Intelligent Systems, Jožef Stefan Institute
- **Tadej Horvat** - Department of Intelligent Systems, Jožef Stefan Institute
- **Dimitar Kitanovski** - Faculty of Computer Science and Engineering, Ss. Cyril and Methodius University
- **Matjaž Gams** - Department of Intelligent Systems, Jožef Stefan Institute
- **Kostadin Mishev** - Faculty of Computer Science and Engineering, Ss. Cyril and Methodius University
- **Monika Simjanoska Misheva** - Faculty of Computer Science and Engineering, Ss. Cyril and Methodius University

## Contact

For questions or collaborations, please contact:
- Jovana Dobreva: jovana.dobreva@finki.ukim.mk


## Disclaimer

Views and opinions expressed are those of the authors only and do not necessarily reflect those of the European Union or the European Research Executive Agency. Neither the European Union nor the granting authority can be held responsible for them.