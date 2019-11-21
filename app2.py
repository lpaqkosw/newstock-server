#-*- coding: utf-8 -*-

from flask import Flask, request
from flask_cors import CORS
import findStock
import datetime as dt
import nlp
import json

app = Flask(__name__)

cors = CORS(app, resources={
    r"/*": {"origin":  "*"},
    })


@app.route('/company', methods=['GET'])
def dashboard():
    data = request.args.to_dict()
    print "Recieved data"
    companyName = data['companyname']
    cleanedCompanyName = nlp.nlp(companyName)[0].encode("utf-8")
    date = data['date']
    print cleanedCompanyName
    print date
    code = findStock.findCode(cleanedCompanyName)
    page = findStock.findPage(date)
    if code is not None:
        print "Company code found. Sending price data back to client"

        '''
        if (dt.datetime.today().strftime("%Y.%m.%d") == dt.datetime.strptime(date,"%Y.%m.%d").strftime("%Y.%m.%d")):    
            finalData = findStock.todayInfo(code)
            finalData[0]['date'] = dt.datetime.strptime(date,"%Y.%m.%d").strftime("%Y.%m.%d")
            return json.dumps(finalData), 200

        else:
        '''
 
        finalData = findStock.pastInfo(code, page)
        return finalData, 200
    else:
        print "code not found"
        return "Failure", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 80)
