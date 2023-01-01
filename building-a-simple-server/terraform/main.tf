# Variable file
variable "access_key" {
  description = "Access key for AWS account"
  default     = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
}

variable "secret_key" {
  description = "Secret key for AWS account"
  default     = "abcdefghijklmnopqrstuvwxyz1234567890"
}

variable "region" {
  description = "AWS region to use"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Type of EC2 instance to use"
  default     = "t2.micro"
}

variable "image_id" {
  description = "ID of the AMI to use"
  default     = "ami-0123456789abcdef"
}

variable "key_name" {
  description = "Name of the SSH key pair to use"
  default     = "my-key-pair"
}

# Output file
output "resources" {
  value = ["docker_image.website", "docker_container.website"]
}

provider "docker" {
  host = "tcp://localhost:2375"
}

resource "docker_image" "website" {
  name = "my-website"
  build = "."
  push = true
}

resource "docker_container" "website" {
  name  = "my-website-container"
  image = docker_image.website.latest
  ports {
    internal = 80
    external = 8080
  }
}
