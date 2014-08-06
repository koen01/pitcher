from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

### Python Requests items for authentication with MD api ###
token = 'md-token xxxxxx'
headers = {'Accept': 'application/json', 'content-type':'application/json', 'Authorization': token }


### Flask app.routes below ###

# Homepage, nothing to see here, move along....
@app.route("/") 
def home():
  return render_template('home.html')

#Use the query string passed to this path to add a client to the MD platform
@app.route('/md_post') 
def md_post():
    client_id = request.args.get('id')
    first_name = request.args.get('first_name')
    infix = request.args.get('infix')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    date_of_birth = request.args.get('date_of_birth')
    gender_query = gender = request.args.get('gender') 
    if gender_query == 'Man' : gender = 'm'
    else: gender = 'f'
    post_url = 'https://orbisggz.training.minddistrict.com/api/1/c/'
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "infix": infix,
	"gender": gender,
	"date_of_birth": date_of_birth,
        "email": email,
	"id": client_id,
	"active": False
        }
    r = requests.post(post_url,data=json.dumps(data),headers=headers)
    print r.status_code
    print r.text
    result = client_details(client_id)
    return render_template("post.html",
                        first_name = result["first_name"],
                        infix = result["infix"] ,
                        last_name = result["last_name"],
                        email =  result["email"],
   	                client_id =  result["id"] )

#Use the query string passed to this path to find and update the specific client in MD platform
@app.route('/md_patch') 
def md_patch():
    client_id = request.args.get('id')
    first_name = request.args.get('first_name')
    infix = request.args.get('infix')
    last_name = request.args.get('last_name')
    email = request.args.get('email')  
    date_of_birth = request.args.get('date_of_birth')
    gender_query = gender = request.args.get('gender')
    if gender_query == 'Man' : gender = 'm'
    else: gender = 'f'
    patch_url = find_client_url(client_id)
    data = {
	"first_name": first_name,
        "last_name": last_name,
        "infix": infix,
	"email": email,
	"date_of_birth": date_of_birth,
	"gender": gender
        }
    r = requests.patch(patch_url,data=json.dumps(data),headers=headers)
    print r.status_code
    print r.text
    result = client_details(client_id)	
    return render_template("patch.html", 
			first_name = result["first_name"],
			infix = result["infix"] ,
			last_name = result["last_name"],
			email =  result["email"],
			client_id =  result["id"] )

### Helper functions ###

#list all clients in MD platform
def list_clients(): 
    url = 'https://orbisggz.training.minddistrict.com/api/1/c/items'
    r = requests.get(url,data=None,headers=headers)
    return r.text

#find a specific client based on the client_id passed to flask (because MD uses different ID's)
def find_client_url(client_id):  
    client_list = json.loads(list_clients())
    client_item = [item["@url"] for item in client_list["@items"]
            if item["id"] == client_id]
    client_url = str(client_item[0])
    return client_url

#get details of specific client
def client_details(client_id):
    client_list = json.loads(list_clients())
    client_detail = [item for item in client_list["@items"]
            if item["id"] == client_id]
    client_details = (client_detail[0])
    return  client_details

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

