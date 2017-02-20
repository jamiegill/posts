import os
from posts import app
from posts.database import *
from posts.models import Post
from posts.database import Base, engine, session

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
def seed():
    post = Post(
        title="ksldfj",
        body="test2-2"
    )
    session.add(post)
    session.commit()

def delete_post():
 #   post = Post(
 #       title="title",
 #       body="body"
  #  )
    session.query(Post.id).filter(Post.id == 2).delete()
    session.commit()

if __name__ == '__main__':
    run()

