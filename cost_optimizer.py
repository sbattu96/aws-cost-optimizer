import boto3
import json
from datetime import datetime, timedelta

# Initialize AWS Cost Explorer Client
client = boto3.client("ce")

def get_aws_cost():
    try:
        # Get the first and last day of the previous month dynamically
        today = datetime.today()
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d")
        last_day_last_month = today.replace(day=1) - timedelta(days=1)
        last_day_last_month = last_day_last_month.strftime("%Y-%m-%d")

        # Fetch AWS cost data
        response = client.get_cost_and_usage(
            TimePeriod={"Start": first_day_last_month, "End": last_day_last_month},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"]
        )
        return response["ResultsByTime"]
    
    except Exception as e:
        print(f"Error fetching AWS cost data: {str(e)}")
        return None

# Run cost analysis
if __name__ == "__main__":
    cost_data = get_aws_cost()
    if cost_data:
        print(json.dumps(cost_data, indent=4))
    else:
        print("No data available or an error occurred.")
