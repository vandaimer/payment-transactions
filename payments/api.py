from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from payments.views import Healthcheck, Restaurant
from payments.schemas import RestaurantSchema
from db import db_connection, async_session


router = APIRouter()


@router.get("/healthcheck")
def healthcheck():
    return Healthcheck.status()


@router.post("/restaurant", response_model=RestaurantSchema, status_code=201)
def restaurante(restaurant: RestaurantSchema, db: Session = Depends(async_session)):
    try:
        return Restaurant.create(restaurant, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Error to create a new restaurant.",
        )


@router.get("/transacao", response_model=RestaurantSchema)
def transacao():
    pass
