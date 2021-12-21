import uuid
import os
from flask import Flask, request
from pylint import epylint as lint

app = Flask(__name__)

@app.route('/lint', methods=['POST'])
def linter():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):

    # get code from request
    json = request.json
    user_code = json['code']

    # create temp file to contain users code
    temp_name = uuid.uuid4()
    temp_file = f'{temp_name}.py'
    with open(temp_file, 'w') as file:
      file.write(str(user_code))

    # run pylint on file and capture output
    (pylint_stdout, pylint_stderr) = lint.py_run(temp_file, return_std=True)

    # delete temp file as no longer needed
    if os.path.exists(temp_file):
      os.remove(temp_file)

    return pylint_stdout.getvalue()
  else:
    return 'Content-Type not supported!'

if __name__ == "__main__":
  app.run()
