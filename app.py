from flask import Flask, jsonify, abort, make_response, request, render_template, redirect, url_for
from forms import ExpenseForm
from models import expenses
import logging
import requests
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/expenses/", methods=["GET"])
def expenses_list_api_v1():
    return jsonify(expenses.all())


@app.route("/api/v1/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = expenses.get(expense_id)
    if not expense:
        abort(404)
    return jsonify({"expense": expense})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/api/v1/expenses/", methods=["POST"])
def create_expense():
    # wyodrebnic całą funkcje
    if not request.json or not 'title' in request.json:
        abort(400)
    expense = {
        'id': 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'koszt': request.json['koszt']
    }
    expenses.create(expense)
    return jsonify({'expense': expense}), 201


@app.route("/api/v1/expenses/<int:expense_id>", methods=['DELETE'])
def delete_expense(expense_id):
    result = expenses.delete(expense_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    expense = expenses.get(expense_id)
    if not expense:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'koszt' in data and not isinstance(data.get('koszt'), int)
    ]):
        abort(400)
    expense = {
        'id': expense_id,
        'title': data.get('title', expense['title']),
        'description': data.get('description', expense['description']),
        'koszt': data.get('koszt', expense['koszt'])
    }
    expenses.update(expense_id, expense)
    return jsonify({'expense': expense})


# first version without REST


@app.route("/expenses/", methods=["GET", "POST"])
def expenses_list():
    form = ExpenseForm()
    error = ""
    if request.method == "POST":
        # create_expense() dopisac
        if form.validate_on_submit():
            response = requests.post(str(request.url_root) + url_for("create_expense"),
                                     json=form.data, headers={'Content-type': 'application/json',
                                                              'Accept': 'text/plain'})
            logging.info("response code: %s" % response.status_code)
            if response.status_code != 201:
                logging.error("Technical problem with API funcion")
        return redirect(url_for("expenses_list"))
    return render_template("expenses.html", form=form, expenses=expenses.all(), error=error)


@app.route("/expenses/<int:expense_id>/", methods=["GET", "POST"])
def expense_details(expense_id):
    expense = expenses.get(expense_id)
    form = ExpenseForm(data=expense)

    if request.method == "POST":
        if form.validate_on_submit():
            full_url = str(request.url_root) + \
                url_for("update_expense", expense_id=expense_id)
            logging.info("full_url %s" % full_url)
            response = requests.put(full_url,
                                    json=form.data, headers={'Content-type': 'application/json',
                                                             'Accept': 'text/plain'})
            logging.info("response code: %s" % response.status_code)
            if response.status_code != 201:
                logging.error("Technical problem with API funcion")
            # expenses.update(expense_id - 1, form.data)
            return redirect(url_for("expenses_list"))
    return render_template("expense.html", form=form, expense_id=expense_id)


if __name__ == "__main__":
    app.run(debug=True)
