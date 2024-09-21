import os

import httpx
import asyncio

from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, Dict



load_dotenv()
VIRUS_TOTAL_API_KEY = os.environ["VIRUS_TOTAL_API_KEY"]


class Stats(BaseModel):
    malicious: int
    suspicious: int
    undetected: int
    harmless: int
    timeout: int


class EngineResult(BaseModel):
    engine_name: str
    category: str
    result: str


class AnalysisAttributes(BaseModel):
    date: int
    status: str
    stats: Optional[Stats]
    results: Optional[Dict[str, EngineResult]]


class AnalysisResponse(BaseModel):
    id: str
    type: str
    links: Dict[str, str]
    attributes: AnalysisAttributes


async def submit_url(client: httpx.AsyncClient, url: str) -> Optional[str]:
    """Submits a URL to VirusTotal for analysis."""
    response = await client.post(
        "https://www.virustotal.com/api/v3/urls",
        headers={"x-apikey": VIRUS_TOTAL_API_KEY},
        data={"url": url})
    
    response.raise_for_status()
    result = response.json()
    return result["data"]["id"] if "data" in result else None


async def get_analysis_results(client: httpx.AsyncClient, analysis_id: str) -> Optional[AnalysisResponse]:
    """Retrieves the analysis results from VirusTotal and checks the status."""
    response = await client.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers={"x-apikey": VIRUS_TOTAL_API_KEY})
    
    response.raise_for_status()
    print(response.json())
    return AnalysisResponse.parse_obj(response.json()["data"])


async def analyze_url(url: str):
    async with httpx.AsyncClient() as client:
        analysis_id = await submit_url(client, url)
        if not analysis_id:
            print(f"Failed to submit the URL: {url}")
            return
        while True:
            result = await get_analysis_results(client, analysis_id)
            if result.attributes.status == 'completed':
                break
            print(f"Status: {result.attributes.status} - waiting for completion...")
            await asyncio.sleep(5)

        if result:
            print(f"Analysis completed for URL: {url}")
            print(f"Status: {result.attributes.status}")
            if result.attributes.stats:
                print(f"Malicious: {result.attributes.stats.malicious}")
                print(f"Harmless: {result.attributes.stats.harmless}")
            else:
                print("No stats available in the response.")
        else:
            print(f"Failed to retrieve analysis results for ID: {analysis_id}")


if __name__ == "__main__":
    url_to_analyze = "https://app.focusmate.com/"
    asyncio.run(analyze_url(url_to_analyze))
