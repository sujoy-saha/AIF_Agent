import os
from aif_project_client import AIF_ProjectClient
from aif_support_agent_factory import AIF_SupportAgentFactory
from aif_data_agent_factory import AIF_DataAgentFactory
from aif_agent_triage_factory import AIF_AgentTriageFactory
from aif_mcp_agent_factory import AIF_MCPAgentFactory

# function to create and run an agent using the project client.
def create_and_run_agent(agent_type):    
    try:  
        project_client = AIF_ProjectClient()
        if agent_type.lower() == "chat_completion":
            project_client.chat_completion()
        elif agent_type.lower() == "run_agent":
            project_client.create_and_run_agent()
        elif agent_type.lower() == "filesearch_agent":
            project_client.create_filesearch_agent()                
        else:
            raise ValueError("Unknown agent function. Use 'chat_completion' or 'run_agent' or 'filesearch_agent'.")
    except Exception as ex:
        print(ex)

# function to create an agent client.
def create_agent(agent_type):
    try:
        agent_factory = None
        name = ""
        if agent_type.lower() == os.getenv("SUPPORT_AGENT_NAME"):
            agent_factory = AIF_SupportAgentFactory(support_level=2)  
            name = "Alice"                  
        elif agent_type.lower() == os.getenv("DATA_AGENT_NAME"):        
            agent_factory = AIF_DataAgentFactory(data_domain="finance")
            name = "Bob"
        elif agent_type.lower() == os.getenv("TRIAGE_AGENT_NAME"):        
            agent_factory = AIF_AgentTriageFactory(support_level=2)  
            name = "John"
        elif agent_type.lower() == os.getenv("MCP_AGENT_NAME"):        
            agent_factory = AIF_MCPAgentFactory(data_domain="finance")  
            name = "Lis"    
        else:
            raise ValueError("Unknown agent type. Use 'support' or 'data'.")
        return agent_factory.create_agent(name)
    except Exception as ex:
            print(ex)

# function to execute an agent.
def execute_agent(agent_type):
    try:
        if agent_type.lower() == os.getenv("SUPPORT_AGENT_NAME") or agent_type.lower() == os.getenv("DATA_AGENT_NAME") or agent_type.lower() == os.getenv("TRIAGE_AGENT_NAME") or agent_type.lower() == os.getenv("MCP_AGENT_NAME"):        
            create_agent(agent_type).execute_agent()   
        else:
            create_and_run_agent(agent_type)           
    except Exception as ex:
            print(ex)

