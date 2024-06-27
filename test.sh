#!/bin/bash

# Run tests with coverage
pytest --cov=app tests/

# Generate coverage report
coverage report -m
coverage html
