# Duke University CompSci 516 Standard Course Project

> Team Name: PentaDevil

> Team Member: Shanghui Yin, Qingqian Wang, Yunze Zhang, Yilin Yang, Han Li

## More will be edited in milestone 4


## Running/Stopping the Website

To run your website, in your container shell, go into the repository
directory and issue the following commands:
```
poetry shell
flask run
```

The first command ensures that you are in the correct Python virtual
environment managed by a tool called `poetry` (you can tell that your
command-line prompt looks differently --- it would start with the name
of the environment).  The second command runs the Flask/web server.
Do NOT run Flask outside the `poetry` environment; you will get
errors.

You can now use your laptop's browser to explore the website.
Depending on your setup, the URL will be different:

* If you use containers on your own laptop, point your browser to
  http://localhost:8080/

* If you use the Duke OIT container, visit
  https://cmgr.oit.duke.edu/containers and open the CONTAINER CONTROLS
  info pane for your CS316/516 container.  There will be a line specifying
  a user-specific URL for accessing a Flask app.  Point your browser
  to that URL.

To stop your app, type <kbd>CTRL</kbd>-<kbd>C</kbd> in the container
shell; that will take you back to the command-line prompt, still
inside the `poetry` environment. If you are all done with this app for
now, you can type `exit` to get out of the `poetry` environment and
get back to the normal container shell.

## Working with the Database

Your Flask server interacts with a PostgreSQL database called `amazon`
behind the scene.  As part of the installation procedure above, this
database has been created automatically for you.  You can access the
database directly by running the command `psql amazon` in your VM.

For debugging, you can access the database while the Flask server is
running.  We recommend you open a second container shell to run `psql
amazon`.  After you perform some action on the website, you run a
query inside `psql` to see the action has the intended effect on the
database.

The `db/` subdirectory of this repository contains files useful for
(re-)initializing the database if needed.  To (re-)initialize the
database, first make sure that you are NOT running your Flask server
or any `psql` sessions; then, from your repository directory, run
`db/setup.sh`.


* If you get `ERROR: database "amazon" is being accessed by other
  users`, that means you likely have Flask or another `psql` still
  running; terminate them and re-run `db/setup.sh`.  If you cannot
  seem to find where you are running them, a sure way to get rid of
  them is to stop/start your container.

To change the database schema, modify `db/create.sql` and
`db/load.sql` as needed.  Make sure you run `db/setup.sh` to reflect
the changes.

Under `db/data/`, you will find CSV files that `db/load.sql` uses to
initialize the database contents when you run `db/setup.sh`.  Under
`db/generated/`, you will find alternate CSV files that will be used
to initialize a bigger database instance when you run `db/setup.sh
generated`; these files are automatically generated by running a
script (which you can re-run by going inside `db/data/generated/` and
running `python gen.py`.

* Note that PostgreSQL does NOT store data inside these CSV files; it
  store data on disk files using an efficient, binary format.  In
  other words, if you change your database contents through your
  website or through `psql`, you will NOT see these changes reflected
  in these CSV files (but you can see them through `psql amazon`).

* For safety, a database should never store password in plain text;
  instead it stores one-way hash of the password.  This rule applies
  to the password value in the CSV files too.  To see what hashed
  password value you should put in a CSV file, see `db/data/gen.py`
  for example of how to compute the hashed value.

## Note on Hiding Credentials

Use the file `.flaskenv` for passwords/secret keys --- we are talking
about passwords used to access your database server, for example (not
user passwords for your website in CSV files for loading sample
database).  This file is NOT tracked by `git` and it was automatically
generated when you first ran `./install.sh`.  Don't check it into
`git` because your credentials would be exposed to everybody on GitLab
if you are not careful.


## Acknowledgement

Originally created by [Rickard
Stureborg](http://www.rickard.stureborg.com) and [Yihao
Hu](https://www.linkedin.com/in/yihaoh/) for Fall 2021.  Amended by
various teaching staff in subsequent years.