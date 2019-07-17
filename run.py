from flask import Flask, render_template, request, send_from_directory, make_response
import main
import os

app = Flask(__name__)

@app.route('/subtitle')
def subtitle():
    return render_template('subtitle.html')

@app.route('/av', methods=["GET", "POST"])
def av():
    global av
    av = request.form.get("av")
    if not av:
        return "invalid input"
    if not av.isdigit():
        return "invalid input"
    else:
        main.SubRequest(av)
        with open(f'data/{av}/content.txt', 'r') as f:
            subs = f.readlines()
        if subs == []:
            return render_template("download.html", subs = ['No subtitle provided'])
        else:
            return render_template("download.html", subs = subs)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    response = make_response(send_from_directory(f'{os.getcwd()}/data/{av}', filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    return response

@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()
