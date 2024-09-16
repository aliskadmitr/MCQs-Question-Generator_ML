from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from PyPDF2 import PdfReader, PdfWriter
import spacy
import random
from collections import Counter

# creating app
app = Flask(__name__)
Bootstrap(app)

nlp = spacy.load("en_core_web_sm")


def generate_mcqs(text, num_questions=5):
    if text is None:
        return []

    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    num_questions = min(num_questions, len(sentences))
    selected_sentences = random.sample(sentences, num_questions)

    mcqs = []

    for sentence in selected_sentences:
        sent_doc = nlp(sentence)

        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]

        if len(nouns) < 2:
            continue

        noun_counts = Counter(nouns)

        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]
            question_stem = sentence.replace(subject, "______")

            answer_choices = [subject]

            distractors = list(set(nouns) - {subject})

            while len(distractors) < 3:
                distractors.append("[Distractor]")

            random.shuffle(distractors)
            for distractor in distractors[:3]:
                answer_choices.append(distractor)

            random.shuffle(answer_choices)
            correct_answer = chr(64 + answer_choices.index(subject) + 1)  # Convert index to letter
            mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs


def process_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text




@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        text = ''
        if 'files[]' in request.files:
            files = request.files.getlist("files[]")
            for file in files:
                if file.filename.endswith('.pdf'):
                    # process pdf files
                    text += process_pdf(file)
                else:
                    # process text file
                    text += file.read().decode('utf-8')

        num_questions = int(request.form['num_questions'])
        mcqs = generate_mcqs(text, num_questions=num_questions)
        # print(mcqs)
        mcqs_with_index = [(i + 1, mcq) for i, mcq in enumerate(mcqs)]
        # print(mcqs_with_index)
        return render_template('mcqs.html', mcqs=mcqs_with_index)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
