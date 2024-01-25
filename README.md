## Prerequesites
Python
Docker


## Commands to run one by one (tested in fedora 39 linux):


```
docker network create traefik
```

```
./build.sh
pip install --no-cache-dir faker mysql-connector-python matplotlib
python generate_data_replicated.py
```

if you get permission denied just:
```
chmod +x <the_file_name>
```

in some other terminal run
```
python flaskapp.py
```
After that wait a few seconds for slave to catch up with data:
you can use to check if slave caught up:
```
docker exec -it mysql_slave mysql -uroot -p111
use mydb
select * from users;
exit
```
after that benchmark the performance with:
```
python measure_and_plot.py 
```

When you are done with measuring replicated_2_db:
```
docker-compose down
sudo rm -rf ./master/data/*
sudo rm -rf ./slave/data/*
ctrl-c in the flaskapp.py terminal to terminate the backend server
```
