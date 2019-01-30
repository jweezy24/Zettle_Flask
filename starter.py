from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/grab/<string:filename>')
def grabZet(filename):
    vals = parseFile(filename)
    returnVal = '''
{title}
{summary}
{url}
{note}
{tags}
    '''.format(**vals)
    return str(returnVal)


def parseFile(file):
    path = "/home/jweezy/Documents/Code/zg-tutorial/zettels/"
    info = open(getFile(file,path), "r")
    files = {file: ''}
    dict = {"title":'', "summary": "", "url":'', "note":"", "tags":"" }
    for i in info:
        for j in dict.keys():
            if j+":" in i:
                currentTag = j
                if j == "url":
                    firstLine = i.split("url:")[1]
                    break
                firstLine = i.split(":")[1]
                break
        if firstLine != '':
            dict.update({currentTag: firstLine})
            firstLine = ''
        else:
            dict.update({currentTag: dict.get(currentTag)+ "\n" + i})
    info.close()
    return dict


def getFile(file,path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for folder in dirnames:
            for (dirpath, dirnames, files) in os.walk(path+folder):
                
                for f in files:
                    if f == file:
                        return path+folder+'/'+file
