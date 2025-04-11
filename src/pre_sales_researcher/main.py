#!/usr/bin/env python
from typing import Dict, Optional
from crewai.flow import Flow, listen, start, router
from src.pre_sales_researcher.crews.companyresearcher.companyresearcher import Companyresearcher
from src.pre_sales_researcher.crews.peoplesearcher.peoplesearcher import PeopleSearcher
from pydantic import BaseModel

class main_research_flow():
    def startCrew(company_name: Optional[str], person_name: Optional[str]):
        Research_agent_results = []
        inputs = {
            'company_name': company_name.strip(),
            'person_name': person_name.strip()
        }
        try:
            Research_agent_results = RouterFlow().kickoff(inputs=inputs)
        except Exception as e:
            Research_agent_results = (f"An error occurred while running the crew: {e}")
        return Research_agent_results

class company_details(BaseModel):
    company_name: str = ""
    person_name: str = ""

class RouterFlow(Flow[company_details]):
    
    @start()
    def start_method(self):
        print("Company Name: ", self.state.company_name)
        print("Person Name: ", self.state.person_name)

    @router(start_method)
    def user_input(self):
        if self.state.company_name and self.state.person_name:
            return "both"
        elif self.state.company_name:
            return "company_name"
        elif self.state.person_name:
            return "person_name"
        else:
            raise ValueError("Invalid input, please provide either company name or person name or both.")

    @listen("company_name")
    def company_researcher_listener(self):
        try:
            print("🔎 Executing Company Researcher Crew...")
            result = Companyresearcher().crew().kickoff(inputs={"company_name": self.state.company_name})
            return result
        except Exception as e:
            result = f"An error occurred while running the crew: {e}"
            return result

    @listen("person_name")
    def people_searcher_listener(self):
        try:
            print("🕵️‍♂️ Executing People Searcher Crew...")
            result = PeopleSearcher().crew().kickoff(
                inputs={"person_name": self.state.person_name, "company_name": self.state.company_name}
                )
            return result
        except Exception as e:
            result = f"An error occurred while running the crew: {e}"
            return result

    @listen("both")
    def company_researcher_and_people_searcher_listener(self):
        try:
            print("🔄 Running Both Crews Sequentially...")
            company_result = Companyresearcher().crew().kickoff(inputs={"company_name": self.state.company_name})
        except Exception as e:
            company_result = f"An error occurred while running the company crew: {e}"

        try:
            people_result = PeopleSearcher().crew().kickoff(
                inputs={"person_name": self.state.person_name, "company_name": self.state.company_name}
            )
        except Exception as e:
            people_result = f"An error occurred while running the people crew: {e}"
        return [company_result, people_result]


def plot():
    researcherflow = RouterFlow()
    researcherflow.plot()
'''
if __name__ == "__main__":
    #inputs = {"company_name": "LatentBridge", "person_name": "Hema Gandhi"}
    RouterFlow().kickoff()'''

if __name__ == "__main__":
    main_research_flow().startCrew(company_name="LatentBridge", person_name="Hema Gandhi")