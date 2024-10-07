import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8001', aws_access_key_id="anything", aws_secret_access_key="anything")

# List all the tables in DynamoDB
try:
    tables = dynamodb.list_tables()
    table_names = tables['TableNames']
    print("Tables in DynamoDB:")
    for table_name in table_names:
        print(f"- {table_name}")
except Exception as e:
    print(f"Error listing tables: {e}")

# Function to print the data from each table
def print_table_data(table_name):
    try:
        # Get the table resource
        dynamodb_resource = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8001', aws_access_key_id="anything", aws_secret_access_key="anything")
        table = dynamodb_resource.Table(table_name)

        # Scan the table to get all the items
        response = table.scan()
        items = response['Items']

        print(f"\nData from table '{table_name}':")
        if items:
            for item in items:
                print(item)
        else:
            print(f"Table '{table_name}' is empty.")
    except Exception as e:
        print(f"Error scanning table {table_name}: {e}")

# Print data from each table
for table_name in table_names:
    print_table_data(table_name)
