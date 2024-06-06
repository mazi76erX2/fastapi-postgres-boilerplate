#!/bin/bash

isort server/ --check-only
black server/ --check
blacken-docs README.md
blacken-docs --all-files