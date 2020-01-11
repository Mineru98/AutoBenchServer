import sys
from database import init_db
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

# mode = 0 # Production Mode
mode = 1 # Reset Mode

app = Flask(__name__)
app.debug = True

app.add_url_rule('/graphql/autobench', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
  init_db(mode)
  app.run(host='0.0.0.0', port=int(sys.argv[1]))
