from graph.state import JobHuntState
from agents.factory import create_agent
from agents.cover import COVER_PROMPT
from agents.networking import NETWORKING_PROMPT
from agents.review import REVIEW_PROMPT


def cover_node(state: JobHuntState) -> JobHuntState:
    agent = create_agent(state.model_name, COVER_PROMPT)
    result = agent.run_sync(
        f"CV:\n{state.cv_text}\n\nJob Description:\n{state.job_description}"
    )
    state.cover_letter = result.output
    return state


def networking_node(state: JobHuntState) -> JobHuntState:
    agent = create_agent(state.model_name, NETWORKING_PROMPT)

    result = agent.run_sync(
        f"CV:\n{state.cv_text}\n\nJob Description:\n{state.job_description}"
    )

    state.networking = {"text": result.output}
    return state


def review_node(state: JobHuntState) -> JobHuntState:
    agent = create_agent(state.model_name, REVIEW_PROMPT)

    result = agent.run_sync(
        f"CV:\n{state.cv_text}\n\nJob Description:\n{state.job_description}"
    )

    state.review = {"text": result.output}
    return state


def revise_node(state: JobHuntState) -> JobHuntState:
    feedback = state.feedback or "Make it clearer and more specific."

    if state.task == "cover" and state.cover_letter:
        agent = create_agent(state.model_name, COVER_PROMPT)

        revised = agent.run_sync(
            f"Original:\n{state.cover_letter}\n\nFeedback:\n{feedback}"
        )
        state.cover_letter = revised.output

    elif state.task == "networking" and state.networking:
        agent = create_agent(state.model_name, NETWORKING_PROMPT)

        revised = agent.run_sync(
            f"Original:\n{state.networking['text']}\n\nFeedback:\n{feedback}"
        )
        state.networking = {"text": revised.output}

    return state
