# Sample Flask App

## Problem

Write a sample backend application for an online marketplace. Here is a sample of some of the products available on
the site.

| Product code | Name                   | Price  |
|--------------|------------------------|--------|
| 001          |  Lavender heart        | £9.25  |
| 002          | Personalised cufflinks | £45.00 |
| 003          | Kids T-shirt           | £19.95 |

Create a RESTful API to implement CRUD operations on this data. The following endpoints should be provided:

- GET /products – A list of products, names, and prices in JSON format.
- POST /product – Create a new product using posted form data
- GET /product/{product_id} – Return a single product in JSON format.
- PUT /product/{product_id} – Update a product’s name or price by id.
- DELETE /product/{product_id} – Delete a product by id.

The service should be implemented in Python 3 using the Flask framework. Make sure that there are sensible return values
for both successful and unsuccessful requests (e.g. the server should report a code such as 404 for an unknown product ID
and not error out). Use and implement a database, though the technology you use is your choice; you may also use any 
publicly-available (i.e. pip installable) Flask extensions you like (ORMs, API helpers, etc).


## Solution

The solution has been implemented in `python3.5` and it's guaranteed to work on that python version. The project has 
been organized into two main folders. The `core` folder contains both the data model (`models.py`) and the implementation
of the API (`api.py`) while the folder `tests` contains the unit tests related to the endpoints exposed by the API. 
Finally the main of the program is located at the root level of the project (`main_app.py`) along with the default
configuration file `config.py`.

### Execution environment

It's strongly recommended to set up a virtual environment, install the requirements, and run the solution (both the main
application and the tests) within the `virtualenv`.

By using `virtualenvwrapper` this can be simply done with:

```$xslt
mkvirtualenv -a /path/to/this/project -p /path/to/your/python3 -r /path/to/this/project/requirements.txt sample-flask-app
```

You can even install the requirements at a later time by doing:

```$xslt
pip3 install -r /path/to/this/project/requirements.txt
```

### Running the program
   
Since the program connects to a `postgreSQL` database, in order to be able to connect to your own database you need to 
do just a few more set up operations. In `config.py`, defaults are provided for the development, testing, staging and 
productions environments. Switching between different environments is implemented via the `SAMPLE_FLASK_APP_ENV`
environment variable and the triggering values are:

- `dev` to refer to the development environment
- `test` to refer to the testing environment
- `stage` to refer to the staging environment
- `prod` to refer to the production environment

It's possible to overwrite defaults by providing an additional custom file with settings in the `SAMPLE_FLASK_APP_ENV`
environment variable. 

Let's say you want to execute this program in the `dev` mode:

1. Create a `dev_config.py` under the `.config` folder at the root level of the project.
2. Fill the `dev_config.py` with the settings you want to overwrite. For example, in my case this file contains:

   ```$xslt
    SQLALCHEMY_DATABASE_URI = 'postgresql://gioiaballin@localhost:5432/products'
   ```
   
3. Export the environment variable before running the app:

    ```$xslt
    export SAMPLE_FLASK_APP_ENV="dev"
    export SAMPLE_FLASK_APP_SETTINGS="./.config/dev_config.py"
    ```
    
4. Run the application from the root level of the project with:

    ```$xslt
    python3 main_app.py
    ```

_Aside note_: remember to add this project to your `PYTHONPATH` in order to avoid problems with import statements.

### Running the tests

In order to run the tests you still need to set the `SAMPLE_FLASK_APP_SETTINGS` in order to feed the tests with the right
URL of the testing database. Setting the `SAMPLE_FLASK_APP_ENV` is not needed because the tests already refers to the
testing default configuration.

If you want to execute the tests:

1. Create a `test_config.py` under the `.config` folder at the root level of the project.
2. Fill the `test_config.py` with the settings you want to overwrite. For example, in my case this file contains:

   ```$xslt
    SQLALCHEMY_DATABASE_URI = 'postgresql://gioiaballin@localhost:5432/test_products'
   ```

3. Run the tests from the root level of the project with:

    ```$xslt
    python -m unittest tests/test_api_endpoints.py
    ```

