# views.py

from flask import render_template
from app import app
from flask import abort
from flask import request
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date

spec = APISpec( 
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)
books = [
    {
        'id': 1,
        'title': 'La hojarasca',
        'description': 'Good one',
        'author': 'Gabo'
    },
    {
        'id': 2,
        'title': 'El coronel no tiene quien le escriba',
        'description': 'Interesting',
        'author': 'Gabo'
    }
]
@app.route('/api/swagger.json')
def create_swagger_spec():
        return jsonify(spec.to_dict())

class GetResponseSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        body = fields.Str()
        author = fields.Str()
        
class PostResponseSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        body = fields.Str()
        author = fields.Str()
    
class PutResponseSchema(Schema):
        title = fields.Str()
        body = fields.Str()
        author = fields.Str()
class DeleteResponseSchema(Schema):
        id = fields.Int()

class GetListResponseSchema(Schema):
        Get_list = fields.List(fields.Nested(GetResponseSchema))
class PostListResponseSchema(Schema):
        Post_list = fields.List(fields.Nested(PostResponseSchema))
class PutListResponseSchema(Schema):
        Put_list = fields.List(fields.Nested(PutResponseSchema))
class DeleteListResponseSchema(Schema):
        Delete_list = fields.List(fields.Nested(DeleteResponseSchema))

@app.route('/books', methods=['GET'])
def get_books():
 """Get List of books
        ---
        get:
            description: Get List of books
            responses:
                200:
                    description: Return an book list
                    content:
                        application/json:
                            schema: GetListResponseSchema
    """
 return jsonify({'Get_list':books})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
 """Get a book
        ---
        get:
            description: Get a book
            responses:
                200:
                    description: Return an book 
                    content:
                        application/json:
                            schema: GetListResponseSchema
 """
 book = [book for book in books if book['id'] == book_id]
 if len(book) == 0:
       abort(404)
 return jsonify({'Get_list':book[0]})
# Add new book
# For testing: curl -i -H "Content-Type: application/json" -X POST -d '{"title":"El libro"}' http://localhost:5000/books
@app.route('/bookss', methods=['POST'])
def create_book():
    """Post a book
        ---
        get:
            description: Post a book
            responses:
                200:
                    description: Create a book
                    content:
                        application/json:
                            schema: PostListResponseSchema
     """
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'author': request.json.get('author', ""),
    }
    books.append(book)
    return jsonify({'Post_list': book})
@app.route('/bookss/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Ubdate a book
        ---
        get:
            description: Update a book
            responses:
                200:
                    description: Update a book
                    content:
                        application/json:
                            schema: PutListResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0 or not request.json:
        abort(404)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['description'] = request.json.get('description', book[0]['description'])
    book[0]['author'] = request.json.get('author', book[0]['author'])
    return jsonify({'Put_list': book[0]})

# Delete a Book
# For testing: curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/books/1
@app.route('/booksss/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book
        ---
        get:
            description: Delete a book
            responses:
                200:
                    description: Delete a book
                    content:
                        application/json:
                            schema: DeleteListResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'Delete_list': True})

with app.test_request_context():
    spec.path(view=get_books)
    spec.path(view=get_book)
    spec.path(view=create_book)
    spec.path(view=update_book)
    spec.path(view=delete_book)
    

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html',base_url='/docs')
    else:
     return send_from_directory('static',path)
