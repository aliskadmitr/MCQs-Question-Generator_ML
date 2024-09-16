from flask import Flask, request, render_template

# creating app
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        text = ''
        if 'files[]' in request.files:
            files = request.files.getlist("files[]")
            for file in files:
                print(file)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


