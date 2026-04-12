To run in local
    docker compose up --build > output.txt

For Render deployment:

Set Build Command: npm ci
Set Start Command: npm start
Add environment variables in Render dashboard


Curl scripts for testing


Create order (from cart snapshot)

curl -X POST http://localhost:8086/orders \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "items": [
      { "product_id": 1, "quantity": 2, "price": 1000.00 },
      { "product_id": 2, "quantity": 1, "price": 500.00 }
    ]
  }'



Get own orders

curl -X GET http://localhost:8086/orders \
  -b cookies.txt



Get order detail (own)

curl -X GET http://localhost:8086/orders/3 \
  -b cookies.txt



Forbidden: user tries to update status

curl -X PUT http://localhost:8086/orders/1/status \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "status": "PAGADO"
  }'



Admin: get any order detail

curl -X GET http://localhost:8086/orders/1 \
  -b admin_cookies.txt



Admin: update order status 'PENDIENTE','PAGADO','ENVIADO','COMPLETADO','CANCELADO'

curl -X PUT http://localhost:8086/orders/1/status \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "status": "CANCELADO"
  }'



Missing token

curl -X GET http://localhost:8086/orders



Invalid order (not owner)

curl -X GET http://localhost:8086/orders/999 \
  -b cookies.txt



### Invalid status value

curl -X PUT http://localhost:8086/orders/1/status \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "status": "INVALID"
  }'

