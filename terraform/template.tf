resource "aws_ses_template" "mail_template" {
  name    = "${var.prefix}-html-checker-template"
  subject = "Change detected at {{url}}"
  html    = "<h1>Hello</h1><p>An HTML change has been detected at <a href=\"{{url}}\">{{url}}</a>.</p>"
  text    = "Hello ,\r\nAn HTML change has been detected at {{url}}."
}
