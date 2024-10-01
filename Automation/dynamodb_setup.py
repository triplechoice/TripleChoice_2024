import boto3
import pandas as pd
import numpy as np
from decimal import Decimal

# Create a local DynamoDB resource with a specified region
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')

# Define the table name
table_name = 'YourTableName'

# Delete the existing table if it exists
try:
    existing_table = dynamodb.Table(table_name)
    existing_table.delete()
    existing_table.wait_until_not_exists()
    print(f"Table {table_name} deleted successfully.")
except dynamodb.meta.client.exceptions.ResourceNotFoundException:
    print(f"Table {table_name} does not exist.")
except Exception as e:
    print(f"Error deleting table: {e}")

# Create a new table
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'Name',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print(f"Table {table_name} created successfully.")
except dynamodb.meta.client.exceptions.ResourceInUseException:
    print(f"Table {table_name} already exists.")
except Exception as e:
    print(f"Error creating table: {e}")

# Load your pump data into a DataFrame
pump_names = ['CM100', 'CM277', 'CM148', 'CM142', 'CM283']
pump_ids = [622015, 860592, 950667, 678864, 391886]
flow_head_data = [
    {0: Decimal('90.1'), 23: Decimal('90.53'), 38: Decimal('90.95'), 46.1: Decimal('91.03'), 69.1: Decimal('90.18'), 92.1: Decimal('86.96'), 115: Decimal('80.72'), 138: Decimal('71.1'), 161: Decimal('58')},
    {0: Decimal('85.1'), 23: Decimal('85.53'), 38: Decimal('85.95'), 46.1: Decimal('86.03'), 69.1: Decimal('85.18'), 92.1: Decimal('81.96'), 115: Decimal('75.72'), 138: Decimal('64.1'), 161: Decimal('50')},
    {0: Decimal('70.1'), 23: Decimal('80.53'), 38: Decimal('80.95'), 46.1: Decimal('81.03'), 69.1: Decimal('80.18'), 92.1: Decimal('76.96'), 115: Decimal('70.72'), 138: Decimal('60.1'), 161: Decimal('48')},
    {0: Decimal('75.0'), 23: Decimal('75.50'), 38: Decimal('75.95'), 46.1: Decimal('76.03'), 69.1: Decimal('75.18'), 92.1: Decimal('72.96'), 115: Decimal('65.72'), 138: Decimal('55.1'), 161: Decimal('43')},
    {0: Decimal('78.0'), 23: Decimal('78.50'), 38: Decimal('78.95'), 46.1: Decimal('79.03'), 69.1: Decimal('78.18'), 92.1: Decimal('74.96'), 115: Decimal('68.72'), 138: Decimal('57.1'), 161: Decimal('46')},
]

# Convert flow head data to the proper format
flow_head_data = [
    {str(key): str(value) for key, value in flow.items()}
    for flow in flow_head_data
]

df = pd.DataFrame({
    'Name': pump_names,
    'ID': pump_ids,
    'Flow Head Data': flow_head_data
})

# Add a new column for the fitted polynomial function
pump_curves = []

for index, row in df.iterrows():
    flow_rates = list(map(float, row['Flow Head Data'].keys()))
    heads = list(map(float, row['Flow Head Data'].values()))
    
    # Perform polynomial fitting (degree 3 for example)
    coefficients = np.polyfit(flow_rates, heads, 3)
    
    # Create the pump curve as a list of coefficients
    pump_curve = [Decimal(str(coef)) for coef in coefficients.tolist()]
    pump_curves.append(pump_curve)

# Add the fitted pump curves to the DataFrame
df['PumpCurve'] = pump_curves

# Upload pump data to DynamoDB
table = dynamodb.Table(table_name)
for index, row in df.iterrows():
    pump_data = {
        'Name': row['Name'],
        'ID': row['ID'],
        'Flow Head Data': row['Flow Head Data'],
        'PumpCurve': row['PumpCurve']
    }
    try:
        table.put_item(Item=pump_data)
        print(f"Uploaded {row['Name']} to DynamoDB with pump curve.")
    except Exception as e:
        print(f"Error uploading {row['Name']} to DynamoDB: {e}")
