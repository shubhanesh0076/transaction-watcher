import os, logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from routes.machine_routes import transaction
from routes.watch_router import watcher_router, watch_insertions
from config.mongodb_starter import startup_db_client, shutdown_db_client


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transaction, prefix="/api/v1")
app.include_router(watcher_router, prefix="/api/v1")


@app.on_event("startup")
async  def startup_app():
    startup_db_client(app)
    
    background_tasks = BackgroundTasks()
    background_tasks.add_task(watch_insertions)
    await  background_tasks()



@app.on_event("shutdown")
async def shutdown_app():
    await shutdown_db_client(app)
