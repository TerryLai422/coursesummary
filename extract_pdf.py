import warnings
from langchain_community.document_loaders import TextLoader, UnstructuredWordDocumentLoader
from langchain_community.document_loaders import PyPDFLoader
import os

# Suppress specific warnings from transformers library
warnings.filterwarnings("ignore", category=FutureWarning, module="torch.nn.modules.module")
# === Document Extraction and Chunking ===

def extract(file_path):
    """
    Extracts and splits text from a file (PDF, TXT, DOCX) into manageable chunks for summarization.
    Also extracts code blocks and image/graph references for inclusion in summary metadata.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text_content = " ".join([p.page_content for p in pages])
    elif ext == ".txt":
        loader = TextLoader(file_path, autodetect_encoding=True)
        pages = loader.load()
        text_content = " ".join([p.page_content for p in pages])
    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(file_path)
        pages = loader.load()
        text_content = " ".join([p.page_content for p in pages])
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported types: .pdf, .txt, .docx")

    return text_content


# Prompt user for document to summarize
file_path = "/Users/admin/ws-2024/coursesummarizer/documents/COMP2401_Ch1_SystemsProgramming.pdf" 

# Step 1: Get "COMP2401_Ch1_SystemsProgramming.pdf"
base_name = os.path.basename(file_path)

# Step 2: Split into ("COMP2401_Ch1_SystemsProgramming", ".pdf") and take [0]
file_name_without_ext = os.path.splitext(base_name)[0]

print(file_name_without_ext)
# Output: COMP2401_Ch1_SystemsProgramming

try:
    texts = extract(file_path)
    # Save text to file
    with open(file_name_without_ext + ".txt", "w", encoding="utf-8") as f:
        f.write(texts)
    print("PDF text saved to " + file_name_without_ext + ".txt")
except Exception as e:
    print(f"[ERROR]: {e}")
