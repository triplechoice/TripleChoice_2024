import boto3


def get_dynamodb_client():
    # Connect to DynamoDB Local
    dynamodb = boto3.client(
        'dynamodb',
        endpoint_url="http://localhost:8001",  # URL for DynamoDB Local
        region_name="us-west-2",  # Dummy region
        aws_access_key_id="anything",  # Dummy credentials
        aws_secret_access_key="anything"  # Dummy credentials
    )
    return dynamodb

def get_dynamodb_resource():
    try:
        # DynamoDB Local runs on localhost:8000
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url="http://localhost:8001",  # URL for DynamoDB Local
            region_name="us-west-2",  # Dummy region
            aws_access_key_id="anything",  # Dummy credentials
            aws_secret_access_key="anything"  # Dummy credentials
        )
        return dynamodb
    except Exception as e:
        print(f"Error connecting to DynamoDB: {str(e)}")
        return None


def list_tables():
    dynamodb = get_dynamodb_client()

    try:
        # List all tables
        response = dynamodb.list_tables()
        table_names = response.get('TableNames', [])

        if table_names:
            print("Tables in DynamoDB Local:")
            for table in table_names:
                print(f"- {table}")
        else:
            print("No tables found in DynamoDB Local.")

    except Exception as e:
        print(f"Error listing tables: {str(e)}")

# Function to retrieve and display items from a table
def get_items_from_table(table_name):
    # Get DynamoDB client
    dynamodb = get_dynamodb_resource()

    if not dynamodb:
        print("Failed to connect to DynamoDB.")
        return

    try:
        # Get table
        table = dynamodb.Table(table_name)

        # Scan the table (to retrieve all items)
        response = table.scan()
        items = response.get('Items', [])

        if items:
            print(f"Items in {table_name}:")
            for item in items:
                print(item)
        else:
            print(f"No items found in {table_name}")

    except Exception as e:
        print(f"Error retrieving data from {table_name}: {str(e)}")


if __name__ == "__main__":
    list_tables()
    get_items_from_table("YourTableName")