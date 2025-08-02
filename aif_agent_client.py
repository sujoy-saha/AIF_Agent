import os
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ListSortOrder, MessageRole

# AI Foundary Agent Client
class AIF_AgentClient:
    
    # constructor    
    def __init__(self, name, type):
        try:
            print("Connecting to agent...")
            # set the name of the agent.            
            self.agent_name = name + "-" + type
            # Clear the console
            os.system('cls' if os.name=='nt' else 'clear')
            # Load environment variables from .env file    
            self.project_endpoint= os.getenv("AI_PROJECT_ENDPOINT")
            self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")        
            # Connect to the Agent client
            self.agent_client = AgentsClient(
                endpoint=self.project_endpoint,
                credential=DefaultAzureCredential
                    (exclude_environment_credential=True,
                    exclude_managed_identity_credential=True)
            )
        except Exception as ex:
            print(ex)
    
     # function to execute the interactions
    def execute_agent(self):
        try:
            with self.agent_client:
                self.create_agents()
                self.execute_task()
                self.disconnect()
        except Exception as ex:
            print(ex)

    # function to create an agent.
    def create_agents(self):
        raise NotImplementedError("This method should be overridden.")
    
    # function to prompt to the user.
    def execute_task(self):
        try:
            #create a new thread for the agent.
            self.thread = self.agent_client.threads.create()
            print(f"You're chatting with: {self.agent.name} ({self.agent.id})") 
            # Loop until the user types 'quit'
            while True:
                # Get input text
                user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
                if user_prompt.lower() == "quit" or user_prompt.lower() == "exit":
                    break
                if len(user_prompt) == 0:
                    print("Please enter a prompt.")
                    continue

                # Send a prompt to the agent            
                message = self.agent_client.messages.create(
                    thread_id=self.thread.id,
                    role="user",
                    content=user_prompt
                )
                # Create and process Agent run in thread
                print("Processing the request. Please wait.")
                run = self.agent_client.runs.create_and_process(thread_id=self.thread.id, agent_id=self.agent.id)
                # Check the run status for failures
                if run.status == "failed":
                    print(f"Run failed: {run.last_error}")  
                #display the log of the conversation.
                self.display_conversation_log()                   
        except Exception as ex:
            print(ex)
    
    # function to display the log of the conversation.
    def display_conversation_log(self):
        try:
            # Show the latest response from the agent
            last_msg = self.agent_client.messages.get_last_message_text_by_role(
                thread_id=self.thread.id,
                role=MessageRole.AGENT,
            )
            if last_msg:
                print(f"Last Message: {last_msg.text.value}")
        except Exception as ex:
            print(ex)
    
    # function to summarize the conversation and delete the agent.
    def disconnect(self):        
        try:
            # Get the conversation history
            print("\nConversation Log:\n")
            messages = self.agent_client.messages.list(thread_id=self.thread.id, order=ListSortOrder.ASCENDING)
            for message in messages:
                if message.text_messages:
                    last_msg = message.text_messages[-1]
                    print(f"{message.role}: {last_msg.text.value}\n")

            # Clean up
            self.agent_client.delete_agent(self.agent.id)
            print("Deleted agent")
        except Exception as ex:
            print(ex)
