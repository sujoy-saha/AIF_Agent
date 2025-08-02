import os
from azure.ai.agents.models import ConnectedAgentTool

class AIF_Agent:
    def __init__(self, agents_client, name, instructions, description):
        self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
        self.agents_client = agents_client
        self.name = name
        self.instructions = instructions
        self.description = description
        self.create_agent()
        self.connected_agent_tool()
    # create an agent.
    def create_agent(self):
        try:
             # Create the an agent on the Azure AI agent service
            self.agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name=self.name,
                instructions=self.instructions
            )                        
        except Exception as ex:
                print(ex)
    # create a connected agent tool for an agent
    def connected_agent_tool(self):
        try:
             # Create a connected agent tool for an agent
            self.agent_tool = ConnectedAgentTool(
                id=self.agent.id, 
                name=self.name, 
                description=self.description
            )                        
        except Exception as ex:
                print(ex)
    