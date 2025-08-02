import os
from dotenv import load_dotenv
from aif_agent_functions import execute_agent

# main function
def main(): 
    try:  
        # Starting the AI Foundary Project
        print('Starting the AI Foundary Project')
        # Initialization of configuration   
        load_dotenv() 
        # Execute an AI Agent 
        agent_type =  os.getenv("AGENT_TYPE")         
        execute_agent(agent_type)
        # Stopping the AI Foundary Project
        print('Stopping the AI Foundary Project')   
    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()