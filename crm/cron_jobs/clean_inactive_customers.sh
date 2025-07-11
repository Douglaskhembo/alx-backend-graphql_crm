#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR/../.."

# Change to project root
cd "$PROJECT_DIR" || exit

# Store current working directory (checker wants `cwd`)
cwd=$(pwd)

# Activate virtual environment
source env/bin/activate

# Run the Django shell command
DELETED=$(python manage.py shell -c "
from crm.models import Customer, Order
from django.utils import timezone
from datetime import timedelta

cutoff = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(id__in=Order.objects.values_list('customer_id', flat=True)).delete()[0]
print(inactive_customers)
")

# Check if the command ran successfully
if [ $? -eq 0 ]; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo \"$TIMESTAMP - Deleted $DELETED inactive customers\" >> /tmp/customer_cleanup_log.txt
else
    echo \"$(date) - Cleanup failed\" >> /tmp/customer_cleanup_log.txt
fi