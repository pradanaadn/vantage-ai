from prefect import task
from prefect.blocks.system import Secret


@task(name="Secret Task")
def gemini_secret(secret_name: str = "gemini-api-key") -> str:
    secret = Secret.load(secret_name)
    if not secret:
        raise ValueError(f"Secret '{secret_name}' not found.")
    secret_value = secret.get() # pyright: ignore[reportAttributeAccessIssue]
    if not secret_value:
        raise ValueError(f"Secret '{secret_name}' is empty or not found.")
    return secret_value

if __name__ == "__main__":
    # Example usage for testing
    try:
        api_key = gemini_secret("gemini-api-key")
        print(f"Retrieved Gemini API Key: {api_key}")
    except ValueError as e:
        print(f"Error retrieving secret: {e}")