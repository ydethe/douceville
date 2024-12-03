#! /bin/sh


rm -f *.whl *.log

pdm build
cp dist/*.whl .
pdm export --prod -o requirements.txt

sudo docker build -t douceville:latest --no-cache .
sudo docker tag douceville:latest ydethe/douceville:latest
sudo docker push ydethe/douceville:latest

# rm -f *.whl requirements.txt
