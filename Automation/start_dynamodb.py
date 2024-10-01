import subprocess
import time
import os

def start_dynamodb():
    # Command to start DynamoDB Local
    command = [
        'java',
        '-Djava.library.path=D:\\TripleChoice\\2024\\DynamoDB\\dynamodb_local_latest\\DynamoDBLocal_lib',
        '-jar',
        'DynamoDBLocal.jar',
        '-sharedDb'
    ]

    # Start the process
    process = subprocess.Popen(command, cwd='D:\\TripleChoice\\2024\\DynamoDB\\dynamodb_local_latest', 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)

    # Wait a few seconds to ensure DynamoDB Local is up and running
    time.sleep(5)  # Adjust this time as needed

    return process

if __name__ == "__main__":
    dynamodb_process = start_dynamodb()
    print("DynamoDB Local started. PID:", dynamodb_process.pid)

    # Keep the process running until manually terminated
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping DynamoDB Local...")
        dynamodb_process.terminate()
