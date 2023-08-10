import logging, pymongo, time

from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse
from config.mongodb_starter import get_database

watcher_router = APIRouter()


def watch_insertions():
    database = get_database()
    collection = database["transactions"]
    transaction_monitoring = database["transaction_monitoring"]

    try:
        resume_token = None
        pipeline = [
            {"$match": {"operationType": "insert", "fullDocument.transaction_count": {"$gt": 65}}}, # Add the condition here
        ]
        
        with collection.watch(pipeline) as stream:
            for insert_change in stream:
                inserted_document = insert_change["fullDocument"] # Check the transaction_count condition
                transaction_count = inserted_document.get("transaction_count")
                if transaction_count is not None and transaction_count > 65:
                    transaction_monitoring.insert_one(inserted_document) # Insert matched document into the "transaction_monitoring" collection

                resume_token = stream.resume_token # Optionally, you can also check for resume_token and recreate the stream
                
    except pymongo.errors.PyMongoError:
        # The ChangeStream encountered an unrecoverable error or the
        # resume attempt failed to recreate the cursor.
        if resume_token is None:
            # There is no usable resume token because there was a
            # failure during ChangeStream initialization.
            logging.error("Failure during ChangeStream initialization.")
        else:
            # Use the interrupted ChangeStream's resume token to create
            # a new ChangeStream. The new stream will continue from the
            # last seen insert change without missing any events.
            with collection.watch(pipeline, resume_after=resume_token) as stream:
                for insert_change in stream:
                    inserted_document = insert_change["fullDocument"] # Check the transaction_count condition
                    transaction_count = inserted_document.get("transaction_count")
                    if transaction_count is not None and transaction_count > 65:
                        transaction_monitoring.insert_one(inserted_document) # Insert matched document into the "transaction_monitoring" collection
