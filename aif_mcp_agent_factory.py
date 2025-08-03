from aif_agent_factory import AIF_AgentFactory
from aif_mcp_agent_client import AIF_MCPAgentClient

# Derived Factory Class to create an agent to interact with mcp server
class AIF_MCPAgentFactory(AIF_AgentFactory):
    def __init__(self, data_domain):
        self.data_domain = data_domain

    def create_agent(self, name):
        return AIF_MCPAgentClient(name, self.data_domain)