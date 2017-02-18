import os
from posts import app
from 
from posts.models import *

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
def seed():
    post = Post(
        title="t",
        body="testbody"
    )
    session.add(post)
    session.commit()

if __name__ == '__main__':
    run()

