from pydantic import BaseModel
from typing import Optional

class Company(BaseModel) :             # Company Info 
    name : Optional[str] = None
    email : Optional[str] = None
    website : Optional[str] = None
    location : Optional[str] = None
    job_role : Optional[str] = None
    job_description : Optional[str] = None
    job_type : Optional[str] = None

class EligibilityCriteria(BaseModel) :  # criteria 
    minimum_cgpa : Optional[float] = None
    required_degree : Optional[list[str]] = None
    required_branches : Optional[list[str]] = None
    eligibility_graduation_year : Optional[list[int]] = None
    minimum_class_10_percentage : Optional[float] = None
    minimum_class_12_percantage : Optional[float] = None

class ParsedJD(BaseModel):           # in this order we need our Data 
    company: Company
    eligibility_criteria: EligibilityCriteria
    skills: Optional[list[str]] = None