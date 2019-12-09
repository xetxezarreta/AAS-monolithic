<<<<<<< HEAD
from application import create_app
from application.event_handler import Rabbit
from application.myjwt import rsa_singleton

app = create_app()

# create rabbitmq queues
exchange_name = 'payment_exchange'
Rabbit(exchange_name, 'payment_reserve_queue', Rabbit.payment_reserve)
Rabbit(exchange_name, 'payment_reserve_cancell_queue', Rabbit.payment_reserve_cancell)    

# request jwt public key
rsa_singleton.request_public_key()

app.app_context().push()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=17000)
=======
from application import create_app
from application.event_handler import Rabbit

app = create_app()

exchange_name = 'payment_exchange'
Rabbit(exchange_name, 'payment_reserve_queue', Rabbit.payment_reserve)
Rabbit(exchange_name, 'payment_reserve_cancell_queue', Rabbit.payment_reserve_cancell)    

app.app_context().push()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=17000)
>>>>>>> f7c5b0da40c8339f5130b3a81aa2cb5e619a6882
