from flask import request, jsonify, abort
from flask import current_app as app
from .models import Order
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session
import requests


# Order Routes #########################################################################################################
#{
#   "userId" : 1    
#   "number_of_pieces" : 2,
#}
@app.route('/order/create', methods=['POST'])
def create_order():
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json

    response = None
    try:      
        new_order =  Order(
            number_of_pieces = content['number_of_pieces'],         
        )    
        session.add(new_order) 
        session.commit()

        payment = {}
        payment['userId'] = content['userId']
        payment['money'] = 10 * new_order.number_of_pieces # 10 por pieza
        # payment_response = requests.post('http://localhost:17000/payment', json=payment).json()  
        payment_response = requests.post('http://192.168.17.3:32700/payment/pay', json=payment).json()

        if payment_response['status']:
            print("bien")
            # Mandar piezas al machine
            manufacture_info = {}
            manufacture_info['number_of_pieces'] = new_order.number_of_pieces
            manufacture_info['orderId'] = new_order.id
            # response = requests.post('http://localhost:15000/machine/request_piece', json=manufacture_info).json()
            response = requests.post('http://192.168.17.3:32700/machine/request_piece', json=manufacture_info).json()
            # Crear el delivery
            delivery_info = {}
            delivery_info['orderId'] = new_order.id
            delivery_info['delivered'] = False
            # requests.post('http://localhost:14000/create_delivery', json=delivery_info).json()
            requests.post('http://192.168.17.3:32700/delivery/create', json=delivery_info).json()
        else:
            print("mal") 
            response = payment_response   
  
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)

    session.close()
    return response

# Machine notifica para actualizar delivery.
#{
#    "orderId": 1
#}
@app.route('/order/notify', methods=['POST'])
def notify_piece():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json

    delivery_update = {}
    delivery_update['orderId'] = content['orderId']
    delivery_update['delivered'] = True

    # response = requests.post('http://localhost:14000/update_delivery', json=delivery_update).json()
    response = requests.post('http://192.168.17.3:32700/delivery/update', json=delivery_update).json()
    print(response)  
    return response

# Error Handling #######################################################################################################
@app.errorhandler(UnsupportedMediaType)
def unsupported_media_type_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(BadRequest)
def bad_request_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(NotFound)
def resource_not_found_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(InternalServerError)
def server_error_handler(e):
    return get_jsonified_error(e)


def get_jsonified_error(e):
    traceback.print_tb(e.__traceback__)
    return jsonify({"error_code":e.code, "error_message": e.description}), e.code


