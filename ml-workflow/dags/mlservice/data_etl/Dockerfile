FROM ubuntu

MAINTAINER Prakritidevverma@arxivoverload.com 

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.6 \
    python-pip  \
    sudo apt-get install -y git

RUN pip install --upgrade pip && pip install awscli

RUN git clone https://github.com/arxivoverload-datascience/data.git && cd data/data

RUN pip install requirements.txt

RUN mkdir PDF references text 

CMD ["python" "~/pdftotext/pdftotext.py"]



