# Full Stack Web Developer Nanodegree
## Project 2: Item Catalog
### Description
This web application is a catalog that classifies items based on their category. Users can browse all the items and categories without being logged in. However, in order to create, modify or delete items a user has to log in using a Google account. Even when logged in, users can only modify and delete the items that were created by themselves.

### How to run?
Vagrant is needed in order to easily run the web application locally. To do so, follow these steps:
 1. `git clone https://github.com/aledejesus/item_catalog.git`
 3. In project's directory run:
	 1. `vagrant up --provision`
	 2. `vagrant ssh`
 4. Inside the virtual machine, run:
	 1. `cd /vagrant`
	 2. `flask run`

After this, application should be accessible via http://localhost:5000. Sample data is inserted as part of the SHELL vagrant provision so there will be some categories and items already created from the first time the site is accessed.