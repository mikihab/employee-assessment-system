from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import department, institution, admin, exam, question, answer, auth, user
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#CORS
origins = ["*"] #list of urls allowed that can communicate with the api. Put ["*"] to allow everyone
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #specific methods allowed (like get, put...)
    allow_headers=["*"], #specific headers allowed
)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(institution.router)
app.include_router(department.router)
app.include_router(user.router)
app.include_router(exam.router)
app.include_router(question.router)
app.include_router(answer.router)

@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to EAS API"}