import os
import io
from PIL import Image
import shutil#
import pymupdf
import pytesseract

def check_and_configure_tessaract() -> str : # check whether tesserat is present 
    cmd = pytesseract.pytesseract.tesseract_cmd
    if cmd and shutil.which(cmd) :
        return cmd
    
    which_cmd = shutil.which("tesseract")

    if which_cmd :
        pytesseract.pytesseract.tesseract_cmd = which_cmd
        return which_cmd
    
    for candidate in [
    "/opt/homebrew/bin/tesseract",
    "/usr/local/bin/tesseract",
    "/usr/bin/tesseract",
     ]:
        
        if os.path.isfile(candidate) and os.access(candidate , os.X.ok): # check whether it has permission to execute it 
            pytesseract.pytesseract.tesseract_cmd = candidate # configure its finded path
            return candidate
        return ""
    
def is_meaningfull_text( # func will receive the txt
            text : str,
            min_words : int = 5,
            min_chars : int = 15,
            
    ) -> bool : 
        
        cleaned = text.strip() # to remove the whitespace(" aayush ") => ("aayush") space 
        if len(cleaned) < min_chars :
            return False
        
        words = [w for w in cleaned.split() if any(c.isalnum() for c in w)]
        return len(words) >= min_words

def extract_text_from_pdf(file_bytes : bytes) -> str : 
     
     try :
          doc = pymupdf.open(stream=file_bytes , filetype = "pdf")
     except Exception as e :
          raise ValueError(f"Unable to open pdf document : {str(e)}")
     
     if doc.page_count == 0:
          doc.close()
          raise ValueError("The uploaded pdf have no pages")
     
     tesseract_available: bool | None = None
     page_texts: list[str] = []

     try :
          for page_idx in range (doc.page_count) :  # Iterate the all the n pages 
               page = doc[page_idx] # get the first page of the JD

               text = page.get_text("text").strip() #pymupdf extract the text

               if is_meaningfull_text(text) : 
                    page_texts.append(text)
                    continue
               
               # if not then its an OCR 
               if tesseract_available is None:                  # This check whether it is available or not
                 tesseract_path = check_and_configure_tesseract()
                 tesseract_available = bool(tesseract_path)

               if not tesseract_available :
                    raise RuntimeError(
                         "Tesseract OCR engine is missing or not installed. "
                          "Please install Tesseract (e.g. 'brew install tesseract') to process scanned PDFs."
                    )
               
               try:
                   # 300 DPI resolution (72 standard PDF points * 4.166667 ≈ 300 DPI)
                     zoom = 300.0 / 72.0
                     mat = pymupdf.Matrix(zoom, zoom)
                     pix = page.get_pixmap(matrix=mat)
                     img = Image.open(io.BytesIO(pix.tobytes("png")))
               except Exception as e:
                     raise ValueError(
                       f"Failed to render page {page_idx + 1} for OCR extraction: {str(e)}"
                )


               try : 
                    ocr_text = pytesseract.image_to_string(img , lang="eng").strip()
               except pytesseract.TesseractNotFoundError : 
                    raise RuntimeError(
                         " Tesseract is not installed"
                    )
               except Exception as e:
                    raise ValueError(f"OCR extarction fails on the page {page_idx+1} : {str(e)}")
               
               if is_meaningfull_text(ocr_text): # to check whether its not empty 
                    page_texts.append(ocr_text)

     finally :
            doc.close()

     combined_text = "\n\n".join(page_texts).strip()

     if not combined_text : 
          raise ValueError(
               " Failed to extract both the ocr and the pymupdf"
          )
     return combined_text








