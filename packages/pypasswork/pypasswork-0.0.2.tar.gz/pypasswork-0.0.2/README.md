# Passwork python library
Library to interract with PassworkAPI with Python.

# Description
The library helps you to make requests to Passwork within your code using.
In current 0.0.1 version it can just find a password by name.

# Dependencies
* Python 3.10+
* requests 2.30.0+

# Examples
```python
from pypasswork import PassworkAPI

papi = PassworkAPI(url='https://passwork.domain.name', key='foobar', vault_name='Some vault')
password = papi.search_password('password_name')
print(password)
P@ssword
```
