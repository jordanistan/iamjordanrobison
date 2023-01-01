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

This script clones the repository to a local directory and creates a Dockerfile with instructions to build a container with the necessary dependencies and run the web application. It then builds the Docker image and runs the container, exposing port 5000 on the host machine. Finally, it opens the website in a browser and waits for the user to press enter to stop the container.

Note: This script assumes that the repository contains a file named requirements.txt with a list of the necessary Python packages, and a file named app.py with the code for the web application. It also assumes that the Docker Python library is installed.

## :checkered_flag: Starting ##


```bash
# To use the Python script to clone a Git repository and run the code locally in a browser:
# Make sure that you have the Docker Python library and GitPython library installed. You can install these libraries using pip:

pip install docker
pip install GitPython


# Clone this project
$ git clone https://github.com/jordanistan/iamjordanrobison/building-a-simple-server/python

# Run
cd repo

# Run the project
python hire-me.py


# The server will initialize in the <http://localhost:3000>
```
The script will clone the repository, create a Dockerfile, build a Docker image, and run a container based on the image. It will then open the website in a browser and wait for the user to press enter to stop the container.

This script is useful for quickly running and testing a web application locally without having to install the necessary dependencies manually. It can also be useful for deploying the application to a remote server or hosting platform.

Note: The script assumes that the repository contains a file named requirements.txt with a list of the necessary Python packages, and a file named app.py with the code for the web application. It also assumes that the Docker daemon is running on the host machine.

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/jordanistan" target="_blank">Jordan Robison</a>

&#xa0;

<a href="#top">Back to top</a>
