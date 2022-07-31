from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#using werkzeug so user doesn't get froggy and try to manupulate server with certain filenames
#path for storing uploaded file
UPLOAD_FOLDER = './upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#defualt webpage (landing page)
@app.route("/")
def index():
    return render_template("index.html")

#page where uploaded file is stored and processed
@app.route("/download", methods=['POST','GET'])
def download():
    #assignt all user provided imputs to variables, using same variables names for readability
    yAxis = request.form.get("yAxis")
    xAxis = request.form.get("xAxis")
    plotTitle = request.form.get("plotTitle")
    val = request.form.get("val")

    #user uploaded file is saved as foo.csv in the upload folder
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename("foo.csv")))

    #processing foo.csv into a heatmap
    df = pd.read_csv("./upload/foo.csv")
    result = df.pivot(index=yAxis, columns=xAxis, values=val )

    #plotting the data
    fig, ax = plt.subplots(figsize=(25,15))

    #setting title for plot
    plt.title(plotTitle,fontsize=24)
    ttl = ax.title
    ttl.set_position([0.5,1.15])

    # Hide ticks for X & Y axis
    ax.set_xticks([])
    ax.set_yticks([])

    # Use the heatmap function from the seaborn package
    sns.heatmap(result)
    #saving the data
    plt.savefig('./upload/foo.pdf')
    plt.savefig('./upload/foo.png')

    return render_template("download.html", plotTitle = plotTitle)


if __name__ =="__main__":
  app.run()
 
