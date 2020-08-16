from fastapi import APIRouter

from payments.views import Healthcheck

router = APIRouter()


@router.get("/healthcheck")
def healthcheck():
    return Healthcheck.status()

@router.get("/transacao")
def transacao():
    pass
