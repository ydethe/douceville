#! /bin/sh


# sudo docker build -t douceville .
# sudo docker tag douceville:latest ydethe/douceville:latest
# sudo docker push ydethe/douceville:latest

rm -f *.whl *.log
pdm build
cp dist/*.whl .
pdm export --prod -o requirements.txt
sudo docker compose -f docker-compose.dev.yml stop
sudo docker compose -f docker-compose.dev.yml up --build --remove-orphans -d
sudo docker compose -f docker-compose.dev.yml logs -f
# sudo docker compose -f docker-compose.yml stop
# sudo docker compose -f docker-compose.yml up --build --remove-orphans -d
# sudo docker compose -f docker-compose.yml logs -f
