import os
from flask import Flask, request
from werkzeug.exceptions import BadRequest
# получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
# проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
# с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
# вернуть пользователю сформированный результат


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def file_proces(f, cmd, value):
    result = map(lambda v: v.strip(), f)
    if cmd == 'filter':
        result = filter(lambda v: value in v, result)
    if cmd == 'sort':
        value = bool(value)
        result = sorted(result, reverse=value)
    if cmd == 'unique':
        result = set(result)
    if cmd == 'limit':
        value = int(value)
        result = list(result)[:value]
    if cmd == 'map':
        value = int(value)
        result = map(lambda v: v.split(' ')[value], result)

    return result


@app.route("/perform_query")
def perform_query():
    try:
        cmd1 = request.args['cmd1']
        cmd2 = request.args['cmd2']
        value1 = request.args['value1']
        value2 = request.args['value2']
        file_name = request.args['file_name']
    except:
        return BadRequest(description="Нет аргумента")

    file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file):
        return BadRequest(description="Файл не найден")
    with open(file) as f:
        result = file_proces(f, cmd1, value1)
        result = file_proces(result, cmd2, value2)
        result = "\n".join(result)
    return app.response_class(result, content_type="text/plain")


app.run()
