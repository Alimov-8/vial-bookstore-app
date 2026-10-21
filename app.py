from vial.app import Vial
from whitenoise import WhiteNoise

from auth import STATIC_TOKEN, login_required, TokenMiddleware, on_exception
from storage import BookStorage


app = Vial()
app.add_middleware(TokenMiddleware)
app.add_exception_handler(on_exception)
book_storage = BookStorage()
book_storage.create(name="System Design Interview", author="Alex Xu")


@app.route("/", allowed_methods=["get"])
def index(request, response):
    books = book_storage.all()
    response.html = app.template("index.html", context={"books": books})


@app.route("/login", allowed_methods=["post"])
def login(request, response):
    response.json = {"token": STATIC_TOKEN}


@app.route("/books", allowed_methods=["post"])
@login_required
def create(request, response):
    book = book_storage.create(**request.POST)
    response.status_code = 201
    response.json = book._asdict()


@app.route("/books/{id:d}", allowed_methods=["delete"])
@login_required
def delete(request, response, id):
    book_storage.delete(id)
    response.status_code = 204
