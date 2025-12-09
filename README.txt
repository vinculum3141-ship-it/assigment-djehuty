
####################################################################################################
############### Assignment for Senior Software Developer Role – 4TU - Dev environment ##############
####################################################################################################

Hello! 

This readme contains instructions about how to run this dev environment.

To speed up the process, we are going to run the virtuoso database in a docker container environment and insert relevant
data for this assigment. This is why we are using a modification of the code that can be found in the GitHub Repository

Note that 'djehuty' folder contains same code when you clone https://github.com/4TUResearchData/djehuty. The exceptions
are: a ready to use config-file 'djehuty.xml', a transactions folder and modifications for docker setup.

Below are the same instructions you can find in the readme of our GitHub Repository. For djehuty installation you can
also check the instructions there. Make sure you skip the git clone step and use this ready-to-use directory.

#1 Djehuty installation

GNU/Linux
For development on GNU/Linux we recommend installing autoconf, automake and make through your system's package manager,
followed by creating a Python virtual environment for djehuty. WE use Python 3.12.3

$ cd djehuty
$ autoreconf -if && ./configure
$ python -m venv ../djehuty-env
$ . ../djehuty-env/bin/activate
$ pip install --upgrade pip
$ pip install --requirement requirements.txt
# pip install --editable .

Test if installation went well by typing:

$ djehuty --help

For macOS X or Microsoft Windows you can follow instructions as in the GitHub Repository as well (make sure you skip
the git clone step)

#2 - Once the Djehuty installation went well, start Virtuoso Docker container:

In the djehuty folder you are going to find the docker-compose.yaml. From there you can start the container.

$ cd djehuty
$ docker-compose up

sparql_1  | 15:28:29 HTTP/WebDAV server online at 8890
sparql_1  | 15:28:29 Server online at 1111 (pid 1)


When container is running you can access the sparql interface at http://localhost:8890/sparql.

#3 Inserting Data

We are going to apply transactions to insert data relevant for this assigment.
Within this djehuty folder, we are already provided a config-file for this assigment 'djehuty.xml'. Make sure you
use this configuration file.

$ cd djehuty
$ djehuty web --config-file=djehuty.xml --apply-transactions

Once is done, you can start the local djehuty environment by typing:

$ djehuty web --config-file=djehuty.xml

Now you can access djehuty web in http://localhost:8080/. The logs can be found in /logs/djehuty-web.log

TIP: useful link to explore the database:
http://localhost:8080/admin/exploratory

TIP2: you can switch from different accounts login by changing the property <automatic-login-email> in the config-file

Please reach me if you have any questions at gkuhn@tudelft.nl


######################################
############### // end ###############
######################################


