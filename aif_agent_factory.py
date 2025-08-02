# Abstract Factory Class to create an agent.
class AIF_AgentFactory:
    def create_agent(self, name):
        raise NotImplementedError("This method should be overridden.")
