from flask import Flask, request, render_template, redirect, url_for
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    """
    Display the list of all blog posts.

    Returns:
        str: The rendered HTML template for the index page.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post.

    Returns: str: The rendered HTML template for the add form or a
    redirect URL.
    """
    if request.method == 'POST':
        blog_posts = load_blog_posts()
        new_post = {
            'id': str(uuid.uuid4()),
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'content': request.form.get('content'),
            'likes': 0
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):
    """
    Delete a blog post by its ID.

    Args:
        post_id (str): The ID of the blog post to be deleted.

    Returns:
        str: A redirect URL to the index page.
    """
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if
                  post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update an existing blog post.

    Args:
        post_id (str): The ID of the blog post to be updated.

    Returns: str: The rendered HTML template for the update form
    or a redirect URL. tuple: A tuple containing an error message
    and HTTP status code if the post is not found.
    """
    blog_posts = load_blog_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


@app.route('/like/<post_id>', methods=['POST'])
def like(post_id):
    """
    Increment the 'likes' of a specific blog post.

    Args:
        post_id (str): The ID of the blog post to be liked.

    Returns:
        str: Redirects to the index page.
    """
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/comment/<post_id>', methods=['POST'])
def comment(post_id):
    """
    Add a comment to a specific blog post.

    Args:
        post_id (str): The ID of the blog post to be commented on.

    Returns:
        str: Redirects to the index page.
    """
    blog_posts = load_blog_posts()
    comment_text = request.form.get('comment')
    for post in blog_posts:
        if post['id'] == post_id:
            if 'comments' not in post:
                post['comments'] = []
            post['comments'].append(comment_text)
            break
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
