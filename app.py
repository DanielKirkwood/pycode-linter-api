import uuid
import os
from flask import Flask, request
import pylint.lint
import pprint

app = Flask(__name__)

@app.route('/lint', methods=['POST'])
def linter():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):

    # get code from request
    json = request.json
    user_code = json['code']

    # create temp file to contain users code
    temp_name = uuid.uuid4().hex
    temp_file = temp_name + '.py'
    with open(temp_file, 'w') as file:
      file.write(str(user_code))

    options = [
      temp_file,
      '--output-format=json'
    ]
    results = pylint.lint.Run(options, do_exit=False).linter.reporter.messages

    # delete temp file as no longer needed
    if os.path.exists(temp_file):
      try:
        os.remove(temp_file)
      except OSError as e:
        print("Failed with:", e.strerror)
        print("Error code:", e.code)


    messages = []
    for m in results:
      messages.append({
        "messageID": m[0],
        "symbol": m[1],
        "message": m[2],
        "type": m[4],
        "line": m[10]
      })

    return {"payload": {"result": messages}, "success": "true"}
  else:
    return {"payload": {"result": 'Content-Type not supported!'}, "success": "false"}

if __name__ == "__main__":
  app.run()
