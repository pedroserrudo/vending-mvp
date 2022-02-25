# Vending Machine Challenge
## Compatibility
- Python: 3.9
- Django: 4.x

## Quickstart

Setting up an Environment
```bash
pip install -U virtualenvwrapper
mkvirtualenv venv
workon venv
```

Installing
```bash
git clone git@github.com:xxxx/xxx.git[<directory>]
cd path/to/repository
```

## Running
call manage.py [command] from anywhere with the virtualenv activated
run migrations
```bash
python manage.py migrate
```

```bash
manage.py runserver 8000
```

## Tests
```bash
python manage.py test
```
---
## API Endpoits
### Auth
`/api/v1/auth/login/` - Login <br/>
`/api/v1/auth/logout/` - Logout <br/>
`/api/v1/auth/logout-all/` - Logout All <br/>
<br/>
### User
`/api/v1/users/` - Create, List Users <br/>
`/api/v1/users/<id>/` - Update, View, Delete Users <br/>
<br/>
### Buyer Wallet 
`/api/v1/wallet/deposit` - Wallet Deposit Coins <br/>
`/api/v1/wallet/balance` - Wallet Balance <br/>
`/api/v1/wallet/reset` - Wallet Balance Reset <br/>
<br/>
### Product
`/api/v1/product/` - Create, List Products <br/>
`/api/v1/product/<id>/` - View, Update, Delete Porduct <br/>


--- 

### Exercise Brief
Design an API for a vending machine, allowing users with a “seller” role to add, update or remove products, while users with a “buyer” role can deposit coins into the machine and make purchases. Your vending machine should only accept 5, 10, 20, 50 and 100 cent coins

###
#### Tasks
- REST API should be implemented consuming and producing “application/json”
- Implement product model with amountAvailable, cost, productName and sellerId fields
- Implement user model with username, password, deposit and role fields
- Implement an authentication method (basic, oAuth, JWT or something else, the choice is yours)
- All of the endpoints should be authenticated unless stated otherwise
- Implement CRUD for users (POST /user should not require authentication to allow new user registration)
- Implement CRUD for a product model (GET can be called by anyone, while POST, PUT and DELETE can be called only by the seller user who created the product)
- Implement /deposit endpoint so users with a “buyer” role can deposit only 5, 10, 20, 50 and 100 cent coins into their vending machine account
- Implement /buy endpoint (accepts productId, amount of products) so users with a “buyer” role can buy products with the money they’ve deposited. API should return total they’ve spent, products they’ve purchased and their change if there’s any (in an array of 5, 10, 20, 50 and 100 cent coins)
- Implement /reset endpoint so users with a “buyer” role can reset their deposit back to 0
- Create web interface for interaction with the API, design choices are left to you
- Take time to think about possible edge cases and access issues that should be solved

###
#### Evaluation criteria:
- Language/Framework of choice best practices
- Edge cases covered
- Write tests for /deposit, /buy and one CRUD endpoint of your choice Code readability and optimization

###
#### Bonus:
- If somebody is already logged in with the same credentials, the user should be given a message "There is already an active session using your account". In this case the user should be able to terminate all the active sessions on their account via an endpoint i.e. /logout/all
- Attention to security
###
#### Deliverables
A Github repository with public access. Please have the solution running on your computer so the domain expert can tell you which tests to run. Please have a Postman collection ready on your computer so the domain expert can tell you what tests to run on the API.

---