import os
from openai import OpenAI # To communicate with the open ai server 

try : 
    from .jd_schema import ParsedJD
    from .jd_prompt import SYSTEM_PROMPT

except ImportError:
    from jd_schema import ParsedJD
    from jd_prompt import SYSTEM_PROMPT

from dotenv import load_dotenv # Help to load env variable 

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def parse_jd_with_llm(text: str) -> ParsedJD:
    if not OPENAI_API_KEY:
        raise ValueError("Open AI Environment is yet to set .")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages = [
            {"role" : "system" , "content" : SYSTEM_PROMPT},
            {"role" : "user" , "content": f"Parse the following Job Description:\n\n{text}"},
        ],
        response_format = ParsedJD,
        n=1
    )

    return completion.choices[0].message.parsed

      

