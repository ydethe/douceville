#! /bin/sh


rm -f *.whl *.log
uv build
cp dist/*.whl .
uv export --no-editable --no-emit-project -o requirements.txt
sudo docker compose -f docker-compose.dev.yml -p dvtest stop
sudo docker compose -f docker-compose.dev.yml -p dvtest up --build --remove-orphans -d
sudo docker compose -f docker-compose.dev.yml -p dvtest logs -f

rm -f *.whl requirements.txt
