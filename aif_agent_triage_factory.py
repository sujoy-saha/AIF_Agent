
from aif_agent_factory import AIF_AgentFactory
from aif_agent_triage_client import AIF_AgentTriageClient

# Derived Factory Class to create a support agent.
class AIF_AgentTriageFactory(AIF_AgentFactory):
    def __init__(self, support_level):
        self.support_level = support_level

    def create_agent(self, name):
        return AIF_AgentTriageClient(name, self.support_level)

