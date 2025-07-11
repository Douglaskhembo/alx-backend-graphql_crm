#!/bin/bash

cd /ALX/Pro/Backend/alx-backend-graphql_crm
source env/bin/activate

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DELETED=$(python3 manage.py shell -c "
from crm.models import Customer, Order
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(id__in=Order.objects.values_list('customer_id', flat=True).distinct()).delete()[0]
print(inactive_customers)
")
echo "$TIMESTAMP - Deleted $DELETED inactive customers" >> /tmp/customer_cleanup_log.txt
