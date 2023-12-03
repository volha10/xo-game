## 1. How to run application 

```
docker-compose up
```
## 2. How to open Swagger
```
http://localhost:81/api/v1/docs
```
## 3. How to use

#### 3.1 Create user 1 
```
curl -X 'POST' \
  'http://localhost:81/api/v1/auth/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "email": "string",
  "password": "string"
}'
```
```
curl -X 'POST' \
  'http://localhost:81/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "string",
  "password": "string"
}'
```

#### 3.2 Create user 2
```
curl -X 'POST' \
  'http://localhost:81/api/v1/auth/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string2",
  "email": "string2",
  "password": "string"
}'
```
#### 3.3 Create game
```
curl -X 'POST' \
  'http://localhost:81/api/v1/games/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{
  "users": [
    {
      "id": 1,
      "mark": "X"
    },
    {
      "id": 2,
      "mark": "O"
    }
  ]
}'
```
#### 3.4 Make turn
```
curl -X 'PATCH' \
  'http://localhost:81/api/v1/games/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{
  "turn_number": 1,
  "mark": "X",
  "position": 1
}'
```

#### 3.5 Get board

```
curl -X 'GET' \
  'http://localhost:81/api/v1/games/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer TOKEN_HERE'
```


#### 3.6 Get user's games

```
curl -X 'GET' \
  'http://localhost:81/api/v1/games' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer TOKEN_HERE'
```


#### 3.7 Start new league season (new ranking table)

```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/management/leagues/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string"
}'
```


#### 3.8 Get current ranking table

```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/management/user-rating' \
  -H 'accept: application/json'
```