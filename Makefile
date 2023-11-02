tag=latest
organization=joyw03
image=linkers_website

build:
	docker build --force-rm $(options) -t linkers_website .
# build docker image
build-prod:
# build only the production image
	$(MAKE) build options="--target production"

push:
	docker tag $(image):latest $(organization)/$(image):$(tag)
	docker push $(organization)/$(image):$(tag)

# command to start up our docker image
# remove files that from previous run that we don't need 
compose-start:
	docker-compose up --remove-orphans $(options)

# remove any networks or containers that were running
compose-stop:
	docker-compose down --remove-orphans $(options)

# can use this command to make migrations
compose-manage-py:
	docker-compose run --rm $(options) website python manage.py $(cmd)

create-superuser:
	docker-compose run --rm website python manage.py createsuperuser

start-server:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate

helm-deploy:
	helm upgrade --install linkers-website ./helm/linkers-website