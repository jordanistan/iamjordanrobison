<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Iamjordanrobison" />

  &#xa0;

  <!-- <a href="https://iamjordanrobison.netlify.app">Demo</a> -->
</div>

<h1 align="center">Iamjordanrobison</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/jordanistan/iamjordanrobison?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/jordanistan/iamjordanrobison?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/jordanistan/iamjordanrobison?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/jordanistan/iamjordanrobison?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/jordanistan/iamjordanrobison?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/jordanistan/iamjordanrobison?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/jordanistan/iamjordanrobison?color=56BEB8" /> -->
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Iamjordanrobison 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/jordanistan" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

Here is an example of a Dockerfile that can be used to build a container for a scalable website:


## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com) and [Docker](https://Docker.io) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/jordanistan/iamjordanrobison

# Access
$ cd iamjordanrobison

```

Dockerfile that can be used to build a container for a scaleable website:

```bash
FROM python:3.8

# Install the necessary libraries
RUN pip install flask

# Copy the web server code
COPY server.py .

# Run the web server
CMD ["gunicorn", "server:app", "-b", "0.0.0.0:80", "-w", "4"]
```

This Dockerfile installs the necessary libraries and runs a simple Flask web server using Gunicorn. Gunicorn is a WSGI HTTP server that is designed to be efficient and easy to use, and it is well-suited for running high-concurrency web applications.

The -b flag specifies the bind address and port that Gunicorn should listen on, and the -w flag specifies the number of worker processes to use. By default, Gunicorn uses a single worker process, but you can increase this number to handle more traffic.

To build the container, navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t hire-jordan
``` .
This will build a Docker image with the tag "hire-jordan" based on the instructions in the Dockerfile.

To run the container locally, use the following command:

```bash
docker run -p 8080:80 hire-jordan
```

This will start a container based on the "hire-jordan" image and bind the container's port 80 to the host machine's port 8080. You should then be able to access the website by visiting http://localhost:8080 in your web browser.

Note: Make sure that port 8080 on the host machine is not already in use by another process. If it is, you can choose a different host port by changing the first number in the -p flag (e.g. -p 8000:80).


## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/jordanistan" target="_blank">{{YOUR_NAME}}</a>

&#xa0;

<a href="#top">Back to top</a>
