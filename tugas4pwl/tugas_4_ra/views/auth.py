from pyramid.view import view_config
from .. import models
from sqlalchemy.exc import SQLAlchemyError
import json
import traceback


@view_config(route_name="register", renderer="json", request_method="POST")
def register(request):
    try:
        if request.json_body["name"] is None or request.json_body["name"] == "":
            request.response.status = 400
            return {"status": "error", "message": "Name is required"}

        if request.json_body["password"] is None or request.json_body["password"] == "":
            request.response.status = 400
            return {"status": "error", "message": "Password is required"}

        if request.json_body["email"] is None or request.json_body["email"] == "":
            request.response.status = 400
            return {"status": "error", "message": "Email is required"}

        user = models.User(
            name=request.json_body["name"],
            password=request.json_body["password"],
            email=request.json_body["email"],
            role="admin",
        )

        request.dbsession.add(user)

        return {"status": "success", "data": request.json_body}

    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}
    except Exception as e:
        print(traceback.format_exc())
        request.response.status = 500
        return {"status": "error", "message": str(e)}


@view_config(route_name="login", renderer="json", request_method="POST")
def login(request):
    try:
        if request.json_body["email"] is None or request.json_body["email"] == "":
            request.response.status = 400
            return {"status": "error", "message": "Email is required"}

        if request.json_body["password"] is None or request.json_body["password"] == "":
            request.response.status = 400
            return {"status": "error", "message": "Password is required"}

        query = request.dbsession.query(models.User)
        result = query.filter(models.User.email == request.json_body["email"]).first()

        if result is None:
            request.response.status = 404
            return {"status": "error", "message": "Not Found"}

        if result.password != request.json_body["password"]:
            request.response.status = 400
            return {"status": "error", "message": "Wrong password"}

        token = request.create_jwt_token(
            result.id,
            role=result.role,
        )

        return {
            "status": "success",
            "token": token,
            "data": {
                "id": result.id,
                "name": result.name,
                "email": result.email,
                "role": result.role,
            },
        }

    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}
    except Exception as e:
        print(traceback.format_exc())
        request.response.status = 500
        return {"status": "error", "message": str(e)}
