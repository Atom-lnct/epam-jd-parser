from fastapi import FastAPI, UploadFile, HTTPException


try : 
    from .pdf_extractor import extract_text_from_pdf
    from .jd_parser import parse_jd_with_llm
    from .database import jd_collection

except ImportError : 
    from pdf_extractor import extract_text_from_pdf
    from jd_parser import parse_jd_with_llm
    from database import jd_collection


app = FastAPI(title="JD Parser API ")

@app.post("/parse-jd")
async def parse_jd(file : UploadFile):
    if(file.content_type != "application/pdf" and not (file.filename and file.filename.lower().endswith(".pdf"))) :
        raise HTTPException(status_code = 400 , detail = "Only PDF is allowed in the JD-Parser")
    
    file_bytes = await file.read()
    if not file_bytes : 
        raise HTTPException(status_code = 400 , detail = "Uploaded file is Empty ")
    
    try :
        text = extract_text_from_pdf(file_bytes)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e : 
        raise HTTPException(status_code = 400 , detail = str(e)) # unable to open , any failure
    except Exception as e :
        raise HTTPException(status_code = 500 , detail = f"pdf extraction error : {str(e)}")
    
    if not text:
        raise HTTPException(status_code = 400 , detail = "The Pdf contains no readable content")
    
    try : 
        parsed = parse_jd_with_llm(text)
    except Exception as e:
        raise HTTPException(status_code = 500 , detail = f"LLM failer {str(e)}")
    
    jd_dict = parsed.model_dump()

    db_error = None
    try : 
        jd_collection.insert_one(jd_dict.copy()) # PyMOngo automatically add the id to the data to avoid it we insert the copy of it 
    except Exception as e:
        db_error = str(e)

    jd_dict.pop("_id",None) # to remove id that mongo have generated 

    return {"data" : jd_dict , "db_error" : db_error}


   