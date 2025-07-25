import warnings

from google.adk.agents import ParallelAgent, SequentialAgent
from ...shared_data import env_variables
from .sub_agents.applicant_agent.agent import applicant_agent
from .sub_agents.search_agent.agent import search_agent
from .writer_agent.agent import writer_refinement_sequence_agent
from google.adk.tools.agent_tool import AgentTool

warnings.filterwarnings("ignore", category=UserWarning)


parallel_agent = ParallelAgent(
    name='parallel_agent',
    description='You will run two sequential streams in parallel. The first is to scrape LinkedIn and the other to summarize'
                'the applicants information',
    sub_agents=[applicant_agent, search_agent],
)


sequential_agent_1 = SequentialAgent(
        name="sequential_agent_1",
        description="You will run the sequence of activating the parallel agent stream, following by the resume writer.",
        sub_agents=[parallel_agent, writer_refinement_sequence_agent],
    )


