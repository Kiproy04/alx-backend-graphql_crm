#!/bin/bash

# Path to your Django project directory (update if needed)
PROJECT_DIR="/path/to/your/project"
PYTHON_BIN="/path/to/your/venv/bin/python"
MANAGE="$PROJECT_DIR/manage.py"

# Log file
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Run cleanup using Django shell
DELETED_COUNT=$($PYTHON_BIN $MANAGE shell << 'EOF'
from datetime import datetime, timedelta
from crm.models import Customer, Order

one_year_ago = datetime.now() - timedelta(days=365)

# Find customers with no orders in the last year
inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(
        created_at__gte=one_year_ago
    ).values_list('customer_id', flat=True)
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

# Write result to log with timestamp
echo "$(date +"%Y-%m-%d %H:%M:%S") - Deleted customers: $DELETED_COUNT" >> $LOG_FILE
