import uvicorn
from fastapi import FastAPI

from endpoints import achieve_endpoints, faculty_endpoint, Notes_endpoints, stu_endpoints, TT_endpoints, event, work
from auth import router
app = FastAPI()

app.include_router(router)
app.include_router(achieve_endpoints.router)
app.include_router(faculty_endpoint.router)
app.include_router(Notes_endpoints.router)
app.include_router(stu_endpoints.router)
app.include_router(TT_endpoints.router)
app.include_router(event.router)
app.include_router(work.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
