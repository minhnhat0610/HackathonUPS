import json
from tabnanny import check
from flask import Flask, make_response, render_template,request, send_file
import webbrowser
from FlattedPDF import Main
from werkzeug.utils import secure_filename
import os
import fitz


app = Flask(__name__,template_folder="./html")
app.config["UPLOAD_FOLDER"] = './upload'
app.config["RESULT_FOLDER"] = './result_pdf'

FilePath = "Filled_form.pdf"

def uploadFiles():
    receivedData = request.files.getlist('files')
    for i in range(len(receivedData)):
        if(receivedData[i]):
            filename = secure_filename(receivedData[i].filename)
            receivedData[i].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


def Draw_PDF(fileDir, saveDir,auditResult):
    invalidTextField = auditResult["Invalid_Text_Field"]
    invalidCheckBox = auditResult["Invalid_Check_Box"]

    doc = fitz.open(fileDir)
    doc.save(saveDir+"/result.pdf")
    # for page in doc:
    #     for field,corr in invalidTextField.items():
    #         drawBox = [corr["left"],corr["top"],corr["right"],corr["bottom"]]
    #         page.draw_rect(drawBox,  color = (1, 0, 0), width = 2)
    #     page.finish()
    
    doc = fitz.open(saveDir+"/result.pdf")
    # Draw invallid Text Field
    for field,corr in invalidTextField.items():
        for Checkcorr in invalidCheckBox:
            drawBox = [corr["left"],corr["top"],corr["left"]+150,corr["top"]+10]
            drawBox2 = [Checkcorr[0],Checkcorr[1],Checkcorr[0]+10,Checkcorr[1]+10]
            for page in doc:
                page.draw_rect(drawBox,  color = (1, 0, 0), width = 1)
                page.draw_rect(drawBox2, color = (1, 0, 0), width = 1)
    doc.saveIncr()

    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validate",methods=['POST'])
def validate():
    try:
        # Upload file to Flask server
        uploadFiles()
        uploadDir = app.config["UPLOAD_FOLDER"]
        fileDir = uploadDir + "/" + os.listdir(uploadDir)[0]

        auditResult = Main(fileDir)

        saveDir = app.config["RESULT_FOLDER"]
        Draw_PDF(fileDir,saveDir,auditResult)

        return make_response(json.dumps(auditResult),200)
    except Exception as e:
        return make_response(f"Internal Error: {e.__traceback__} {e.__cause__}",500)

if __name__ == "__main__":
    # the command you want
    webbrowser.open('http://127.0.0.1:5000')
    app.run(port=5000,debug=True)