from langgraph.graph import StateGraph
from langgraph_supervisor import create_supervisor
from langchain_core.messages import AIMessage
from retrieval_agent import retrieval_agent
from generator_agent import generator_agent
from backend.state_models import SupervisorState
from __init__ import llm


supervisor_graph: StateGraph = create_supervisor(
    supervisor_name="supervisor",
    model=llm,
    prompt=(
        """You are a helpful food ordering assistant and supervisor that can answer questions.\n
        If the queries require searching fro meals and informations about restaurants use the retrieval agent.\n
        Whatever information you get from the retreival agent, send it to the generator agent to get a better response for the user.\n
        Then use the generator agent to process the information from the retrieval agent and return the answer from the generator agent to the user.\n
        """
    ),
    state_schema=SupervisorState,
    agents=[generator_agent, retrieval_agent],
)

supervisor = supervisor_graph.compile()


def process_messages(state: SupervisorState) -> AIMessage:
    """Process the messages and return an AI response."""
    return supervisor.invoke(
        state,
        config={"configurable": {"thread_id": state["thread_id"]}},
    )
