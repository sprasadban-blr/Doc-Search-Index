''' pip install wtforms '''
''' pip install flask '''
''' Flask Examples: https://pythonspot.com/flask-web-app-with-python/'''
''' https://stackoverflow.com/questions/45227076/how-to-send-data-from-flask-to-html-template '''
from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import Form, TextField, validators
import requests
import json
from URLConstants import URLConstants
 
# App config.
DEBUG = True
app = Flask(__name__)
app.debug = DEBUG
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class DogGleWebForm(Form):
    urlConstants = URLConstants()
    txtsearch = TextField('txtsearch', validators=[validators.required()])
    
    def checkDocLinks(self, doctype, searchPattern):
        responseJson = ""
        if doctype == 'wiki':
            wikiUrl = self.urlConstants.getWikiURL() + searchPattern
            response = requests.get(wikiUrl)
            if(response.status_code == 200):
                responseJson = response.text
        elif doctype == 'ngpbug':
            ngpBugUrl = self.urlConstants.getNGPBugURL() + searchPattern
            response = requests.get(ngpBugUrl)
            if(response.status_code == 200):
                responseJson = response.text                
        elif doctype == 'bcp':
            bcpIncidentUrl = self.urlConstants.getBCPIncidentURL() + searchPattern
            response = requests.get(bcpIncidentUrl)
            if(response.status_code == 200):
                responseJson = response.text                
        
        return responseJson        

@app.route('/sap/docs', methods=['GET', 'POST'])
def docs():
    searchPattern = session.get('search_criteria')
    doctype = session.get('doc_type')    
    form = DogGleWebForm(request.form)    
    responseJson = json.loads(form.checkDocLinks(doctype, searchPattern))
    return render_template("DocgleSearchResult.html", result=responseJson)
     
@app.route("/sap", methods=['GET', 'POST'])
def docgle():
    ''' reset the session data '''
    session.clear()
    form = DogGleWebForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        searchPattern = request.form['txtsearch']
        print(searchPattern)
        if form.validate():
            flash('Success!')
            session['search_criteria'] = searchPattern
            if request.form.get('wiki') == 'wiki_clicked':
                session['doc_type'] = 'wiki'
            elif request.form.get('ngpbug') == 'ngpbug_clicked':
                session['doc_type'] = 'ngpbug'
            elif request.form.get('bcp') == 'bcp_clicked':
                session['doc_type'] = 'bcp'
            return redirect(url_for('docs'))
        else:
            flash('Error: Please enter search terms.')
 
    return render_template('DocgleTemplate.html', form=form)

@app.before_request
def session_management():
    ''' make the session last indefinitely until it is cleared '''
    session.permanent = True
    
if __name__ == "__main__":
    app.run(host="10.53.216.88", port=5000)
    #app.run()