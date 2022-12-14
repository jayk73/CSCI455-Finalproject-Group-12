# CSCI455-Finalproject-Group-12

To run this project, there are a few things you need.
First, you need a windows computer with bluetooth capabilities.

Then you will need some software.

The Project Requires a python version of at least 3.10 (3.11 works as well.)
You will also need 2 python packages, PyBluez and PyQt5

To install PyBlues, run the following commands in the command prompt (you may need to run as an administrator):

>git clone https://github.com/pybluez/pybluez
>cd pybluez
>python setup.py install

(Directly using PIP install dosen't work for pybluez, for some reaason. This method will copy the directory from github and then run the setup file.)

PyBluez also has 2 software dependecies that you may already have, including the Windows 10 SDK (https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/) and a C++ compiler.

The details of the dependecies are listed here:
https://pybluez.readthedocs.io/en/latest/install.html

--------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------
To Install PyQt5, run the following command in the command line:

> pip install PyQt5


-------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

RUNNING THE PROJECT

Once every computer has the necessary software installed, make sure to enable bluetooth on each device.
(on Windows 10, search for bluetooth and other devices in the serch bar then enable bluetooth.)

On each computer, run the file main.py

For the host, click the button titled "Host Server". This will open the chatroom window. Now, wait for client connections.

For the client, click the button titled "Search for Nearby Devices". This will display all detected devices in the window on the right. After that, it will filter one by one based on whether they are currently running a server. You may select a devices at any time and click "Attempt connection to selected device". If succesfull, this will open the chatroom window

If the client connection is succesfull, the server will display a message saying that a client has connected (and send that message to all other clients). The server will also send a welcome message to each client. 
Once one or more clients are connected, the server and client's will be able to type messages to send to all other connected devices. 