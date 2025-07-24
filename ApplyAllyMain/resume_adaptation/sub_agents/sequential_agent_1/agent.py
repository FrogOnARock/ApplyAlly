import warnings

from google.adk.agents import ParallelAgent, SequentialAgent
from ...shared_data import env_variables
from .sub_agents.sequential_agent_2.agent import sequential_agent_2
from .sub_agents.sequential_agent_3.agent import sequential_agent_3
#from .sub_agents.writer_agent.agent import sequential_agent_4
warnings.filterwarnings("ignore", category=UserWarning)


parallel_agent = ParallelAgent(
    name='parallel_agent',
    description='You will run two sequential streams in parallel. The first is to scrape LinkedIn and the other to summarize'
                'the applicants information',
    sub_agents=[sequential_agent_2, sequential_agent_3],
)

sequential_agent_1 = SequentialAgent(
        name="_agent",
        description="You will run the sequence of activating the parallel agent stream, following by the resume writer.",
        sub_agents=[parallel_agent],
    )


