from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import requests
import json
import re

client = MongoClient('localhost:27017')
db = client.knowledgebase

app = Flask( __name__ )
port = '5000'


@app.route('/api_search', methods=['POST'])
def api_search():
    search_data = json.loads(request.get_data().decode('utf8'))
    search_query = search_data['conversation']['memory']['query']['raw']
    print(search_query)
    search_type = search_data['conversation']['memory']['search-type']['raw']

    i = 0
    replies = ""
    if search_type in ['wiki', 'ngpbug']:
        r = requests.get('http://10.52.12.225:5002/' + search_type + '/' + search_query)
        data = r.json()
        if search_type == 'wiki':
            for res in data['result']:
                i += 1
                replies = replies + "\n" + res['title'] + "\n" + res['link'] + "\n"
                if i >= 10:
                    break
        elif search_type == 'ngpbug':
            for res in data['result']:
                i += 1
                replies = replies + "\n" + res['component'] + "\n" + res['link'] + "\n"
                if i >= 10:
                    break

    else:
        w = requests.get('http://10.52.12.225:5002/wiki/' + search_query)
        links = w.json()
        l_replies = ""
        b_replies = ""
        for res in links['result']:
            i += 1
            l_replies = l_replies + "\n" + res['title'] + "\n" + res['link'] + "\n"
            if i >= 5:
                break
        replies = l_replies
        n = requests.get('http://10.52.12.225:5002/ngpbug/' + search_query)
        bugs = n.json()
        for res in bugs['result']:
            i += 1
            b_replies = b_replies + "\n" + res['component'] + "\n" + res['link'] + "\n"
            if i >= 10:
                break
        replies = replies + b_replies
    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': replies,
        }]
    )


@app.route('/username', methods=['POST'])
def username():
    search_data = json.loads(request.get_data().decode('utf8'))
    username = search_data['conversation']['participant_data']['userName']

    message = "Hey," + " " + username + "!"
    return jsonify(
        status=200,
        replies=[{
            'type': 'text',
            'content': message,
        }]
    )


@app.route( '/store_conversation', methods=['POST'] )
def store_conversation():
    try:
        search_data = json.loads(request.get_data().decode('utf8'))
        print(search_data)
        con_id = search_data['conversation']['conversation_id']
        a = requests.get('https://api.recast.ai/connect/v1/conversations/' + con_id,
                          headers={'Authorization': 'xoxp-289803715811-381563306374-466687061664-7c5eb091e8a3ddfa6aa35e2ebfc0472a'})
        con = a.json()
        if 'response' in search_data['conversation']['memory'] and search_data['conversation']['memory']['response'] is not None:
            response_title = search_data['conversation']['memory'][
                'response']  # Title of the last response to which user gave rating
        else:
            response_title = ""
        intent = search_data['conversation']['memory']['intent']                #Intent triggered to send last response

        message = con['results']['messages']
        i = len(message) - 1
        print(i)
        while i >= 0:
            message_type = message[i]['attachment']['type']
            if message_type == "text":
                if response_title == message[i]['attachment']['content']:
                    if response_title == message[i - 1]['attachment']['content']:
                        invalid_response = message[i - 1]['attachment']['content']
                        break
                    else:
                        invalid_response = message[i]['attachment']['content']
                        break
            elif message_type in ("buttons", "quickReplies"):
                if 'title' in message[i]['attachment']['content'] and message[i]['attachment']['content']['title'] is not None:
                    res = message[i]['attachment']['content']['title']
                else:
                    res = message[i]['attachment']['content']['elements'][0]['title']
                if re.split( response_title, res ):
                    if 'title' in message[i - 1]['attachment']['content'] and message[i - 1]['attachment']['content']['title'] is not None:
                        res_repetitive = message[i - 1]['attachment']['content']['title']
                    else:
                        res_repetitive = message[i - 1]['attachment']['content']['elements'][0]['title']
                    if re.split( response_title, res_repetitive ):
                        invalid_response = message[i - 1]['attachment']['content']       #Last response to which user gave rating
                        unknown_expression = message[i - 2]['attachment']['content']                 #Expression(User Input) that chatbot failed to interpret
                        break
                    else:
                        invalid_response = message[i]['attachment'][
                            'content']  # Last response to which user gave rating
                        unknown_expression = message[i - 1]['attachment'][
                            'content']  # Expression(User Input) that chatbot failed to interpret
                        break
            i -= 1

        print("\nUser query unsupported by chatbot\n", unknown_expression)                                           #New User Input
        print("\nResponse that did not solve user query\n", invalid_response)                                          #response received negative rating
        print("\nIntent triggered to send response for above unknown user query\n", intent)                          #intent of wrong response
        if unknown_expression and intent:
            if db.Expressions.find_one({"expression": unknown_expression}):
                print(intent)
            else:
                db.Expressions.insert_one({
                    "expression": unknown_expression,
                    "invalid_intent": intent,
                    "valid_intent": ""
                })
        expression = db.Expressions.find()
        for ex in expression:
            print(ex)
        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': 'SUCCESS',
            }]
        )
    except Exception as e:
        return dumps({'error': str(e)})

