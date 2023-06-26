# basic_cli_serv

## Description

This is a basic client-server application that uses TCP sockets to communicate. The client can send task to the server and the server will execute the task and send the result back to the client.

## Usage

You can launch the program by running the following commands:

- ./main.sh in the root of the project. (This will create the dynamic library)
- run the server by running the following command: python3 server.py
- run the client by running the following command: python3 client.py

If the command does not work, it's maybe because the .sh file is not executable. You can make it executable by running the following command:

- chmod +x main.sh

## Clean

You can clean the project by running the following command:

- ./clean.sh in the root of the project. (This will delete the dynamic library and the object files)