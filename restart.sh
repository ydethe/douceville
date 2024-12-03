#! /bin/sh


rm -f *.whl *.log
pdm build
cp dist/*.whl .
pdm export --prod -o requirements.txt
# sudo docker build -t douceville:latest --no-cache .
# sudo docker tag douceville:latest ydethe/douceville:latest
# sudo docker push ydethe/douceville:latest
sudo docker compose -f docker-compose.dev.yml stop
sudo docker compose -f docker-compose.dev.yml up --build --remove-orphans -d
sudo docker compose -f docker-compose.dev.yml logs -f douceville-web-1
# sudo docker compose -f docker-compose.yml stop
# sudo docker compose -f docker-compose.yml up --build --remove-orphans -d
# sudo docker compose -f docker-compose.yml logs -f

# rm -f *.whl requirements.txt
