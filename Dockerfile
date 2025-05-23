# Use imagem oficial do Python
FROM python:3.11-slim

# Crie diretório de trabalho
WORKDIR /app

# Instale dependências do sistema (opcional, para fontes/ssl etc)
RUN apt-get update && apt-get install -y gcc

# Copie requirements.txt (caso exista, veja o passo 2)
COPY requirements.txt .

# Instale dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie seu app
COPY . .

# Exponha a porta (padrão Streamlit: 8501)
EXPOSE 8501

# Comando para rodar o Streamlit ouvindo em 0.0.0.0
CMD ["streamlit", "run", "seu_app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.baseUrlPath=/streamlit"]
