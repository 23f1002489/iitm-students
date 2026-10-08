
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import csv
from pathlib import Path

app = FastAPI()

# Enable CORS for GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_FILE = Path(__file__).parent / "q-fastapi.csv"

# Load students while preserving CSV row order
students = []

with open(CSV_FILE, mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })


@app.get("/api")
def get_students(
    classes: Optional[List[str]] = Query(default=None, alias="class")
):
    # Return all students if no class filter is supplied
    if classes is None:
        return {"students": students}

    # Filter without changing the original CSV order
    filtered_students = [
        student
        for student in students
        if student["class"] in classes
    ]

    return {"students": filtered_students}
