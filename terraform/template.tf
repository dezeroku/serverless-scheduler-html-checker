resource "aws_ses_template" "mail_template" {
  name    = "${var.prefix}-html-checker-template"
  subject = "Change detected at {{url}}"
  html    = <<EOT
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<meta http-equiv="Content-Type"
      content="text/html; charset=utf-8"/>
</head>
<body><h1>Hello</h1><p>An HTML change has been detected at <a href="{{url}}">{{url}}</a>.</p></br><p>See the (possibly shortened) diff below:</p></br>{{diff_html}}</body></html>"
    EOT
  text    = "Hello ,\r\nAn HTML change has been detected at {{url}}.\r\nDiff is shown below:\r\n{{diff_html}}"
}
