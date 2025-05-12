**Introduction:**
This project is designed to get started with Python networking by implementing a simple TCP socket client that communicates with a local server. The server challenges the client with a set of mathematical questions. After correctly answering all questions, the server returns a unique flag for each user.
**Requirements:**
Python 3.x
Java Runtime Environment (JRE) 1.8
Unix-like environment
  macOS / Linux: Built-in Terminal
  Windows: Use WSL or Linux VM (recommended)
**How to run the Server?**
PythonProject.jar and Python script (e.g., client.py) are in the same directory
Port 8888 is available (not used by other applications)
**Run the server:**
java -jar PythonProject.jar client.py
1. The server listens on port 8888
2. If no connection is made within 10 seconds, the server will terminate with a "Socket Time Out" message
3. Restart the server each time you modify your client script to get a new flag
**Server Communication protocol**:
1. Welcome message: Upon connecting, the server will send: "Hello there!"
2. Say Hello: HELLO <Husky name>
3. Receive and Solve Math problems
4. Receive Final Flag
**NOTE:**
Always restart the Python server once you have modified the client Python code.


