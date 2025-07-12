# CRM Celery Setup

## Requirements
- Python 3.12+
- Redis running locally at `redis://localhost:6379/0`

## Setup Instructions

1. **Install Redis**
   Make sure Redis is installed and running locally:
   ```bash
   sudo apt update
   sudo apt install redis
   sudo systemctl start redis
   sudo systemctl enable redis
