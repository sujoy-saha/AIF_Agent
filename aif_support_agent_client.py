import os
from azure.ai.agents.models import FunctionTool, ToolSet
from user_functions import user_functions
from aif_agent_client import AIF_AgentClient

# AI Foundary Agent Client
class AIF_SupportAgentClient(AIF_AgentClient):
    
    # constructor    
    def __init__(self, name, support_level):
        try:
            type = os.getenv("SUPPORT_AGENT_NAME")
            super().__init__(name, type)            
            self.support_level = support_level            
        except Exception as ex:
            print(ex)
    
    # function to create an agent.
    def create_agents(self):
        try:
            # Define an agent that can use the custom functions
            toolset = self.create_toolset()
            #create a support agent using the toolset.                
            self.agent = self.agent_client.create_agent(
                model=self.model_deployment,
                name=self.agent_name,
                instructions="""You are a technical support agent.
                                When a user has a technical issue, you get their email address and a description of the issue.
                                Then you use those values to submit a support ticket using the function available to you.
                                If a file is saved, tell the user the file name.
                            """,
                toolset=toolset
            )
        except Exception as ex:
            print(ex)

    # function to define the toolset.
    def create_toolset(self):
        try:
            # Define an agent that can use the custom functions
            functions = FunctionTool(user_functions)
            toolset = ToolSet()
            toolset.add(functions)
            self.agent_client.enable_auto_function_calls(toolset)
            return toolset
        except Exception as ex:
            print(ex)
        