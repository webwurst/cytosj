
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

test-pypy2:
	docker pull pypy:2-slim
	docker build -t cytosj-testing-pypy:2 -f testing/Dockerfile_pypy_2 ./
	docker run --rm -ti cytosj-testing-pypy:2

test-pypy3:
	docker pull pypy:3-slim
	docker build -t cytosj-testing-pypy:3 -f testing/Dockerfile_pypy_3 ./
	docker run --rm -ti cytosj-testing-pypy:3

test: test-27 test-33 test-34 test-pypy2 test-pypy3

clean-test:
	docker rmi cytosj-testing:2.7
	docker rmi cytosj-testing:3.3
	docker rmi cytosj-testing:3.4
	docker rmi cytosj-testing-pypy:2
	docker rmi cytosj-testing-pypy:3
