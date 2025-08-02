import os
from pathlib import Path
from azure.ai.agents.models import FilePurpose, CodeInterpreterTool
from aif_agent_client import AIF_AgentClient

# AI Foundary Agent Client
class AIF_DataAgentClient(AIF_AgentClient):
    
    # constructor    
    def __init__(self, name, data_domain):
        try:
            type = os.getenv("DATA_AGENT_NAME")
            super().__init__(name, type)
            self.data_domain = data_domain            
        except Exception as ex:
            print(ex)

    # function to create an agent.
    def create_agents(self):
        try:
            # create the code interpreter 
            code_interpreter = self.create_code_interpreter()

            # Define an agent that uses the CodeInterpreterTool        
            self.agent = self.agent_client.create_agent(
                model=self.model_deployment,
                name=self.agent_name,
                instructions="You are an AI agent that analyzes the data in the file that has been uploaded. Use Python to calculate statistical metrics as necessary.",
                tools=code_interpreter.definitions,
                tool_resources=code_interpreter.resources,            
            )  
        except Exception as ex:
            print(ex)
    
    # function to define the code interpreter.
    def create_code_interpreter(self):
        try:
            # Display the data to be analyzed
            script_dir = Path(__file__).parent  # Get the directory of the script
            file_path = script_dir / 'data.txt'

            with file_path.open('r') as file:
                data = file.read() + "\n"
                print(data)
            # Upload the data file and create a CodeInterpreterTool
            file = self.agent_client.files.upload_and_poll(
                file_path=file_path, purpose=FilePurpose.AGENTS
            )
            print(f"Uploaded {file.filename}")
            code_interpreter = CodeInterpreterTool(file_ids=[file.id])
            return code_interpreter   
        except Exception as ex:
            print(ex)
        
        
    
        