#!/bin/bash
cd ~/django-forbid/
git restore .
git pull
sudo rm -r /var/www/docs/django-forbid/
cd ~/django-forbid/docs/ && npm install && npm run build
sudo cp -r ~/django-forbid/docs/.vitepress/dist/ /var/www/docs/django-forbid/
