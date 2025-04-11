import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
import requests
from dotenv import load_dotenv
load_dotenv()


class LinkedInSearchtoolInput(BaseModel):
    """Input schema for MyCustomTool."""
    #company_founder: str = Field(..., description="Name of the company founder")
    person_name: str = Field(..., description="Name of the person")
    company_name: str = Field(..., description="Name of the company")

class LinkedInSearchTool(BaseTool):
    name: str = "LinkedIn Profile Search Tool"
    description: str = (
        "Search the person linkedin profile and retreive all the information from the profile."
    )
    args_schema: Type[BaseModel] = LinkedInSearchtoolInput
    
    def _run(self, person_name: str, company_name: str) -> str:
        serper_tool = SerperDevTool()
        
        # First search for the LinkedIn profile
        search_query = f"site:linkedin.com/in {person_name} {company_name}"
        search_results = serper_tool.run(query=search_query)
        
        # Extract LinkedIn profile link
        linkedin_links = [
            result['link'] 
            for result in search_results.get('results', [])
            if 'linkedin.com/in' in result.get('link', '')
        ]
        
        if not linkedin_links:
            return "No LinkedIn profile found."
            
        # Get profile details using the first LinkedIn URL found
        profile_url = linkedin_links[0]
        profile_details = serper_tool.run(
            query=f"Extract all professional information, experience, education and skills from LinkedIn profile: {profile_url}"
        )
        
        # Format the results
        if profile_details and profile_details.get('results'):
            profile_info = profile_details['results'][0].get('snippet', '')
            return f"LinkedIn Profile Information for {person_name}:\n\n{profile_info}\n\nProfile URL: {profile_url}"
        
        return f"Found profile at {profile_url} but could not extract detailed information."


class LinkedInJobSearchtoolInput(BaseModel):
    """Input schema for MyCustomTool."""
    #company_founder: str = Field(..., description="Name of the company founder")
    company_name: str = Field(..., description="Name of the company")

class LinkedInJobSearchTool(BaseTool):
    name: str = "LinkedIn job opening search tool"
    description: str = (
        "Search the job opening on linkedin for the provided company and return all the current opening."
    )
    args_schema: Type[BaseModel] = LinkedInJobSearchtoolInput
    
    def _run(self, company_name: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")  # Replace with your actual key
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        query = f"site:linkedin.com/jobs {company_name} careers"
        payload = {"q": query}
        search_results =  requests.post(url, headers=headers, json=payload)
        search_results.raise_for_status()
        data = search_results.json()
        
        if search_results.status_code == 200:
            data = search_results.json()
            results = data.get("organic", [])
            if not results:
                return "No job listings found."
            return "\n\n".join([f"{item['title']}\n{item['link']}" for item in results])
        else:
            return f"Error: {search_results.status_code}, {search_results.text}"