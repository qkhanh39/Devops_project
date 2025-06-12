resource "aws_instance" "web" {
  ami = var.ami_id
  instance_type = var.instance_type
  key_name  = aws_key_pair.key_pair_for_web_instance.key_name
  vpc_security_group_ids = [aws_security_group.Jenkins-VM-SG.id]
  user_data = templatefile("./install.sh", {})
  tags = {
    Name = "MicroInstance"
  }
  root_block_device {
    volume_size = 40
  }
}

resource "aws_key_pair" "key_pair_for_web_instance" {
  key_name = "my_key_pair"
  public_key = file("my_key_pair.pem.pub")
}


resource "aws_security_group" "Jenkins-VM-SG" {
  name        = "Jenkins-VM-SG"
  description = "Allow TLS inbound traffic"

  ingress = [
    for port in [22, 80, 443, 8080, 9000, 3000] : {
      description      = "inbound rules"
      from_port        = port
      to_port          = port
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      security_groups  = []
      self             = false
    }
  ]

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Jenkins-VM-SG"
  }
}