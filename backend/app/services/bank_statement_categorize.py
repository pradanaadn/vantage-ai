import io
from google import genai
from google.genai import types
from loguru import logger
from app.schemas.financial import BankStatement
from app.schemas.file_upload import FileUpload

TEMPERATURE = 0.3
API_KEY = ""  


def analyze_and_categorize_statement_batch(
    bank_statement: FileUpload,
    system_instruction: str,
    model_name: str = "gemini-flash-latest",
) -> types.BatchJob:
    client = genai.Client(api_key=API_KEY)

    # 1. Configure and upload the file to Gemini File API
    config = types.UploadFileConfig(
        display_name=bank_statement.filename,
        mime_type=bank_statement.content_type,
    )
    data = io.BytesIO(bank_statement.data)
    uploaded_file = client.files.upload(file=data, config=config)
    logger.info(f"File uploaded. URI: {uploaded_file.uri}")

    if not (
        uploaded_file.state == types.FileState.ACTIVE
        and uploaded_file.source == types.FileSource.UPLOADED
    ):
        logger.error("File upload failed.")
        raise Exception("File upload failed.")

    # 2. Construct the InlinedRequest
    request = types.InlinedRequest(
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=uploaded_file.uri, mime_type=uploaded_file.mime_type
                    ),
                    types.Part.from_text(
                        text="Extract and categorize the data from this bank statement."
                    ),
                ],
            )
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=BankStatement,
            temperature=TEMPERATURE,
        ),
    )

    # 3. Submit the Batch Job
    batch_job = client.batches.create(
        model=model_name,
        src=[request],
    )
    logger.info(f"Batch job initiated. Job Name: {batch_job}")

    return batch_job


def check_batch_job_status( batch_job_name: str) -> types.BatchJob:
    client = genai.Client(api_key=API_KEY)
    batch_job = client.batches.get(name=batch_job_name)
    logger.info(f"Batch job status: {batch_job.state}")
    return batch_job


if __name__ == "__main__":
    # with open("data/output/statement_1d.pdf", "rb") as f:
    #     file_data = f.read()

    # bank_statement = FileUpload(
    #     filename="sample_statement.pdf",
    #     content_type="application/pdf",
    #     data=file_data,
    # )

    # with open("prompts/bank_statement_classifier.md", "rb") as f:
    #     system_instruction = f.read()

    # batch_job = analyze_and_categorize_statement_batch(
    #     bank_statement, system_instruction
    # )
    
    # logger.info(f"Batch job submitted successfully. Job Name: {batch_job.name}")
    # import time
    # # while True:
    # job_status = check_batch_job_status(batch_job_name="batches/lxa2scznfe5qak22egrlizkbw4r5lgop0aep")
    # print(job_status.dest.inlined_responses[0])
