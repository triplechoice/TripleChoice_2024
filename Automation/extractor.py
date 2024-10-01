import mysql.connector
import json
import time
import subprocess

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pashandi2015$",
        database="triple_choice"
    )

def fetch_latest_order():
    db = connect_to_db()
    cursor = db.cursor()

    query = """
    SELECT 
        order_id, 
        quantity, 
        comment, 
        answer,
        created_at  
    FROM 
        order_request 
    ORDER BY 
        created_at DESC  
    LIMIT 1;
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    if result:
        order_id, quantity, comment, answer_json, created_at = result
        specifications = json.loads(answer_json)
        
        # Extract the title from the specifications
        title = specifications.get('title', 'N/A')  # Default to 'N/A' if title is not found
        
        return order_id, quantity, comment, specifications, title, created_at  # Return title along with other details
    return None

def monitor_database():
    last_created_at = None  # Keep track of the last processed created_at timestamp

    while True:
        order_details = fetch_latest_order()
        
        if order_details:
            order_id, quantity, comment, specifications, title, created_at = order_details
            
            if created_at != last_created_at:
                print(f"\nNew Order Detected:")
                print(f"Title: {title}")  # Print the extracted title
                print(f"Order ID: {order_id}")
                print(f"Quantity: {quantity}")
                print(f"Comment: {comment if comment else 'N/A'}")
                print("Specifications:")
                
                input_flow_rate = None
                head_input = None
                
                for spec in specifications.get('partclassification_set', []):
                    print(f"- {spec['classification']['title']}:")
                    for attr in spec['partclassificationattribute_set']:
                        print(f"  - {attr['attribute']['title']}: {attr['attribute']['value']}")
                        if attr['attribute']['title'] == "Flow":  # Adjust this to your actual attribute title
                            input_flow_rate = float(attr['attribute']['value'])  # Set Flow value
                        if attr['attribute']['title'] == "Head":  # Adjust this to your actual attribute title
                            head_input = float(attr['attribute']['value'])  # Set Head value
                
                # Call the PumpMatch code if the title is "1_Pump"
                if title == "1_Pump" and input_flow_rate is not None and head_input is not None:
                    # Call the PumpMatch.py script and pass flow rate and head as arguments
                    subprocess.run(["python", "PumpMatch.py", str(input_flow_rate), str(head_input)])
                
                last_created_at = created_at  # Update last processed created_at timestamp

        time.sleep(1)  # Check for new entries every second

if __name__ == "__main__":
    monitor_database()
