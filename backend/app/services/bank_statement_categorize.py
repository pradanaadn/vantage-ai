import io
from google import genai
from google.genai import types
from loguru import logger
from pydantic import ValidationError
from app.models.financial import BankStatement
from app.schemas.file_upload import FileUpload

TEMPERATURE = 0.3
API_KEY = ""


def analyze_and_categorize_statement_batch(
    bank_statement: FileUpload,
    system_instruction: str,
    api_key: str ,
    temperature: float = TEMPERATURE,
    model_name: str = "gemini-flash-latest",
) -> types.BatchJob:
    client = genai.Client(api_key=api_key)

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

    if uploaded_file.uri is None or uploaded_file.mime_type is None:
        logger.error("Uploaded file URI or MIME type is missing.")
        raise Exception("Uploaded file URI or MIME type is missing.")

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
            temperature=temperature,
        ),
    )
    try:
        batch_job = client.batches.create(
            model=model_name,
            src=[request],
        )
        logger.info(f"Batch job initiated. Job Name: {batch_job}")
    except Exception as e:
        logger.error(f"Batch job submission failed: {e}")
        raise Exception(f"Batch job submission failed: {e}")

    return batch_job


def check_batch_job_status(batch_job_name: str , api_key:str) -> types.BatchJob:
    client = genai.Client(api_key=api_key)
    batch_job = client.batches.get(name=batch_job_name)
    logger.info(f"Batch job status: {batch_job.state}")
    return batch_job


def get_bank_statement_from_batch_result(batch_job: types.BatchJob) -> BankStatement:
    destination = batch_job.dest
    if destination is None or not destination.inlined_responses:
         logger.error("Batch job has no inlined responses.")
         raise ValueError("Batch job has no inlined responses.")
    response = destination.inlined_responses[0]
    if response.response is None or not response.response.candidates:
        logger.error("Batch job response has no candidates.")
        raise ValueError("Batch job response has no candidates.")
    content = response.response.candidates[0].content
    if content is None or not content.parts:
        logger.error("Batch job response content has no parts.")
        raise ValueError("Batch job response content has no parts.")
    text = content.parts[0].text
    if text is None:
        logger.error("Batch job response content part has no text.")
        raise ValueError("Batch job response content part has no text.")
    try:
        bank_statement = BankStatement.model_validate_json(text)
        logger.info("Bank statement extracted and categorized successfully.")
        return bank_statement
    except ValidationError as e:
        logger.error(f"Failed to parse bank statement from batch result: {e}")
        raise e
    # if response
    


# if __name__ == "__main__":
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
    #     bank_statement=bank_statement,
    #     system_instruction=system_instruction.decode("utf-8"),
    # )

    # logger.info(f"Batch job submitted successfully. Job Name: {batch_job.name}")
    # # import time
    # # while True:
    # job_status = check_batch_job_status(batch_job_name="batches/zpdk2xodrz3z65tc0ve92bj8y7vm2vmuydoi")
    # logger.info(f"Batch job status: {job_status}")
    # # print(job_status.dest.inlined_responses[0].response.candidates[0].content.parts[0].text)
    # print(get_bank_statement_from_batch_result(job_status))