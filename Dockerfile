FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get -y install python3-pip
RUN alias pip=pip3
RUN pip3 install torch torchvision torchaudio
RUN apt-get install -y curl git wget --fix-missing
RUN mkdir workspace
WORKDIR ./workspace
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install -r ./webui/requirements.txt

EXPOSE 7860

ENTRYPOINT ["gradio", "app.py"]
