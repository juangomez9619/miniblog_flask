from flask import Flask, render_template

app = Flask(__name__)

posts = []


@app.route('/') #URL a la página principal
def index():
    return render_template("index.html", num_posts=len(posts))

@app.route('/p/<string:slug>/')
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)

'''Dos URL para la misma vista'''
@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>")
def post_form(post_id=None):
    return render_template("admin/post_form.html", post_id=post_id)

    