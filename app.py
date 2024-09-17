from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        blog_posts = load_blog_posts()

        new_post = {
            'id': len(blog_posts) + 1,
            'title': title,
            'author': author,
            'content': content
        }

        blog_posts.append(new_post)

        save_blog_posts(blog_posts)

        # Redirect back to the index route
        return redirect(url_for('index'))

        # If it's a GET request, display the form
    return render_template('add.html')


def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
