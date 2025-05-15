from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks

from sqlalchemy.orm import Session
from db.db_pg import engine as pg_engine, get_db as pg_get_db
from normalizer import Normalizer

from config import QUEUE_HOST, QUEUE_PORT, QUEUE_NAME
from consumer_rabbitmq import RabbitMQConsumer

from config import SOCKET_HOST, SOCKET_PORT
from consumer_socket import SocketDataClient

from config import TRANSPORT

from models.base import Base as TargetBase
from models import tables_list as target_tables_list

from app_state import AppState

import threading

def init_target_db():
    TargetBase.metadata.drop_all(pg_engine) 
    TargetBase.metadata.create_all(bind=pg_engine, tables=target_tables_list)

app = FastAPI()

app_state = AppState()

@app.on_event("startup")
def on_startup():
    init_target_db()

@app.post("/start_consumer")
def start_consumer(postgres_session: Session = Depends(pg_get_db)):
    if app_state.consumer_thread and app_state.consumer_thread.is_alive():
        raise HTTPException(status_code=400, detail="Consumer already running")

    normalizer = Normalizer(postgres_session)
    
    if TRANSPORT == 'rabbitmq':
        app_state.consumer = RabbitMQConsumer(
            rabbitmq_host=QUEUE_HOST,
            rabbitmq_port=QUEUE_PORT,
            rabbitmq_queue=QUEUE_NAME,
            normalizer=normalizer
        )
    elif TRANSPORT == 'socket':
        app_state.consumer = SocketDataClient(
            host=SOCKET_HOST,
            port=SOCKET_PORT, 
            normalizer=normalizer
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid data source specified")
    
    app_state.consumer_thread = threading.Thread(
        target=app_state.consumer.start_consuming,
        daemon=True
    )
    app_state.consumer_thread.start()
    
    return {"status": "consumer started"}

@app.post("/stop_consumer")
def stop_consumer():
    if not app_state.consumer or not app_state.consumer_thread.is_alive():
        raise HTTPException(status_code=400, detail="Consumer not running")
    
    app_state.consumer.stop()
    app_state.consumer_thread.join(timeout=5)
    
    return {"status": "consumer stopped"}

@app.get("/consumer_status")
def consumer_status():
    return {
        "is_running": app_state.consumer_thread.is_alive() if app_state.consumer_thread else False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)