FROM ubuntu:18.04

RUN apt update && apt -y upgrade

RUN apt update
RUN apt -y install sudo apache2 python3-pip
RUN pip3 install flask
COPY ./files/000-default.conf /etc/apache2/sites-available/000-default.conf
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install -y php php-sqlite3 php-curl
RUN a2dismod status

COPY ./files/entrypoint /entrypoint
RUN chmod +x /entrypoint
ENTRYPOINT ["/entrypoint"]

#RUN service apache2 reload
CMD ["/usr/sbin/apache2ctl", "-DFOREGROUND"]