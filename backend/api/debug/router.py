""" Debug api module """

from utils.db import User
from utils.template import json_render
from fastapi import APIRouter
from .geoip import get_freegeoip
from .ext_api import get_users, create_user, PostUser

router = APIRouter()

@router.get('/geoip')
async def get_geoip():
    """ Query external api example """
    return get_freegeoip() 



@router.post('/users')
async def serve_create_user(postuser: PostUser):
    return create_user(postuser);

@router.get('/users')
async def serve_get_users(limit: int):
    return get_users(limit)

@router.get('/mytemp')
async def mytemp():
    """ Jinja template example """
    return json_render(__file__, "mytemp.json.j2", {"name": "Alibaba", "age": 40})


@router.get('/sample')
async def sample():
    """ Sample """
    # user = User()
    # print(user)
    return {'users': ['a', 'b', 'c']}


# Simulate exception to check proper handling
# of exception and returning json response
@router.get('/mybad')
async def mybad():
    """Test path"""
    raise Exception("My bad!")
