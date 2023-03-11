# serverless-scheduler HTML checker

This repo provides a plugin to [serverless-scheduler](https://github.com/dezeroku/serverless-scheduler) project
that's meant to consume 'html_monitor_job' events.

# High Level Overview

![High Level Overview](docs/diagrams/created/high_level_overview.png?raw=true "High Level Overview")

The general concept for the plugin is to:

1. Obtain the HTML for the provided `url`
2. Compare it with the previous HTML code (stored in S3) if it exists, otherwise just save it to S3.
3. If the state differs from the previous HTML code, send an email to `user_email` describing the difference.
   Then the new state is written to S3.

# Requirements

1. It's assumed that SES identity for a domain is defined outside of this plugin

# Building

This project is meant to be run and built as a subdirectory in the `serverless-scheduler/plugins`.
It's currently added there as a submodule.
Especially the `bin/package_lambda_entrypoint` strictly relies on the `common` package's build system.
