""" Debug api module """

from fastapi import APIRouter
from utils.db import User
router = APIRouter()


@router.get('/sample')
def sample():
    """ Sample """
    user = User()
    print(user)
    return {'users': ['a', 'b', 'c']}


# Simulate exception to check proper handling
# of exception and returning json response
@router.get('/mybad')
def mybad():
    """Test path"""
    raise Exception("My bad!")
