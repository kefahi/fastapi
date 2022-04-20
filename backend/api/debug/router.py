""" Debug api module """

from utils.db import User
from utils.template import json_render
from fastapi import APIRouter

router = APIRouter()


@router.get('/mytemp')
async def mytemp():
    """ Jinja template example """
    return json_render(__file__, "mytemp.json.j2", {"name": "Alibaba", "age": 40})


@router.get('/sample')
async def sample():
    """ Sample """
    user = User()
    print(user)
    return {'users': ['a', 'b', 'c']}


# Simulate exception to check proper handling
# of exception and returning json response
@router.get('/mybad')
async def mybad():
    """Test path"""
    raise Exception("My bad!")
