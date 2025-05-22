import boto3
from datetime import datetime
import numpy as np
import pandas as pd

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_basename = f"helloworld_{timestamp}"

    filename = f"{filename_basename}.txt"
    filename_csv = f"{filename_basename}.csv"

    now = datetime.now()

    random_df = pd.DataFrame(
        np.random.randint(0, 100, size=(3, 3)),
        columns=['A', 'B', 'C']
    )

    # Add row and column labels for better readability
    random_df.index = ['Row 1', 'Row 2', 'Row 3']
    random_df.to_csv(filename_csv, index=True)

    print("The current time is:", now.strftime("%Y-%m-%d %I:%M:%S %p"))

    # Create the hello world file
    with open(filename, 'w') as f:
        now_formatted = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        first_line =f"Hello World! The current time is: {now_formatted}\n"
        f.write(first_line)
        f.write("This is a test file uploaded from a Jupyter Notebook\n")
        f.write("If you can see this file in S3, your permissions are working correctly!")
    print(f"Created file: {filename}")
    print(f"Content: \n{open(filename).read()}")

    s3 = boto3.client('s3')

    bucket_name = "jonchengws3"
    # Upload file to S3
    s3.upload_file(
        Filename=filename,
        Bucket=bucket_name,
        Key=f"hello-world-tests/{filename}"
    )

    s3.upload_file(
        Filename=filename_csv,
        Bucket=bucket_name,
        Key=f"hello-world-tests/{filename_csv}"
    )

if __name__ == "__main__":
    main()