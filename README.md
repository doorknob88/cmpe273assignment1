# cmpe273assignment1
use localhost:8000/ to access the server

1) Install redis
2) Install dependenies (redis, Flask, etc) with Pip

3) Start Server in a terminal with: `python3 app.py`

4) In another Terminal, make a post request with: `curl -i -X POST -H "Content-Type: multipart/form-data" -F "data=@foo.py" http://localhost:8000/api/v1/scripts`

![image](https://github.com/doorknob88/cmpe273assignment1/blob/master/temp/1.png)


as you can see an ID is generated here: 807ee3d6894a4500828efe3e1efe893f

copy this into the GET request after scripts to call it

`curl -i http://localhost:8000/api/v1/scripts/807ee3d6894a4500828efe3e1efe893f`

![](https://github.com/doorknob88/cmpe273assignment1/blob/master/temp/1.5.png)

Result:

![](https://github.com/doorknob88/cmpe273assignment1/blob/master/temp/2.png)
