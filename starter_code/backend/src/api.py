import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import traceback

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    
    try :
        print("From getrinks() method")
        print(Drink.query.all(), flush=True)
        drinks= [x.short() for x in Drink.query.all()]
        #Drink.query.order_by(Drink.id).all()
        return jsonify({
                        "success": True, 
                        "drinks": drinks
                        }), 200
    except:
        print(traceback.format_exc(), flush=True)
        abort(404)
#         raise AuthError({
#                 'code': 'not found',
#                 'description': 'Unable to find drinks.'
#             }, 404)
        #abort(error)

'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_details(payload):
    #print()
    try:
        drinks= [x.long() for x in Drink.query.all()]
        return jsonify({
                    "success": True, 
                    "drinks": drinks
                    }), 200
    except:
        print(traceback.format_exc(), flush=True  )              
        abort(404)
    

'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    #print(payload)
    try :
        body = request.get_json()
        if body == None:
            abort(404)
        
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        
        print("title:" + new_title, flush=True)
        print(new_recipe, flush=True)
        
        #[{'color': string, 'name':string, 'parts':number}]
        
        drink= Drink(title=new_title, recipe=json.dumps(new_recipe))
        
        #drink.id 
        drink.insert() 
        
        drinks=[x.long() for x in Drink.query.all()]
        print(drinks, flush=True)
        
        return jsonify({
                        "success": True, 
                        "drinks": drinks
                        }), 200
    except:
        print(traceback.format_exc() , flush=True )        
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    print("id= " + str(id), flush=True)
    try :
        drink= Drink.query.filter(Drink.id == id).one_or_none()
        print(drink, flush=True)
        
        if drink is None :
            abort(404)
            
        body = request.get_json()
        if body is None:
            abort(404)
        
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        
        if new_title is not None:
            drink.title=new_title
        
        if new_recipe is not None:
            drink.recipe=new_recipe
            
        drink.update()    
                
        
        drinks= [x.long() for x in Drink.query.all()]
        return jsonify({
                        "success": True, 
                        "drinks": drinks
                        }), 200
    except:
        (traceback.format_exc()  )        
        abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
    
        if drink is None:
            abort(404)
    
        drink.delete()
        drinks= [x.long() for x in Drink.query.all()]
        return jsonify({
                        "success": True, 
                        "drinks": drinks
                        }), 200
    except:
        abort(422)        

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def notfound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error
                    }), error.status_code
