from configuration.config import *

@router.post("/example_router", summary="Example Router",tags=["Example"])
async def get_All_Blog():
    return  "Welcome to the Fast api"