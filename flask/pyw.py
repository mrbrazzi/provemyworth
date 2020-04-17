from pathlib import Path

from flask import Flask, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename

BASE_DIR = Path('.')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    # this has changed from the original example because the original did not work for me
    # return filename[-3:].lower() in ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(req, param):
    if param not in req.files:
        print(f'Missing information detected. {param} not found. Try again.')
        return redirect(req.url)
    file = req.files[param]
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('Missing information detected. Filename empty. Try again.')
        return redirect(req.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(BASE_DIR / app.config['UPLOAD_FOLDER'] / filename)
        return filename
    return redirect(req.url)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if not request.form:
            print('Missing information detected. Missing data. Try again.')
            return redirect(request.url)
        print('\n*** Received values ***')
        # print(request.form)
        for param in request.form.lists():
            print(f'{param[0].capitalize()}: {param[1][0]}')
        print('\n')
        # check if the post request has the files
        filename = save_file(req=request, param='code')
        save_file(req=request, param='image')
        save_file(req=request, param='resume')
        return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=code>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
