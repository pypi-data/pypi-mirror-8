qjson
=====

quick and dirty way to convert json string to python object.

# install

just copy the qjson.py to your project.

#usage

```python
import qjson

json_str = '{"person":\
    {"name":"jerry", "age":32, "web":{"url":"http://jatsz.org", "desc":"blog"}}, \
    "grade": "a", "score":[80,90]}'

info = qjson.loads(json_str)

assert info.person.name == "jerry"
assert info.grade == "a"
assert info.score == [80, 90]
```


