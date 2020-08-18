from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from payments.views import Healthcheck, Restaurant, Transaction
from payments.schemas import RestaurantSchema, ListOfTransactionSchema

from db import db_connection, async_session


router = APIRouter()


@router.get("/healthcheck")
def healthcheck():
    return Healthcheck.status()


@router.post("/restaurant", response_model=RestaurantSchema, status_code=201, tags=["Restaurant"])
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


@router.get("/transacoes/estabelecimento", response_model=ListOfTransactionSchema, tags=["Transaction"])
def transacoes(cnpj: int, db: Session = Depends(async_session)):
    try:
        return Transaction.all(cnpj, db)
    except NoResultFound as e:
        raise HTTPException(
            status_code=400,
            detail=f"Restaurant not found with cnpj: {cnpj}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error to retrieve transactions with cnpj: {cnpj}",
        )
