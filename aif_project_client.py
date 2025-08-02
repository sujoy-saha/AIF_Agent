import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder, FilePurpose, FileSearchTool,FunctionTool, ToolSet, MessageRole

# AI Foundary project client
class AIF_ProjectClient:
    def __init__(self):
        print("Connecting to agent...")
         # Clear the console
        os.system('cls' if os.name=='nt' else 'clear')
        # Load environment variables from .env file    
        self.project_endpoint= os.getenv("AI_PROJECT_ENDPOINT") 
        self.api_version = os.getenv("API_VERSION") 
        self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
        self.writing_agent_name = os.getenv("WRITING_AGENT_NAME")
        self.file_search_agent_name = os.getenv("FILE_SEARCH_AGENT_NAME")
        #create the project client
        self.project_client = AIProjectClient(
            endpoint=self.project_endpoint,
            credential=DefaultAzureCredential(),
        )
    
    # chat completiion function
    def chat_completion(self):         
        # Load environment variables from .env file
        models = self.project_client.inference.get_azure_openai_client(api_version=self.api_version)            
        response = models.chat.completions.create(
                model=self.model_deployment,
                messages=[
                    {"role": "system", "content": "You are a helpful writing assistant"},
                    {"role": "user", "content": "Write me a poem about flowers"},
                ],
            )
        print(response.choices[0].message.content) 

    def create_and_run_agent(self):        
        self.agent = self.project_client.agents.create_agent(
            model=self.model_deployment,
            name=self.writing_agent_name,
            instructions="You are a helpful writing assistant")
        
        thread = self.project_client.agents.threads.create()
        message = self.project_client.agents.messages.create(
            thread_id=thread.id, 
            role="user", 
            content="Write me a poem about flowers")
        
        run = self.project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=self.agent.id)
        if run.status == "failed":
            # Check if you got "Rate limit is exceeded.", then you want to get more quota
            print(f"Run failed: {run.last_error}")

        # Get messages from the thread
        messages = self.project_client.agents.messages.list(thread_id=thread.id)

        # Get the last message from the sender
        messages = self.project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        for message in messages:
            if message.run_id == run.id and message.text_messages:
                print(f"{message.role}: {message.text_messages[-1].text.value}")
        
        # delete agent
        self.project_client.agents.delete_agent(self.agent.id)
        print("Deleted agent")   

    def create_filesearch_agent(self):
    
        # Upload file and create vector store
        file = self.project_client.agents.files.upload(file_path="./product_info_1.md", purpose=FilePurpose.AGENTS)
        vector_store = self.project_client.agents.vector_stores.create_and_poll(file_ids=[file.id], name="my_vectorstore")

        # Create file search tool and agent
        file_search = FileSearchTool(vector_store_ids=[vector_store.id])
        agent = self.project_client.agents.create_agent(
            odel=self.model_deployment,
            name=self.file_search_agent_name,
            instructions="You are a helpful assistant and can search information from uploaded files",
            tools=file_search.definitions,
            tool_resources=file_search.resources,
        )

        # Create thread and process user message
        thread = self.project_client.agents.threads.create()
        self.project_client.agents.messages.create(thread_id=thread.id, role="user", content="Hello, what Contoso products do you know?")
        run = self.project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

        # Handle run status
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        # Print thread messages
        messages = self.project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        for message in messages:
            if message.run_id == run.id and message.text_messages:
                print(f"{message.role}: {message.text_messages[-1].text.value}")

        # Cleanup resources
        self.project_client.agents.vector_stores.delete(vector_store.id)
        self.project_client.agents.files.delete(file_id=file.id)
        self.project_client.agents.delete_agent(agent.id)
       