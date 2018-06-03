import logging
import subprocess
import understand
import sys
import os
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from yattag import Doc

# pip install plotly
# pip install yattag

# function to create the understand db file
def create_udb(udb_path, language, project_root):
    try:
        # create the .udb file
        output = subprocess.check_output(
            "und create -db {udb_path} -languages {lang}".format(udb_path=udb_path, lang=language),
            shell=True)
        logging.info(output)
        # add the project root to the file
        output = subprocess.check_output("und add -db {udb_path} {project}".format(
            udb_path=udb_path, project=project_root), shell=True)
        logging.info(output)
        # analyse the udb file to get the list of entities
        output = subprocess.check_output("und analyze -db {udb_path}".format(
            udb_path=udb_path), shell=True)
        logging.info(output)

    except subprocess.CalledProcessError as e:
        logging.exception(e.output)
        logging.fatal("udb creation failed")
        raise Exception


# get the path of the script file
#print('sys.argv[0] =', sys.argv[0])
#pathname = os.path.dirname(sys.argv[0])
#print('path =', pathname)
#print('full path =', os.path.abspath(pathname))
#abspathname = os.path.abspath(pathname)
#repo_name = 'java-sdk'
#print('Generating Understand Reports for '+ repo_name)
#udbPath = abspathname +'/'+repo_name+'/test.udb'
# create the understand db in the same location as the script file.
# replace the project name with the name of the repository
#create_udb(udbPath, 'Java', abspathname + '/'+repo_name)
#open the udb file
# db = understand.open(udbPath)
#
# print(len(db.ents()))
#
# db.close()

def getUnderstandReport(udb_path, report_dir_path):

    # set plotly credentials
    plotly.tools.set_credentials_file(username='', api_key='')

    # open the udb file
    db = understand.open(udb_path)
    images = []

    for a in db.root_archs():
        if (len(a.children()) > 0):
            for child in a.children():
                #print(child.longname())
                child.draw('Internal Dependencies', report_dir_path + '/dependency_' + child.name() + '.png')
                images.append('dependency_' + child.name() + '.png')

    metric_list = 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment'
    met = db.metric(metric_list)
    trace = go.Pie(labels=list(met.keys()), values=list(met.values()))
    plot = [trace]
    layout = go.Layout(title='Code Lines', width=800, height=640)
    fig = go.Figure(data=plot, layout=layout)

    py.image.save_as(fig, filename=report_dir_path + '/code_lines.png')

    db.close()

    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('style'):
                text('table, th, td {border: 1px solid black; border-collapse: collapse; padding:10px;white-space: nowrap;}')
        with tag('body'):
            with tag('h1'):
                text('Code BreakDown')
            with tag('table'):
                for key, value in met.items():
                    with tag('tr'):
                        with tag('td'):
                            text(key)
                        with tag('td'):
                            text(value)
            doc.stag('img', src=report_dir_path + '/code_lines.png')
            with tag('h1'):
                text('Dependency Graphs')
            for image in images:
                doc.stag('img', src=report_dir_path + "/" + image)

    report = open(report_dir_path+"/report.html", "w")
    report.write(doc.getvalue())
    report.close()

#getUnderstandReport(udbPath, abspathname + '/'+repo_name)