#! /bin/sh


rm -f *.whl *.log
pdm build
cp dist/*.whl .
pdm export --prod -o requirements.txt
sudo docker compose -f docker-compose.dev.yml -p dvtest stop
sudo docker compose -f docker-compose.dev.yml -p dvtest up --build --remove-orphans -d
sudo docker compose -f docker-compose.dev.yml -p dvtest logs -f

rm -f *.whl requirements.txt
