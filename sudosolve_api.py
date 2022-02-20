from PIL import Image
from flask import Flask, request, Response, jsonify, render_template
from flask_restful import Resource, Api
from numpy import asarray

from base_64_handling.B64Utils import b64ToImage
from my_sudoku_solver.Sudoku import Sudoku
from my_sudoku_solver.utils import flatten
from sudoku_identification.sudoku_image_processing import analyze_image

AUTH_KEY = 'e41a8de0-714d-4aad-8b74-2f722cdc93b6'
app = Flask(__name__)
api = Api(app)


class SudokuSolverResource(Resource):
    def post(self):
        try:
            auth = request.headers.get('Auth')
        except LookupError:
            return Response('Authentication needed.\n', status=401)

        if auth != AUTH_KEY:
            return Response('Authentication didn\'t succeed.\n', status=401)

        try:
            req_data = request.get_json()
            board = req_data.get("board")
        except LookupError:
            return Response('The request is invalid.\n', status=400)

        try:
            puzzle = Sudoku(board)
            solved = puzzle.backtracking_search()
        except ValueError:
            return Response('Could not build a Sudoku grid.\n', status=400)

        if not solved:
            return Response('Could not solve the Sudoku.\n', status=400)

        return jsonify({"solved": puzzle.assignment_to_str()})


class SudokuIdentifierResource(Resource):
    def post(self):
        try:
            auth = request.headers.get('Auth')
        except LookupError:
            return Response('Authentication needed.\n', status=401)

        if auth != AUTH_KEY:
            return Response('Authentication didn\'t succeed.\n', status=401)

        try:
            req_data = request.get_json()
            encoded: str = req_data.get('image').get('data')
        except LookupError:
            return Response('The request is invalid.\n', status=400)

        try:
            decoded: Image = asarray(b64ToImage(encoded=encoded))
            rows = analyze_image(image=decoded, debug=False)
            board = ''.join(map(str, flatten(rows)))
        except Exception as e:
            return Response(str(e), status=400)

        return jsonify({"board": board})


@app.route('/', methods=['GET'])
def helpPage():
    return render_template('help.html')


api.add_resource(SudokuSolverResource, '/solve')
api.add_resource(SudokuIdentifierResource, '/identify')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
