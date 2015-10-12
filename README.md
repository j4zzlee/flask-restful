# flask-restful

* View docker-machine ip: 
> docker-machine ls
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM
default   *        virtualbox   Running   tcp://192.168.99.100:2376   

* Download mysql: 
> docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=<my-secret-pw> -d mysql
> docker run -p 5000:80 --link some-mysql:mysql -d st2forget/flask-restful

* Database Migrations:
> python migrations.py db revision --autogenerate -m 'Your message goes here' --version-path '1.0'
> OR: python migrations.py db migrate
* Go to the site (http://192.168.99.100:5000). Enjoy!!!

