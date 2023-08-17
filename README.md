## **Prerequisites**

- python 3.9
- [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)
- mysql-server
  
## **Installation** 

- Install python packages.
```bash
pipenv sync 
```

- Create ``restaurant_supply_express`` database.
```console
mysql> source path/to/schema.sql;
```

- Add procedures to database.
```console 
mysql> source path/to/procedures.sql;
```

- Create ``secrets.toml`` by copying the ``secrets.toml.sample``and set the password of the mysql root user.
  
- Activate pipenv virtual environment.
```bash
pipenv shell 
```
- Start application.
```bash
streamlit run src/app.py
```

## **Dependencies**

### **[streamlit](https://streamlit.io/)**

Streamlit is a low-stake frontend tool, that requires not prior experience in frontend development.

### **[streamlit-book](https://github.com/sebastiandres/streamlit_book)**

Streamlit library that adds support for multiple layouts; in our case private and public layouts. The public layout is used for authentication and login; the private layouts are used to enforce role-based access control.

###  **[mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)**

Python package used to connect to mysql database and execute queries.

## **Acknowledgments**

[streamlit-book template](https://github.com/sebastiandres/template_streamlit_multipage)