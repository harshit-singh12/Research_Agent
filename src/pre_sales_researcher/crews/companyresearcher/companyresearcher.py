import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pre_sales_researcher.tools.custom_tool import LinkedInJobSearchTool
from dotenv import load_dotenv
load_dotenv()

# Loading tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
linkedInJobSearch_tool = LinkedInJobSearchTool()

# Loading LLM

llm= LLM(
    model=os.getenv('MODEL'),
    api_key=os.getenv('AZURE_API_KEY'),
    base_url=os.getenv('AZURE_API_BASE'),
    api_version=os.getenv('AZURE_API_VERSION')
)

@CrewBase
class Companyresearcher:
    """Companyresearcher crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[search_tool, scrape_tool],
            llm=llm,
            verbose=True
        )

    @agent
    def linkedin_jobOpening_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_jobOpening_researcher'],
            tools=[linkedInJobSearch_tool],
            llm = llm,
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            llm= llm,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def linkedin_jobopening_researcher_task(self) -> Task:
        return Task(
            config=self.tasks_config['linkedin_jobopening_researcher_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file= '{company_name}_research.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Companyresearcher crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )