from flask import Flask, request, render_template, redirect, url_for
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    """
    Display the list of all blog posts.

    This route handles GET requests to the root URL. It loads all
    blog posts from the JSON file and renders the index.html
    template with these posts.

    Returns:
        str: The rendered HTML template for the index page.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post.

    Handles both GET and POST requests. For GET requests,
    it renders the add.html form for creating a new blog post. For
    POST requests, it processes the form data, creates a new blog
    post, saves it to the JSON file, and redirects to the index page.

    Returns: str: The rendered HTML template for the add form or a
    redirect URL.
    """
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
    """
    Delete a blog post by its ID.

    Handles DELETE requests to remove a specific blog post
    identified by post_id. After deletion, it updates the JSON
    file and redirects to the index page.

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

    Handles both GET and POST requests. For GET requests, it loads
    the specific blog post by its ID and renders the update.html
    template pre-filled with the post's current details. For POST
    requests, it updates the blog post with the new data provided
    in the form, saves the changes to the JSON file, and redirects
    to the index page.

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


def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
