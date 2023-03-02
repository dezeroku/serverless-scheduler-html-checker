# serverless-scheduler HTML checker

This repo provides a plugin to [serverless-scheduler](https://github.com/dezeroku/serverless-scheduler) project
that's meant to consume 'html_monitor_job' events.

The general concept for the plugin is to:

1. Obtain an HTML code for the provided `url`
2. Compare it with the previous HTML code (stored in S3) if it exists, otherwise just save it to S3.
3. If the state differs from the previous HTML code, an email is sent to `user_email` describing the difference.
   Then the new state is written to S3.

This project is meant to be run and built as a subdirectory in the `serverless-scheduler/plugins`.
It's currently added there as a submodule.
Especially the `bin/package_lambda_entrypoint` strictly relies on the `common` package's build system.
