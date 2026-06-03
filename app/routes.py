from app import app
from app.ai import make_test_call

@app.route('/')
@app.route('/index')
def index():
    return "Hello world!"

@app.route('/make_test/<subject>&<question_amount>')
def make_test(subject: str, question_amount: int):
    return make_test_call(subject, question_amount)
