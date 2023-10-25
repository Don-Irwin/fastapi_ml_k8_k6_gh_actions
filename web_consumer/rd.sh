#!/bin/bash
rm *.db
gunicorn --bind 0.0.0.0:5000 app:app --threads 20
