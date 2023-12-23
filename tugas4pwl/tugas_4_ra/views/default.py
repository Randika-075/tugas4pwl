from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from .. import models


@view_config(route_name="home", renderer="json")
def my_view(request):
    return {"project": "tugas 4"}
