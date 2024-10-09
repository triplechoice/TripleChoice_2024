import mysql.connector
import json
from decimal import Decimal
import numpy as np
from scipy.interpolate import interp1d
from tabulate import tabulate

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'TripleChoice',  # Update with your MySQL username
    'password': 'Pashandi2015$',  # Update with your MySQL password
    'database': 'triplechoice'  # The database that contains the pump_data table
}

def interpolate_parameters(pump_curve, Required_Q):
    """Interpolate for H, P1, P2, NPSH, Eta1, Eta2 based on Required_Q."""
    try:
        Q_values = np.array([float(curve['Q']) for curve in pump_curve])
        H_values = np.array([float(curve['H']) for curve in pump_curve])
        P1_values = np.array([float(curve['P1']) for curve in pump_curve])
        P2_values = np.array([float(curve['P2']) for curve in pump_curve])
        NPSH_values = np.array([float(curve['NPSH']) for curve in pump_curve])
        Eta1_values = np.array([float(curve['Eta1']) for curve in pump_curve])
        Eta2_values = np.array([float(curve['Eta2']) for curve in pump_curve])

        # Create interpolation functions for all parameters
        H_interp = interp1d(Q_values, H_values, kind='linear', fill_value="extrapolate")
        P1_interp = interp1d(Q_values, P1_values, kind='linear', fill_value="extrapolate")
        P2_interp = interp1d(Q_values, P2_values, kind='linear', fill_value="extrapolate")
        NPSH_interp = interp1d(Q_values, NPSH_values, kind='linear', fill_value="extrapolate")
        Eta1_interp = interp1d(Q_values, Eta1_values, kind='linear', fill_value="extrapolate")
        Eta2_interp = interp1d(Q_values, Eta2_values, kind='linear', fill_value="extrapolate")

        # Interpolate for the required Q
        Predicted_H = H_interp(Required_Q)
        Predicted_P1 = P1_interp(Required_Q)
        Predicted_P2 = P2_interp(Required_Q)
        Predicted_NPSH = NPSH_interp(Required_Q)
        Predicted_Eta1 = Eta1_interp(Required_Q)
        Predicted_Eta2 = Eta2_interp(Required_Q)

        return Predicted_H, Predicted_P1, Predicted_P2, Predicted_NPSH, Predicted_Eta1, Predicted_Eta2
    except Exception as e:
        print(f"Error during interpolation: {e}")
        return None, None, None, None, None, None

def process_pumps(Required_Q, Required_H):
    """Process all pumps and find matches based on required flow rate (Q) and head (H)."""
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # Query to get all pump data
        query = "SELECT PumpModel, Price, Qmin, Qmax, CurveData, Link, ImageLink FROM pump_data"
        cursor.execute(query)
        pumps = cursor.fetchall()

        total_pumps = len(pumps)
        matching_pumps = []

        # Loop through each pump and check for a match
        for pump in pumps:
            pump_model = pump['PumpModel']
            pump_curve = json.loads(pump['CurveData'])

            print(f"Processing pump model: {pump_model}")

            try:
                # Perform interpolation for this pump
                Predicted_H, Predicted_P1, Predicted_P2, Predicted_NPSH, Predicted_Eta1, Predicted_Eta2 = interpolate_parameters(pump_curve, Required_Q)

                # Check if predicted head meets the criteria
                if Predicted_H is not None and Required_H < Predicted_H < 1.25 * Required_H:
                    matching_pumps.append({
                        'Model': pump_model,
                        'Predicted_H': Predicted_H,
                        'Predicted_P1': Predicted_P1,
                        'Predicted_P2': Predicted_P2,
                        'Predicted_NPSH': Predicted_NPSH,
                        'Predicted_Eta1': Predicted_Eta1,
                        'Predicted_Eta2': Predicted_Eta2,
                        'Price': pump['Price'],
                        'Link': pump['Link'],
                        'Image Link': pump['ImageLink']
                    })
            except Exception as e:
                print(f"Error processing pump {pump_model}: {e}")

        # Handle prices and sort by numerical price values
        def price_key(pump):
            try:
                return float(pump['Price'].strip('$').replace(',', ''))
            except ValueError:
                return float('inf')

        matching_pumps = sorted(matching_pumps, key=price_key)

        # Display results with correct grammar
        num_matches = len(matching_pumps)
        match_text = "Match" if num_matches == 1 else "Matches"
        print(f"Search Results: {num_matches} {match_text} out of {total_pumps}")

        if matching_pumps:
            print(tabulate(matching_pumps, headers="keys"))
        else:
            print("No matching pumps found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    Required_Q = float(input("Enter the required flow rate (Q) in US gpm: "))
    Required_H = float(input("Enter the required head (H) in ft: "))
    process_pumps(Required_Q, Required_H)
