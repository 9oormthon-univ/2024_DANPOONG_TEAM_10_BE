from flask import Flask
from flask_graphql import GraphQLView
from config import app, db
from schema import schema

@app.route('/')
def hello():
    return "Hello, World!"

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)