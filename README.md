# Vending Machine Challenge


Compatibility
=============
- Python: 2.9
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

