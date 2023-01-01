import git
import os

# Clone the repository
repo = git.Repo.clone_from("https://github.com/jordanistan/iamjordanrobison/building-a-simple-server/", "./python")

# Create a Dockerfile
with open("./python/Dockerfile", "w") as f:
  f.write("FROM python:3.8\n")
  f.write("WORKDIR /app\n")
  f.write("COPY . .\n")
  f.write("RUN pip install -r requirements.txt\n")
  f.write("EXPOSE 8080\n")
  f.write("CMD [\"python\", \"app.py\"]\n")

# Build the Docker image
client = docker.DockerClient()
image, build_logs = client.images.build(path='./python', tag='web-app')

# Run the Docker image as a container
container = client.containers.run(image, ports={'8080/tcp': 8080}, detach=True)

# Print the logs from the container
print(container.logs())

# Open the website in a browser
import webbrowser
webbrowser.open("http://localhost:8080")

# Stop the container when the user is finished
input("Press enter to stop the container...")
container.stop()
