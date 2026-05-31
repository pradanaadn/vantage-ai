from google import genai
from google.genai import types
from loguru import logger
from pydantic import TypeAdapter
from app.models.bussines import BussinessCompetitor
from app.core.config import settings


async def analyze_business(
    business_name: str,
    business_google_maps_url: str,
    system_instruction: str,
    api_key: str,
    number_of_competitors: int = 3,
    temperature: float = 0.6,
    model_name: str = "gemini-flash-latest",
) -> BussinessCompetitor:

    logger.info(f"Starting analysis for business: {business_name}")
    client = genai.Client(api_key=api_key)

    # 1. Define the Tools
    tools = [types.Tool(google_maps=types.GoogleMaps())]
    generate_content_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools,
        temperature=temperature,
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.HIGH,
        ),
        response_schema=BussinessCompetitor,
    )

    prompt = prompt = (
        f"Cari dan analisis kompetitor untuk bisnis berikut: '{business_name}' dengan googlemaps {business_google_maps_url}. "
        f"Identifikasi minimal {number_of_competitors} kompetitor (Direct, Indirect, dan Replacement). "
        "Lakukan analisis mendalam untuk masing-masing kompetitor berdasarkan ulasan Google Maps terbaru. "
        "Output harus mengikuti skema JSON BussinessCompetitor tanpa sitasi dan menggunakan bahasa Indonesia yang lugas."
    )

    try:
        logger.info(f"Sending analysis request for {business_name} to Gemini API.")
        response = await client.aio.models.generate_content(
            model=model_name,
            contents=prompt,
            config=generate_content_config,
        )

        logger.info(f"Analysis for {business_name} successful.")
        logger.debug(f"Raw response: {response.parsed}")
        response_data = TypeAdapter(BussinessCompetitor).validate_python(
            response.parsed
        )
        return response_data

    except Exception as e:
        logger.error(f"Business analysis failed: {e}")
        raise


if __name__ == "__main__":
    import asyncio
    from app.core.config import settings

    # Example usage
    business_name = "SEDJUK BAKMI & KOPI CINERE"
    business_google_maps_url = "https://www.google.com/maps/place/SEDJUK+BAKMI+%26+KOPI+CINERE/@-6.3428635,106.7777535,15z/data=!4m6!3m5!1s0x2e69ef4f61fdf84f:0x43946b267bdf020a!8m2!3d-6.3428676!4d106.7859521!16s%2Fg%2F11fv7pdbp0?entry=ttu&g_ep=EgoyMDI2MDUyNy4wIKXMDSoASAFQAw%3D%3D"
    with open("prompts/bussiness_competitor.md", "r") as f:
        system_instruction = f.read()

    result = asyncio.run(
        analyze_business(
            business_name,
            business_google_maps_url,
            system_instruction,
            settings.GEMINI.API_KEY,
        )
    )
    print(result.model_dump_json(indent=2))
