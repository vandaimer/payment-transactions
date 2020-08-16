import time

from fastapi import FastAPI, APIRouter

from payments.api import router as payments_api


app = FastAPI()
router = APIRouter()

@router.get("/{path:path}", status_code=404)
def not_implement(path):
    return {
        'path': f"/{path}",
        'status': 'notImplemented',
        'now':  time.time(),
    }

app.include_router(payments_api, prefix="/api/v1")
app.include_router(router)
