
test-27:
	docker pull python:2.7-slim
	docker build -t cytosj-testing:2.7 -f testing/Dockerfile_python_2.7 ./
	docker run --rm -ti cytosj-testing:2.7

test-33:
	docker pull python:3.3-slim
	docker build -t cytosj-testing:3.3 -f testing/Dockerfile_python_3.3 ./
	docker run --rm -ti cytosj-testing:3.3


test-34:
	docker pull python:3.4-slim
	docker build -t cytosj-testing:3.4 -f testing/Dockerfile_python_3.4 ./
	docker run --rm -ti cytosj-testing:3.4

test: test-27 test-33 test-34

clean-test:
	docker rmi cytosj-testing:2.7
	docker rmi cytosj-testing:3.3
	docker rmi cytosj-testing:3.4
