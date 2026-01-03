from pydantic_ai import Agent

def create_agent(model_name: str, system_prompt: str) -> Agent:
    return Agent(
        model=model_name,        # e.g. "gpt-4o-mini" OR "ollama:llama3.1"
        system_prompt=system_prompt
    )
