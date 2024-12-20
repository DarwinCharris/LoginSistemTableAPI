import azure.functions as func
import logging
from TableActions import TableActions  #Table class 
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="InsertPerson")
@app.route(route="table/insert", methods=['POST'])
def insert_person(req: func.HttpRequest) -> func.HttpResponse:
    #Try to get the body of the request and make the insertion
    try:
        data = req.get_json()
        table_actions = TableActions()
        result = table_actions.insert_person(data)
        return func.HttpResponse(
        json.dumps(result),
        status_code=201)
    except Exception as e:
        logging.error(f"Insertion error: {str(e)}")
        #Conflict error (email already in use)
        if str(e).__contains__("EntityAlreadyExists"):
            return func.HttpResponse(
            json.dumps({"error": "This email is already in use"}),
            status_code=409)
        #Other errors 
        return func.HttpResponse(
        json.dumps({"error": f"Unexpected error {str(e)}"}),
        status_code=500)

@app.function_name(name="GetPersonById")
@app.route(route="table/get", methods=['GET'])
def get_person(req: func.HttpRequest) -> func.HttpResponse:
    person_mail = req.params.get("mail")
    if not person_mail:
        return func.HttpResponse("Por favor, proporciona un id.", status_code=400)

    table_actions = TableActions()
    person = table_actions.get_person_by_id(person_mail)
    if person:
        return func.HttpResponse(
        json.dumps(person),
        status_code=200)
    else:
        return func.HttpResponse(
        json.dumps({"error": "Person not found"}),
        status_code=404)
    
@app.function_name(name="ChangePassword")
@app.route(route="table/changepassword", methods=['POST'])
def insert_person(req: func.HttpRequest) -> func.HttpResponse:
    #Try to get the body of the request and make the change
    try:
        data = req.get_json()
        if "mail" not in data or "password" not in data:
            return func.HttpResponse(
            json.dumps({"error": "mail and password must be provided"}),
            status_code=400)
        table_actions = TableActions()
        result = table_actions.change_password(data["mail"], data["password"])
        if result is None:
            return func.HttpResponse(
            json.dumps({"error": "Person not found"}),
            status_code=404)
        return func.HttpResponse(
        json.dumps(result),
        status_code=201)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
        json.dumps({"error": f"Unexpected error {str(e)}"}),
        status_code=500)

