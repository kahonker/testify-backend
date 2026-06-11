from app import app
from app.ai import make_test_call

@app.route('/')
@app.route('/index')
def index():
    return "Hello world!"

@app.route('/make_test/<subject>/<question_amount>')
async def make_test(subject: str, question_amount: int):
    return await make_test_call(subject, int(question_amount))
