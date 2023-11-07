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

papi = PassworkAPI(url='https://passwork.domain.name', key='foobar')
passwords = papi.passwords.search('Some_password')
print(passwords)
[Password(name='Some_password')]
password = passwords[0]
dir(password)
['__annotations__', '__class__', '__dataclass_fields__', '__dataclass_params__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__match_args__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'access', 'access_code', 'as_dict', 'attachments', 'color', 'description', 'encrypted_password', 'id', 'is_favorite', 'login', 'name', 'password', 'path', 'tags', 'url', 'vault_id']
print(password.name)
Some_password
print(password.encrypted_password)
abcxyzfoobar=
print(password.password)
P@ssw0rd
```
