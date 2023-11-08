from configuration.config import *
from api.example.example_router import *
import uvicorn

router.mount('/api/v1', router )

if __name__ == '__main__':
    uvicorn.run("main:router", host="localhost",port=5001, reload=True)