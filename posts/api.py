import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session
from sqlalchemy import and_

@app.route("/api/posts", methods=['GET'])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """
    # Get the querystring arguments
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")
    
    # Get and filter the posts from the database
    posts = session.query(models.Post)
    if title_like and body_like:
        posts = posts.filter(and_(models.Post.body.contains(body_like),
                                  models.Post.title.contains(title_like)))
    elif body_like:
        posts = posts.filter(models.Post.body.contains(body_like))
    elif title_like:
        posts = posts.filter(models.Post.title.contains(title_like))
    posts = posts.order_by(models.Post.id)
    
    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts/<int:id>", methods=["GET"])
def post_get(id):
    """ Single post endpoint """
    # Get the post from the database
    post = session.query(models.Post).get(id)
    
    # Check whether the post exists
    # If not return a 404 with a helful message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
        
    # Return the post as json
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts/<int:id>", methods=["DELETE"])
def post_delete(id):
    """ Single post endpoint """
    # Get the post from the database
    post = session.query(models.Post).get(id)
    
    # Check whether the post exists
    # If not return a 404 with a helful message
    if not post:
        message = "Could not find post with id {} so cannot DELETE post".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
        
    session.query(models.Post.id).filter(models.Post.id == id).delete()
    session.commit()
    message = "successfully DELETED post {}".format(id)
    data = json.dumps({"mesage": message})
    return Response(data, 200, mimetype="application/json")