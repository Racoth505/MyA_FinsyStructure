#!/bin/bash

echo "Actualizando sistema..."
sudo apt update -y && sudo apt upgrade -y

echo "Instalando herramientas básicas..."
sudo apt install -y git vim curl
sudo apt install -y awscli

echo "Instalando Python y pip..."
sudo apt install -y python3 python3-pip

echo "Instalando Docker..."
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

echo "Instalando Boto3..."
pip3 install boto3

echo "Configuración completada"