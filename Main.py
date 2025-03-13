import uvicorn
from fastapi import FastAPI

from endpoints import Achievement, Faculty, Notes, Students, Time_table, Event, Assignment
from Auth import router
app = FastAPI()

app.include_router(router)
app.include_router(Achievement.router)
app.include_router(Faculty.router)
app.include_router(Notes.router)
app.include_router(Students.router)
app.include_router(Time_table.router)
app.include_router(Event.router)
app.include_router(Assignment.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
