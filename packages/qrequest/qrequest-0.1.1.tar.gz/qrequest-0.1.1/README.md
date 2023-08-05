qrequest
========

Instantly create an API and web interface for SQL queries.

# Basic Setup

1. Write SQL queries to collect the data users can access. Use :keywords for parameters.
2. Run `python qrequest.py setup` to get an sql folder to put your queries and default settings file 
2. Put these queries in the sql/main directory
3. Modify the settings below to specify the database driver (name of the python module) and databsae connection string
4. Then run `python qrequest.py run` to get a website which lets users run any of your queries without installing a thing, as well as an API endpoint.

The settings file looks like this. You can change the website title, description and the port the site runs on
```
{
    "sites": {
        "main": {
            "db_connection_string": "<database connection string>",
            "db_driver": "<python module name>"
        }
    },
    "website_description": "Run some queries",
    "website_port_number": 5000,
    "website_title": "qRequest"
}
```

Users can view queries through the web interface, and download the json or csv formatted query results.

The URL format for the json endpoint is
```
/api/{site_name}/{query_name}.json?{params}
```

The URL format for the CSV endpoint is
```
/api/{site_name}/{query_name}.csv?{params}
``` 

As an example, if you have a query called example_query.sql with two parameters (param1 and param2),
to run the query with param1=1234 and param2="string", go to
```
/api/main/example_query.sql.csv?param1=1234&param2=string
```

# Multiple Sites

qrequest supports multiple database connections, which are called sites.
To setup qrequest for multiple sites, pass all the site names as arguments to the
`setup` command. If none are passed, one site called `main` is created by default.

As an example, to setup two sites called `site1` and `site2` run

```
python qrequest.py setup site1 site2
```

This will generate the following settings file

```
{
    "sites": {
        "site1": {
            "db_connection_string": "<database connection string>",
            "db_driver": "<python module name>"
        },
        "site2": {
            "db_connection_string": "<database connection string>",
            "db_driver": "<python module name>"
        }
    },
    "website_description": "Run some queries",
    "website_port_number": 5000,
    "website_title": "qRequest"
}
```

You can specify different connection strings and database drivers for each site.


