data "aws_vpc" "selected" {
  default = true
}

resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow http inbound traffic"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow ssh inbound traffic"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["202.80.214.161/32"] # CHANGETHIS
  }
}

resource "aws_instance" "myweb" {
  ami           = "ami-0e763a959ec839f5e"
  instance_type = "t2.micro"
  user_data     = file("init-script.sh")
  tags = {
        Name = "ubuntu18.04"
        Description = "Managed by terraform"
  }
  lifecycle {
    ignore_changes = [
      tags, security_groups, vpc_security_group_ids, associate_public_ip_address
    ]
  }
  key_name = "training_fajri" #CHANGETHIS
  security_groups = [ "${aws_security_group.allow_http.name}", "${aws_security_group.allow_ssh.name}" ]
}

output "public_dns" {
  value = aws_instance.myweb.public_dns
}
output "public_ip" {
  value = aws_instance.myweb.public_ip
}