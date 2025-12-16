#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USERNAME

sudo docker run -d --name slm-poc -p 80:80 vvasylkovskyi1/vvasylkovskyi-slm-poc:${docker_image_tag}