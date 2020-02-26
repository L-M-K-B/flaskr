# bookshelf app

###Base URL
```
http://127.0.0.1:5000/books
```

###My API ...
- is organised around REST
- accepts JSON-encoded request bodies
- returns JSON-encoded responses
- uses standard HTTP response codes

###Errors
In order to indicate success or failure of an API request this API uses conventional HTTP response codes.

####HTTP Status Code Summary
```
200 - everything worked well
400 - bad request
404 - resource not found 
405 - method not allowed
422 - unprocessable
```
####Example
```
curl -X POST -H "Content-Type: application/json" -d '{"search_term":"xyzwrtghfr"}' http://127.0.0.1:5000/books/search
```
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```
###Endpoints

For all available data. View is paginated. Available request: GET, POST
```
http://127.0.0.1:5000/books
```

For specific books. Available requests: GET, PATCH, DELETE
```
http://127.0.0.1:5000/books/<id>
```

For searching a book title. Available request: POST
```
http://127.0.0.1:5000/books/search
```