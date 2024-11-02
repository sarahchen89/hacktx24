from mindee import Client, AsyncPredictResponse, product
import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("MINDEE_API_KEY")
if not key:
    raise ValueError("API key not found")

# Init a new client
mindee_client = Client(api_key=key)

# Add the corresponding endpoint (document). Set the account_name to "mindee" if you are using OTS.
my_endpoint = mindee_client.create_endpoint(
    account_name="mindee",
    endpoint_name="expense_receipts",
    version="5"
)

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Parse the file.
# The endpoint must be specified since it cannot be determined from the class.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.GeneratedV1,
    input_doc,
    endpoint=my_endpoint
)

# Print a brief summary of the parsed data
print(result.document)

# # Iterate over all the fields in the document
# for field_name, field_values in result.document.inference.prediction.fields.items():
#     print(field_name, "=", field_values)