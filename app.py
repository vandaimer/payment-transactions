import time

from fastapi import FastAPI, APIRouter

from payments.api import router as payments_api


def start(db):
    app = FastAPI()
    router = APIRouter()
    db.create_tables()

    @router.get("/{path:path}", status_code=501)
    def not_implement(path):
        return {
            'path': f"/{path}",
            'status': 'notImplemented',
            'now':  time.time(),
        }

    app.include_router(payments_api, prefix="/api/v1")
    app.include_router(router)

    return app
