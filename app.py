from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from models import Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'urmom'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app=app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)

@app.route('/makepost', methods=['POST'])
def makepost():
    data = request.json
    post = Post(text=data['text'])
    db.session.add(post)
    db.session.commit()
    return data

@app.route('/makecomment', methods=['POST'])
def makecomment():
    data = request.json
    comment = Comment(text=data['text'], post_id=data['post_id'])
    post_exists = db.session.query(Post.id).filter_by(id=data['post_id']).first() is not None
    if post_exists:
        db.session.add(comment)
        db.session.commit()
        return data
    else:
        return 'post doesnt exist'

@app.route('/showposts', methods=['GET'])
def showposts():
    posts = Post.query.all()
    comments = Comment.query.all()
    output = []

    for post in posts:
        output_comments = []
        #print(post.id)
        for comment in comments:
            if comment.post_id == post.id:
                #print(comment.post_id, post.id, comment.text)
                output_comments.append({
                    'id': comment.id,
                    'text': comment.text
                    }
                )
            #else:
                #print('no')
        #print('cycle end')

        output.append({
            'id': post.id,
            'text': post.text,
            'comments': output_comments
        })
    return output

@app.route('/post', methods=['GET'])
def post():
    id = request.args.get('id')
    comments = Comment.query.all()
    post_exists = db.session.query(Post.id).filter_by(id=id).first() is not None
    if post_exists:
        post = db.session.query(Post).filter_by(id=id).first()
        output_comments = []
        for comment in comments:
            if comment.post_id == post.id:
                output_comments.append({
                    'id': comment.id,
                    'text': comment.text
                }
                )
        return {
            'comments': output_comments,
            'id': post.id,
            'text': post.text

        }
    else:
        return 'post doesnt exist'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()


#test