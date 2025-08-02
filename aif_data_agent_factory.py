from aif_agent_factory import AIF_AgentFactory
from aif_data_agent_client import AIF_DataAgentClient

# Derived Factory Class to create a data agent.
class AIF_DataAgentFactory(AIF_AgentFactory):
    def __init__(self, data_domain):
        self.data_domain = data_domain

    def create_agent(self, name):
        return AIF_DataAgentClient(name, self.data_domain)