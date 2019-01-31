from flask import Flask
from flask import request
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

@app.route('/change', methods=['GET'])
def changeZet():
    file = request.args.get('file')
    tag = request.args.get('tag')
    url = request.args.get('url')
    summary = request.args.get('summary')
    note = request.args.get('note')
    title = request.args.get('title')
    allArgs = [file, tag, url, summary, note, title]
    path = "/home/jweezy/Documents/Code/zg-tutorial/zettels/"
    f = parseFile(file)
    if tag != None:
        f.update({'tags': tag})
    if title != None:
        f.update({'title': title})
    if summary != None:
        f.update({'summary': summary})
    if note != None:
        f.update({'note': note})
    if url != None:
        f.update({'url': url})
    writeFile(getFile(file,path), f)

    return str(parseFile(file))


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

def writeFile(filePath, vals):
    file = open(filePath, 'w')
    firstLine = True
    for i in vals.keys():
        firstLine = True
        list = vals.get(i).split('\n')
        for j in list:
            if firstLine:
                file.write(i+': ' + j +'\n')
                firstLine = False
                continue
            file.write(j+'\n')
    file.close()

def getFile(file,path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for folder in dirnames:
            for (dirpath, dirnames, files) in os.walk(path+folder):

                for f in files:
                    if f == file:
                        return path+folder+'/'+file
