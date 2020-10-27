# Mini CRM 

    For start project use python 3.8.2:
    Docker
     - use 
`git clone https://github.com/Arnacels/crmitlight.git`

     - go to the project directory
     - use 
`docker-compose up -d --build`
     
     - go to https://127.0.0.1:8000/
     
     
    
    Without Docker
     - use 
`git clone https://github.com/Arnacels/crmitlight.git`

     - go to the project directory
     - in crm/settings.py change SECRET_KEY on "n!s$@r)sorp27ui76ijigznkc$xkj--)2bp0mba-ck3qd0_w_m"
     - in crm/settings.py change HASHID_FIELD_SALT on "sht7vlw4"
     - run 
`python -m venv venv`

     - if windows 
`venv/Scripts/activate`

     - if linux 
`source venv/bin/activate`

     - run 
`pip install -r requirements.txt`

     - run 
`python manage.py makemigrtaions shop`

`python manage.py migrate`

`python manage.py loaddata fixtures/data.json`

`python manage.py runserver`

     - go to https://127.0.0.1:8000/


**Use postman collection for test REST.**

#### Users:

    admin - ADMIN
    323232
    
    anna - Paymaster
    323232anna

    lina - Accountant
    323232anna

    yana - Shop Assistant
    323232anna



#### Api

###### Basic auth

    api/v1/login/
    POST
    username
    password

###### Product list
    
    api/v1/products/
    GET

###### Order list only Accountant
    
    api/v1/orders/
    GET
    params:
    from_date - time in timestamp
    to_date - time in timestamp

###### Order

    api/v1/order/<oder_id>/
    GET
    return JSON

###### Create order
    
    api/v1/create_order/
    POSt
    body:
    product - product id
    
    return JSON

###### Change status order

    api/v1/order/change_status/<oder_id>/
    PATCH
    body:
    status - (1,2,3)
    
     0 - Send order (No change)
    1 - Processing (Paymaster) return JSON
    2 - Done (Shop Assistant) return JSON
    3 - Payed (Paymaster) return HTML check
