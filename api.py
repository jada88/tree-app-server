from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from tree_db import TreeDb

app = Flask(__name__)
CORS(app, support_credentials=True)
tree_db = TreeDb()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return '<h1>You want path: %s to be /api/traverse, and the search: ?node=</h1> the parameter should be the folders number <br> <h2>Example: /api/traverse?node=1</h2>' % path

@app.route("/api/traverse")
@cross_origin(supports_credentials=True)

def traverse():
    x = request.args["node"]
    node = tree_db.get_subtree(int(x))
    if node is None:
      return jsonify()
    return jsonify(_generate_traverse_response(node))

def _generate_traverse_response(node):
    result = {"id" : node.id, "name" : node.name}
    childs =[]
    for child in node.childs:
        childs.append({"id": child.id, "name" : child.name})
    result["childs"] = childs
    return result

if __name__ == "__main__":
  app.run(host='0.0.0.0')
  # app.run(host='0.0.0.0', port=8000, debug=True)