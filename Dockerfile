FROM python:3.9-alpine

WORKDIR /app
# Definindo variáveis de ambiente que serão usadas pela aplicação flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# instalando pacotes com o gerenciador do Alpine Linux
RUN apk add --no-cache gcc musl-dev linux-headers

# Iremos montar um volume e não copiar (COPY app/* .) o código para dentro da imagem.
# Isso permitirá alterar o código fonte do projeto sem a necessidade de alterar a imagem.
# copiando somente o arquivo requirements.txt

COPY requirements.txt requirements.txt
# instalando pacotes python
RUN pip install -r requirements.txt

CMD ["flask", "run"]