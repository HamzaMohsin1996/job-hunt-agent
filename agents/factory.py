from pydantic_ai import Agent

def create_agent(model_name: str, system_prompt: str) -> Agent:
    # model_name MUST already include provider
    # e.g. "ollama:llama3.1"
    return Agent(
        model=model_name,
        system_prompt=system_prompt,
    )
