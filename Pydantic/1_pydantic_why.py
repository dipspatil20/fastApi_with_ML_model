from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='name of patient', description='give name', examples=['Amish','nitish'])]
    # name: str = Field(max_length=50)
    age: int = Field(gt=0, lt=120)
    #weight: float = Field(gt=0)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: bool
    email: EmailStr
    linkedin_url: AnyUrl
    #allergies: Optional[List[str]] = None #List[str]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

patient_info = {'name':'nitish', 'age': 30, 'weight':75.2, 'married':True, 'allergies':['pollen', 'dust'], 'contact_details':{'email':'abc@gmail.com', 'phone':'788897546545'}}


def inster_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Updated")

patient1 = Patient(**patient_info)

inster_patient_data(patient1)
update_patient_data(patient1)