variable "ami_id" {
  description = "The AMI ID to use for the web instance"
  type = string
  default = "ami-08c40ec9ead489470"
}

variable "instance_type" {
    description = "The type of web instance to launch"
    type = string
    default = "t2.medium"
}