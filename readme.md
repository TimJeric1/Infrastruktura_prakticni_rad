ova implementacija je bazirana na ovom guideu: https://developer.redis.com/howtos/solutions/caching-architecture/write-through

komande za testiranje redisa

pip install gears-cli

sudo -S rm -rf ./master/data/* docker compose build docker compose up -d

""Redoslijed je bitan (iz nepoznatog razloga)"" gears-cli run --host localhost --port 6379 products_write_through.py --requirements requirements.txt gears-cli run --host localhost --port 6379 categories_write_through.py --requirements requirements.txt gears-cli run --host localhost --port 6379 users_write_through.py --requirements requirements.txt

python generate_data_replicated.py

curl -H "Host:master.localhost" http://localhost/api/read-users

curl -H "Host:dujetim.test" http://localhost/express/read-users

za provjeravanje syncanja s mysql bazom

docker exec -it <container_id_or_name> /bin/bash mysql -u root -p 111 USE mydb; SELECT * FROM users; SELECT * FROM products; SELECT * FROM categories;
