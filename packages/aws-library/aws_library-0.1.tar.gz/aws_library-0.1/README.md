Certainly! Below is a template for a `README.md` file for your AWS utility library. You'll need to customize it with your own information, such as installation instructions, usage examples, and contact information. Save this content in a `README.md` file in the root of your project directory.

```markdown
# AWS Utility Library

This `aws_library` is a Python package that provides a simplified interface for interacting with various AWS services using `boto3`.

## Features

- Easy-to-use methods for common AWS operations.
- Handles S3 uploads/downloads, RDS queries, and triggering deployments for AWS CodeDeploy, CodeBuild, and CodePipeline.

## Installation

Install `aws_library` using pip:

```bash
pip install aws_library
```

## Usage

Here is how you can use the `aws_library`:

```python
from aws_library import AWSLibrary

# Create an instance of the library
aws_lib = AWSLibrary()

# Save data to an S3 bucket
aws_lib.save_to_s3('my-bucket', 'test/key', 'Some data')

# Get data from an S3 bucket
data = aws_lib.get_from_s3('my-bucket', 'test/key')
print(data)

# Execute a query on RDS
records = aws_lib.execute_query('my-database', 'SELECT * FROM my_table')
print(records)

# Trigger a deployment
deployment_success = aws_lib.trigger_deployment('my-app', 'my-deployment-group', {
    'revisionType': 'S3',
    's3Location': {
        'bucket': 'my-bucket',
        'key': 'builds/my-app.zip',
        'bundleType': 'zip'
    }
})
print(deployment_success)

# Start a build in CodeBuild
build_success = aws_lib.start_build('my-build-project', 'sourceVersion')
print(build_success)

# Get the state of a pipeline in CodePipeline
pipeline_state = aws_lib.get_pipeline_state('my-pipeline')
print(pipeline_state)
```

Replace `'my-bucket'`, `'my-database'`, `'my-app'`, etc., with your actual AWS resource names.

## Requirements

- Python 3.7+
- boto3

## Development

To contribute to this project, please fork the repository and submit a pull request.

## License

pypi-AgEIcHlwaS5vcmcCJDJlNGExYTcwLWYxNmYtNDI1Yi1iNzVhLTBhMTYxNmMzZGM4ZgACKlszLCJhNjViYWJiZi1lOTI2LTQ3NzMtOTMyNC1hZTcxOTdmNzFjZjAiXQAABiA30kNEkVPeM7cG3Jg9PGI9bI79qIGLreECTfjqpJlgjw

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please contact me at your.email@example.com.

## Acknowledgments

- Thanks to the `boto3` team for their excellent AWS SDK for Python.
```

In the `Usage` section, you can include examples of how to use your library. Make sure to provide enough information so that someone unfamiliar with your code can understand how to use it.

In the `Contact` section, put your actual contact email so users can reach out to you if they have questions or issues.

Remember to create a `LICENSE` file if you haven't already and to reference it correctly in the `README.md` file.