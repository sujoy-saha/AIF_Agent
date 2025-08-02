
from aif_agent_factory import AIF_AgentFactory
from aif_support_agent_client import AIF_SupportAgentClient

# Derived Factory Class to create a support agent.
class AIF_SupportAgentFactory(AIF_AgentFactory):
    def __init__(self, support_level):
        self.support_level = support_level

    def create_agent(self, name):
        return AIF_SupportAgentClient(name, self.support_level)