@app.route( '/create_expression', methods=['POST'] )
def create_expression():
    try:
        search_data = json.loads( request.get_data().decode( 'utf8' ) )
        print( search_data )
        con_id = search_data['conversation']['conversation_id']
        a = requests.get( 'https://api.recast.ai/connect/v1/conversations/' + con_id,
                          headers={'Authorization': '134559a2519e476a5d45c481ce9462e2'} )
        con = a.json()
        print(search_data['conversation']['memory']['response'])
        if 'response' in search_data['conversation']['memory'] and search_data['conversation']['memory']['response'] is not None:
            response_title = search_data['conversation']['memory'][
                'response']  # Title of the last response to which user gave rating
        else:
            response_title = ""
        intent = search_data['conversation']['memory']['intent']  # Intent triggered to send last response

        message = con['results']['messages']
        i = len( message ) - 1
        while i >= 0:
            message_type = message[i]['attachment']['type']
            if message_type == "text":
                if response_title == message[i]['attachment']['content']:
                    print( message[i]['attachment']['content'] )
                    if response_title == message[i - 1]['attachment']['content']:
                        valid_response = message[i - 1]['attachment']['content']
                        known_expression = message[i - 2]['attachment'][
                            'content']  # Expression(User Input) that chatbot failed to interpret
                        break
                    else:
                        valid_response = message[i]['attachment']['content']
                        known_expression = message[i - 1]['attachment'][
                            'content']  # Expression(User Input) that chatbot failed to interpret
                        break

            elif message_type in ("buttons", "quickReplies", "list"):
                if 'title' in message[i]['attachment']['content'] and message[i]['attachment']['content']['title'] is not None:
                    res = message[i]['attachment']['content']['title']
                else:
                    res = message[i]['attachment']['content']['elements'][0]['title']
                if re.split( response_title, res ):
                    if 'title' in message[i - 1]['attachment']['content'] and message[i - 1]['attachment']['content']['title'] is not None:
                        res_repetitive = message[i - 1]['attachment']['content']['title']
                    else:
                        res_repetitive = message[i - 1]['attachment']['content']['elements'][0]['title']
                    if re.split( response_title, res_repetitive ):
                        valid_response = message[i - 1]['attachment'][
                            'content']  # Last response to which user gave rating
                        known_expression = message[i - 2]['attachment'][
                            'content']  # Expression(User Input) that chatbot failed to interpret
                        if known_expression == res_repetitive:
                            known_expression = message[i - 3]['attachment']['content']
                        break
                    else:
                        valid_response = message[i]['attachment'][
                            'content']  # Last response to which user gave rating
                        known_expression = message[i - 1]['attachment'][
                            'content']  # Expression(User Input) that chatbot failed to interpret
                        break
            i -= 1

        print( "\nUser query supported by chatbot\n", known_expression )  # New User Input
        print( "\nResponse that has solved user query\n", valid_response )  # response received negative rating
        print( "\nIntent triggered to send response for above unknown user query\n",
               intent )  # intent of wrong response
        #db.Expressions.remove()
        if known_expression and intent:
            if db.Expressions.find_one({"expression": known_expression}):
                db.Expressions.update(
                    {"expression": known_expression},
                    {
                        "$set": {
                            "valid_intent": intent
                        }
                    },
                )
            else:
                db.Expressions.insert_one({
                    "expression": known_expression,
                    "invalid_intent": "",
                    "valid_intent": intent
                })

        expression = db.Expressions.find()
        for ex in expression:
            print( ex )

        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': 'SUCCESS',
            }]
        )
    except Exception as e:
        print(str(e))

@app.route('/save_timestamp', methods=['POST'])
def save_timestamp():
    try:
        search_data = json.loads( request.get_data().decode( 'utf8' ) )
        print(search_data)

        return jsonify(
            status=200,
            replies=[{
                'type': 'text',
                'content': '',
            }]
        )
    except Exception as e:
        print(str(e))





@app.route( '/errors', methods=['POST'] )
def errors():
    print( json.loads( request.get_data().decode( 'utf8' ) ) )
    return jsonify( status=200 )

@app.route( '/slack', methods=['GET, POST'] )
def slack():
    e = requests.get('https://slack.com/api/rtm.connect')
    events = e.json()
    print(events)


app.run(port=port)


