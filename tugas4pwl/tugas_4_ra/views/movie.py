from pyramid.view import view_config
from .. import models
from sqlalchemy.exc import SQLAlchemyError
import json
import traceback


@view_config(route_name="movie", renderer="json", request_method="GET")
def get_movie(request):
    try:
        results = request.dbsession.query(models.Movie).all()
        return {
            "status": "success",
            "data": [
                dict(
                    id=row.id,
                    title=row.title,
                    description=row.description,
                    year=row.year,
                    rating=row.rating,
                    genre=row.genre,
                )
                for row in results
            ],
        }
    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}
    except Exception as e:
        print(traceback.format_exc())
        request.response.status = 500
        return {"status": "error", "message": str(e)}


@view_config(route_name="movie_detail", renderer="json", request_method="GET")
def get_movie_detail(request):
    try:
        query = request.dbsession.query(models.Movie)
        result = query.filter(models.Movie.id == request.matchdict["id"]).first()

        if result is None:
            request.response.status = 404
            return {"status": "error", "message": "Not Found"}

        return {
            "status": "success",
            "data": {
                "id": result.id,
                "title": result.title,
                "description": result.description,
                "year": result.year,
                "rating": result.rating,
                "genre": result.genre,
            },
        }
    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}


@view_config(
    route_name="movie_create",
    renderer="json",
    request_method="POST",
    permission="admin",
)
def create_movie(request):
    try:
        movie = models.Movie(
            title=request.json_body["title"],
            year=request.json_body["year"],
            description=request.json_body["description"],
            genre=request.json_body["genre"],
            rating=request.json_body["rating"],
        )
        request.dbsession.add(movie)
        return {"status": "success", "data": request.json_body}
    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}
    except KeyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e) + " not found"}
    except Exception as e:
        request.response.status = 500
        return {"status": "error", "message": str(e)}


@view_config(
    route_name="movie_update", renderer="json", request_method="PUT", permission="admin"
)
def update_movie(request):
    try:
        query = request.dbsession.query(models.Movie)
        movie = query.filter(models.Movie.id == request.matchdict["id"]).first()

        if movie is None:
            request.response.status = 404
            return {"status": "error", "message": "Not Found"}

        movie.title = request.json_body["title"]
        movie.description = request.json_body["description"]
        movie.year = request.json_body["year"]
        movie.rating = request.json_body["rating"]
        movie.genre = request.json_body["genre"]
        return {"status": "success", "data": request.json_body}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e.orig)}
    except KeyError as e:
        return {"status": "error", "message": str(e) + " not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@view_config(
    route_name="movie_delete",
    renderer="json",
    request_method="DELETE",
    permission="admin",
)
def delete_movie(request):
    try:
        query = request.dbsession.query(models.Movie)
        movie = query.filter(models.Movie.id == request.matchdict["id"]).first()

        if movie is None:
            request.response.status = 404
            return {"status": "error", "message": "Not Found"}

        request.dbsession.delete(movie)
        return {"status": "success"}
    except SQLAlchemyError as e:
        print(traceback.format_exc())
        return {"status": "error", "message": str(e.orig)}
    except KeyError as e:
        print(traceback.format_exc())
        return {"status": "error", "message": str(e) + " not found"}
    except Exception as e:
        print(traceback.format_exc())
        return {"status": "error", "message": str(e)}
