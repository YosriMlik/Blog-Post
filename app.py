'''
    flask installation: pip install flask
    SQLAlchemy installation: pip install flask-sqlalchemy

    creating the DataBase:
        - run python environnement
        - open the app file
        - tap:
            #>>> from app import db(our DataBase object)
            #>>> db.create_all() [ creating the db file if not exists ]
'''
from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# chemin mta3 sqlite file we use [sqlite:///"filename"] ki yabda sqlite file wel app.py file fi nafs el path OR [ sqlite://// _ ../filepath ] ki yaba sqlite file fi absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='Unknown')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # method tsirelha execution when creating successfully the BlogPost table
    def __repr__(self):
        return 'Blog Post: '+str(self.id)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posting():
    posts = BlogPost.query.order_by(BlogPost.date_posted).all() 
    return render_template('posts.html', posts=posts)


@app.route('/posts/delete/post<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/post<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)   
    if request.method == 'POST':
        if request.form['content'] != "" and request.form['title'] != "":
            post.content = request.form['content']
            post.title = request.form['title']
            db.session.commit()
            return redirect('/posts')
        else:
            return render_template('edit.html',post=post, verif="nothing") 
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if request.form['content'] != "" and request.form['title'] != "":
            # ken saret submit (method='post'=updating the DataBase) 3al <form> elli fi '/posts' page we collect data from that </form> & add to the DataBase [WRITING]
            post_title = request.form['title']
            post_content = request.form['content']
            post_author = request.form['author']
            new_post = BlogPost(title=post_title, content=post_content, author=post_author)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts')
        else:
            return render_template('new_post.html', verif="nothing")
    # else just [READING]
    else:
        return render_template('new_post.html')

if __name__ == '__main__':
    app.run()
