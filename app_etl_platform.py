from flask import Flask, render_template, Response

from extractor import extract


app = Flask(__name__)


@app.route('/')
def upload_form():
    return render_template('download.html')


@app.route('/download')
def download_file():

    csv_file = extract()

    return Response(csv_file, mimetype = "text/csv", headers = {"Content-disposition":
                    "attachment; filename=reports.csv"})

    
if __name__ == "__main__":
    app.run("0.0.0.0", port=5002, debug=True)
