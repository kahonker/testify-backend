from app import app
from app.ai import make_test_call

if __name__ == "__main__":
    #app.run(host="127.0.0.1", port=5000, debug=True)
    print(make_test_call("Python", 5))