rmdir "./migrations" -Force -Recurse
echo rm -R -f ./migrations
pipenv run init
mysql -u root -p -e "DROP DATABASE example;"
mysql -u root -p -e "CREATE DATABASE example;"
pipenv run migrate
pipenv run upgrade