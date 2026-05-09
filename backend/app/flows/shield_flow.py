from prefect import flow, task
import asyncio

# These tasks will be executed by a Prefect Worker, not your FastAPI server
@task(retries=3, retry_delay_seconds=10)
async def extract_invoice_data(image_url: str):
    # In Week 1, we replace this with real Gemini 1.5 Flash logic
    await asyncio.sleep(5)
    return {
        "vendor": "Acme Coffee Co",
        "total": 150.00,
        "savings_found": 15.50
    }

@flow(name="invoice-audit-flow")
async def invoice_audit_flow(image_url: str):
    return await extract_invoice_data(image_url)

if __name__ == "__main__":
    # This command creates the deployment in Prefect Cloud
    # Run this once to register the flow
    invoice_audit_flow.serve(name="vantage-prod")
