import warnings

from google.adk.agents import SequentialAgent
from .sub_agents.search_agent.agent import search_agent
from .sub_agents.job_extraction_agent.agent import job_extraction_agent
warnings.filterwarnings("ignore", category=UserWarning)


job_detail_sequence_agent = SequentialAgent(
    name='job_detail_sequence_Agent',
    description='You will run the sequential stream to retrieve the job information',
    sub_agents=[search_agent, job_extraction_agent],
)
