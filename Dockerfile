FROM python:3.8.2
RUN mkdir /project/
WORKDIR /project/
RUN git clone https://github.com/Arnacels/crmitlight.git .
RUN git pull origin master
RUN pip install -r requirements.txt
RUN mkdir sf
RUN echo "sht7vlw4" > sf/salt
RUN echo "n!s$@r)sorp27ui76ijigznkc$xkj--)2bp0mba-ck3qd0_w_m" > sf/sk
RUN python manage.py makemigrations shop
RUN python manage.py migrate
RUN python manage.py loaddata fixtures/data.json