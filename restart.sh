#! /bin/sh

rm -f *.whl *.log
pdm build
cp dist/*.whl .
pdm export --prod -o requirements.txt
sudo docker compose -f docker-compose.dev.yml up --build --remove-orphans -d
sudo docker compose -f docker-compose.dev.yml logs -f
