FROM circleci/python:2.7-browsers
ENV MTAF_SITE mm_ro_docker
ENV MTAF_DB_HOST 10.0.12.42
ENV PYTHONPATH /mtaf
WORKDIR /home/circleci/mtaf
RUN sudo apt-get update
RUN sudo apt-get install -y apt-utils
RUN sudo apt-get install -y libasound2-dev
RUN sudo apt-get install -y python-pip
RUN sudo apt-get install -y default-jre
COPY --chown=circleci:circleci . .
RUN sudo /bin/bash -c "cd /home/circleci/mtaf/package/mtaf; source build_script"
