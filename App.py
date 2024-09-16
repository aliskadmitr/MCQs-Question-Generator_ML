from flask import Flask, request, render_template
from PyPDF2 import PdfReader, PdfWriter
# creating app
app = Flask(__name__)


def process_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num]
        text+=page_text
    return text

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        text = ''
        if 'files[]' in request.files:
            files = request.files.getlist("files[]")
            for file in files:
                if file.filename.endswith('.pdf'):
                    #process pdf files
                    text += process_pdf(file)
                else:
                    #process text file
                    text += file.read().decode('utf-8')

    num_questions = int(request.form['num_questions'])
    mcqs = qenerate_mcqs(text, num_questions=num_questions)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


