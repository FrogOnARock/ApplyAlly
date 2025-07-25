import warnings

from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.recruiter_agent.agent import recruiter_agent
from .subagents.resume_generator_agent.agent import resume_generator_agent
from .subagents.resume_refiner_agent.agent import resume_refiner_agent



warnings.filterwarnings("ignore", category=UserWarning)


refinement_loop_agent = LoopAgent(
            name="refinement_loop_agent",
            max_iterations=3,
            sub_agents=[
                recruiter_agent,
                resume_refiner_agent,
            ],
            description="Iteratively reviews and refines the applicant's resume until quality requirements are met",
    )


writer_refinement_sequence_agent = SequentialAgent(
            name="writer_refinement_sequence_agent",
            sub_agents=[
                resume_generator_agent,  # Step 1: Generate initial Resume
                refinement_loop_agent,  # Step 2: Review and refine in a loop
            ],
            description="Generates and refines an Applicant Resume tailored to the LinkedIn post through an iterative review process",
        )



