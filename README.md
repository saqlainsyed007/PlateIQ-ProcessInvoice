# PlateIQ-ProcessInvoice

# Setup Instructions

## Pyenv Setup(MacOS 10.9+)

#### Step 1: Install Pre-Requisites

```
brew install openssl readline sqlite3 xz zlib

export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
```

#### Step 2: Install pyenv

```
curl https://pyenv.run | bash
```

Add the following code to your `~/.bash_profile` file
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
This will load pyenv when a terminal is started

#### Step 3: Install Python 3.7.9

```
pyenv install -v 3.7.9
```
Here `-v` represents the python version. In our case it is `3.7.9`.
You could install different versions using the `-v` option.

#### Step 4: Create Virtual Environment

```
pyenv virtualenv 3.7.9 plateiq-3.7.9
```
The above command creates a virtual environment with name `plateiq-3.7.9` using python version `3.7.9`. You can choose a name that is preferable to you.

#### Step 5: Activate Virtual Environment

```
pyenv activate plateiq-3.7.9
```
Once the virtual environment that you created is activated, you can install the requirements and run the server. Once the work is completed you could deactivate your virtual environment using `pyenv deactivate`


## DB Setup

Using sqlite3 for this project to keep things simple.
```
brew install sqlite3
```

## Django Project Setup

#### Pre-Requisites

- Forked and cloned this repository.
- Navigate into cloned location.
- An activated virtual environment with python version 3.7.9

#### Step 1: Install requirements.

```
pip install -r requirements.txt
```

#### Step 2: Migrate

```
python manage.py migrate
```

#### Step 4: Create an admin user

```
python manage.py createsuperuser
```

#### Step 5: Runserver

```
python manage.py runserver 0:8000
```

## Testing the Application

#### Admin URL for viewing/creating Invoices
```
http://localhost:8000/admin/invoice/invoice/
```

#### Postman Collection for Testing the Invoice APIs.
```
https://www.getpostman.com/collections/a61edf4c3d97806da81e
```
