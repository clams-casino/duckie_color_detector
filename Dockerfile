FROM duckietown/dt-duckiebot-interface:daffy-arm32v7

WORKDIR /color_detector

COPY dependencies-py3.txt ./
copy dependencies-apt.txt ./

RUN pip install -r dependencies-py3.txt
RUN dt-apt-install dependencies-apt.txt

COPY color_detector.py .

CMD python3 ./color_detector.py