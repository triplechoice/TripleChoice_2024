import sys
import boto3
import pandas as pd
import numpy as np
from decimal import Decimal

# Create a local DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8001')

# Define the table name
table_name = 'YourTableName'  # Replace with your actual table name
table = dynamodb.Table(table_name)

# Function to get pump data from DynamoDB
def get_pump_data():
    response = table.scan()
    return response['Items']

# Function to predict head based on flow rate using the pump curve
def predict_head(flow_rate, pump_curve):
    # Calculate predicted head using polynomial coefficients
    predicted_head = sum(coef * (flow_rate ** i) for i, coef in enumerate(reversed(pump_curve)))
    return predicted_head

if __name__ == "__main__":
    # Get input parameters from command line arguments
    if len(sys.argv) != 3:
        print("Usage: python PumpMatch.py <input_flow_rate> <head_input>")
        sys.exit(1)

    input_flow_rate = float(sys.argv[1])
    head_input = float(sys.argv[2])

    # Fetch pump data from DynamoDB
    pump_data_list = get_pump_data()

    # Prepare a list for results
    results = []

    # Check for all pumps
    for pump_data in pump_data_list:
        pump_name = pump_data['Name']
        pump_curve = [float(coef) for coef in pump_data['PumpCurve']]  # Convert to float for calculation
        
        # Predict the head using the input flow rate
        head_predicted = predict_head(input_flow_rate, pump_curve)

        # Determine if it's a matching pump
        is_match = head_input < head_predicted < head_input * 1.25
        match_status = "Match" if is_match else "No Match"

        # Append the results
        results.append({
            'Pump Name': pump_name,
            'Input Flow Rate (GPM)': input_flow_rate,
            'Input Head (ft)': head_input,
            'Predicted Head (ft)': head_predicted,
            'Match Pump': match_status
        })

    # Create a DataFrame from results and print it
    results_df = pd.DataFrame(results)
    print("\nSummary of Results:")
    print(results_df)  # Print all results, including matches and non-matches
