from elasticHelper import ESCrud
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

elasticHelper = ESCrud()

class Student(BaseModel):
    name: str
    age: int
    major: str
    enrollment_date: str

class UpdateStudent(BaseModel):
    name: str = None
    age: int = None
    major: str = None
    enrollment_date: str = None

@app.post("/students/")
def create_student(student: Student):
    response = elasticHelper.insert_document('students', student.dict())
    return {"id": response['_id'], "result": "Student created successfully"}

@app.get("/students/{student_id}")
def read_student(student_id: str):
    try:
        student = elasticHelper.get_document('students', student_id)
        return {"student": student['_source']}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Student not found")
@app.put("/students/{student_id}")
def update_student(student_id: str, student: UpdateStudent):
    try:
        elasticHelper.update_document('students', student_id, student.dict(exclude_none=True))
        return {"result": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    try:
        elasticHelper   .delete_document('students', student_id)
        return {"result": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Student not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

