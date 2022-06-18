


## Description

This is a basic http server implementation for learning purpose

Server runs on **localhost** and listens port **8080** 

## Requests

- GET / isPrime
    - **Purpose** : Controling whether the number is prime
    - Expected parameter name : **number**
    - Expected value : **integer**
    ```
    http://localhost:8080/?number=5
    ```

- POST / upload
    - **Purpose** : Uploading a file from client to server

- PUT / rename
    - **Purpose** : Renaming the file located on the server
    - Expected parameter name : **oldFileName** & **newName**
    ```
    http://localhost:8080/?oldFileName=old.txt&newName=new.txt
    ```

- DELETE / remove
    - **Purpose** : Removing the file located on the server
    - Expected parameter name : **fileName** 
    ```
    http://localhost:8080/?fileName=new.txt
    ```

- GET / download
    - **Purpose** : Downloading the file from server to client
    - Expected parameter name : **fileName** 

## Run

```
python3 server.py
```
