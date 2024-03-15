from app.dashboard import main
from flask import render_template, request, flash, session, send_file
import os
from wtforms.validators import InputRequired
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_login import login_required
from config.dev import ALLOWED_EXTENSIONS, UPLOAD_PATH, OUTPUT_PATH
from haystack.nodes import QuestionGenerator
from pypdf import PdfReader
from datetime import datetime


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadFileForm(FlaskForm):
    file = FileField("File",
                     validators=[
                         InputRequired()
                     ])
    submit = SubmitField("Upload File")


@main.route('/', methods=['GET', "POST"])
@main.route('/home', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    return render_template('HomeContent.html', form=form)


@main.route('/upload', methods=['GET', "POST"])
@login_required
def upload():
    form = UploadFileForm()
    file = form.file.data
    show_btn = False
    if request.method == "POST":
        if not allowed_file(file.filename):
            flash('File format can be either pdf or text', 'error')
        else:
            if form.validate_on_submit():
                file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), UPLOAD_PATH,
                                         secure_filename(file.filename))
                file_name_splitup = os.path.splitext(file.filename)
                session['file_extn'] = file_name_splitup[1]
                session['file_path'] = file_path
                file.save(file_path)
                show_btn = True
                flash('File has been uploaded successfully', 'success')
    return render_template('FileUpload.html', form=form, show_btn=show_btn)


@main.route('/output', methods=['GET', "POST"])
@login_required
def output():
    text = ""
    if session['file_extn'] == '.pdf':
        reader = PdfReader(session['file_path'])
        for page in reader.pages:
            text += page.extract_text() + "\n"
    else:
        file = open(session['file_path'], "r", encoding="utf8")
        text = file.read()
        file.close()

    qg = QuestionGenerator()
    result = qg.generate(text)
    my_output = session['result'] = result

    return render_template('result.html', my_output=my_output)


@main.route('/download', methods=['GET', "POST"])
@login_required
def download():
    op_file_name = "result_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), OUTPUT_PATH, op_file_name)
    if session['result']:
        split_string = str(session['result']).split(",")
        file = open(file_path, 'w')
        for s in split_string:
            file.write(s + "\n")
        file.close()
        return send_file(str(file_path), as_attachment=True)
