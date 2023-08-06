#!/bin/bash
echo "Flushing DB..."
python manage.py flush --noinput
echo "Creating superuser with username 'admin'...";
python manage.py createsuperuser --username=admin --email=d@d.de;
echo "Creating example project data...";
python manage.py createexampledata;
echo "Finished. You're good to go! :-)";
