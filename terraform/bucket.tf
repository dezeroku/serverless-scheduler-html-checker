resource "aws_s3_bucket" "state_bucket" {
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "state_bucket" {
  bucket = aws_s3_bucket.state_bucket.id

  block_public_acls   = true
  block_public_policy = true
}
