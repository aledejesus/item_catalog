# Full Stack Web Developer Nanodegree
## Project 2: Item Catalog
### Description
This web application is a catalog that classifies items based on their category. Users can browse all the items and categories without being logged in. However, in order to create, modify or delete items a user has to log in using a Google account. Even when logged in, users can only modify and delete the items that were created by themselves.

### How to run?
#### With Vagrant
This is the recommended method to run the app as it takes care of most of the job for you. To run the app using vagrant, follow these steps:
 1. `git clone https://github.com/aledejesus/item_catalog.git`
 2. In project's directory run:
	 1. `vagrant up --provision`
	 2. `vagrant ssh`
 3. Inside the virtual machine, run:
	 1. `cd /vagrant`
	 2. `flask run`

After this, application should be accessible via http://localhost:5000. Vagrant provision SHELL takes care of installing the required packages in the virtual machine, creating the .env file necessary to run the app and creating the PostgreSQL role and database the app will use.

Also, sample data is inserted in the database as part of the aforementioned vagrant provision so some categories and items will be shown on the site from the start.

#### Without Vagrant
In case you don't want to use vagrant to run the app, follow these steps:
 1. `git clone https://github.com/aledejesus/item_catalog.git`
 2.  Install (if not already installed):
	 1. postgresql
	 2. python3.5
	 3. python3-pip
 3. Create a virtual environment with python3.5
 4. Activate the virtual environment created in the previous step
 5. Use pip to install all the packages in requirements.txt
 6. Duplicate the .env_example file and rename it .env
 7. Using postgres user, run sql/create_user.sql
 8. Using the vagrant PostgreSQL role created in the previous step, create a database called "catalog"
 9. Run flask migrations by typing `flask db upgrade`
 10. Using the vagrant PostgreSQL role created in step 7, run sql/dump_test.sql. This inserts sample data to the database so this step is optional.
 11. Change directory to the project's main directory (if not already there)
 12. Type `flask run` to start the app

After this, application should be accessible via http://localhost:5000. For concrete commands on how to run the previous steps in an Ubuntu machine, refer to the SHELL provision in the project's Vagrantfile.

### Environment Variables
All environment variables needed to run the project are in the .env_example file. All the variables are used either to run the app by python dotenv or to configure it by python decouple. If you need more details about these, feel free to check the aforementioned file.

Bear in mind that if you are running the project with vagrant, the .env_example file is automatically copied to a .env file. Project does not need any modification to this file to run.