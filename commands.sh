#!/bin/bash

find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +

echo "Every __pycache__ and .ipynb_checkpoints folders have been deleted."