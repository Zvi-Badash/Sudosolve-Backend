import os

from PIL import Image
from flask import Flask, request, Response, jsonify, render_template
from flask_restful import Resource, Api
from numpy import asarray

from base_64_handling.B64Utils import b64ToImage
from sudoku_identification.sudoku_image_processing import analyze_image
from sudoku_logic.generating.DifficultyLevel import DifficultyLevel
from sudoku_logic.generating.generate_sudokus import get_sudoku
from sudoku_logic.solving.Sudoku import Sudoku
from sudoku_logic.solving.utils import flatten

AUTH_KEY = os.environ.get('SUDOSOLVE_API_AUTH_KEY')
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
            unsolved = req_data.get("unsolved")
        except LookupError:
            return Response('The request is invalid.\n', status=400)

        try:
            puzzle = Sudoku(unsolved)
            solved = puzzle.backtracking_search()
        except ValueError:
            return Response('Could not build a Sudoku grid.\n', status=400)

        if not solved:
            return Response('Could not solve the Sudoku.\n', status=400)

        # puzzle.display()
        # print(jsonify({"solved": puzzle.assignment_to_str()}))
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
            encoded: str = req_data.get('image')
        except LookupError:
            return Response('The request is invalid.\n', status=400)

        try:
            decoded: Image = asarray(b64ToImage(encoded=encoded))
            rows = analyze_image(image=decoded, debug=False)
            board = ''.join(map(str, flatten(rows)))
        except Exception as e:
            return Response(str(e), status=400)

        return jsonify({"board": board})


class SudokuGeneratorResource(Resource):
    def get(self):
        try:
            auth = request.headers.get('Auth')
        except LookupError:
            return Response('Authentication needed.\n', status=401)

        if auth != AUTH_KEY:
            print(auth)
            print(AUTH_KEY)
            return Response('Authentication didn\'t succeed.\n', status=401)

        try:
            level = DifficultyLevel(request.args.get('level', ''))
        except ValueError:
            return Response('That is not a correct difficulty level.', status=400)

        board = get_sudoku(level)
        return jsonify({'generated': board})


api.add_resource(SudokuSolverResource, '/solve')
api.add_resource(SudokuIdentifierResource, '/identify')
api.add_resource(SudokuGeneratorResource, '/generate')


@app.route('/', methods=['GET'])
def helpPage():
    return render_template('help.html')


@app.route('/check_connection', methods=['GET'])
def isConnected():
    return jsonify({'connected': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
