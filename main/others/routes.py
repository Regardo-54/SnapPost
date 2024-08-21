from flask import render_template, request, Blueprint
from main.models import Post

others = Blueprint('others', __name__)

@others.route('/')
def home():
    page_num = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page_num, per_page=5)
    return render_template('home.html', posts=posts, title="Home")

@others.route('/about')
def about():
    return render_template('about.html')