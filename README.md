# orff_book_search

## elb config notes

Using a python ami in an elastic beanstalk deploy, the app gets copied to `/var/app/current`,

a virtualenv is created in `/var/app` and the file `/etc/systemd/system/web.service` configures the service (see example [here](./service_script/web.service))
