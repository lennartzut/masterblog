from flask import Flask, request, render_template, redirect, url_for
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_blog_posts()
        new_post = {
            'id': str(uuid.uuid4()),
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'content': request.form.get('content')
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if
                  post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        # Update the post details from the form data
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
