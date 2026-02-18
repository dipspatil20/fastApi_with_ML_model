from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patients')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of patient')]
    gender: Annotated[Literal['male','female','others'], Field(..., description="Gender of patient")]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of patients in kgs')]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi< 30:
            return 'Normal'
        else:
            return 'Obese'



def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {'message':'Patient Managment System API'}

@app.get("/about")
def about():
    return {'message':'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    #load all data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort on the basis of weight, height or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid fields selected from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0),reverse=sort_order)

    return sorted_data

#Post endpoint

@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')

    #if not then new patient add to the db  data=dictionary, patient=pydantic object so first convert object to dictionary
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into json file
    save_data(data)

    #return Response
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

#to run this file use this command
# ---- uvicorn main:app --reload
