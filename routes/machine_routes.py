# import pymongo
from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse

transaction = APIRouter(tags=["Machine"])


# @transaction.get("/machine", description="this is the machine list view.")
# def getTransactionAPIVIew(request: Request):
#     payload={
#         "data": "Hello"
#     }
#     return JSONResponse(
#             content=payload,
#             status_code=status.HTTP_200_OK
#     )

@transaction.get("/machine", description="this is the machine list view.")
def getTransactionAPIVIew(request: Request):
    try:
        db = request.app.database
        collection = db['transactions']
        
        # change_stream = collection.changestream.collection.watch()
        # for change in change_stream:
        #     print("CHANGE: ",change)
        #     print('') # for readability only

       
      
        
        payload = {
            "ok": True,
            "message": "Machines List",
            "status": status.HTTP_200_OK,
            "data": [],
        }
        return JSONResponse(
            content=payload,
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        payload = {
            "ok": False,
            "message": f"Error Occurred {e}",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "data": [],
        }
        response = JSONResponse(
            content=payload,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return response