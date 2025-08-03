import os
from azure.ai.agents.models import McpTool, ListSortOrder
from aif_agent_client import AIF_AgentClient

# AI Foundary Agent Client
class AIF_MCPAgentClient(AIF_AgentClient):
    
    # constructor    
    def __init__(self, name, data_domain):
        try:
            type = os.getenv("MCP_AGENT_NAME")
            super().__init__(name, type)
            self.data_domain = data_domain 
            # MCP server configuration
            self.mcp_server_url = os.getenv("MCP_SERVER_URL")
            self.mcp_server_label = os.getenv("MCP_SERVER_LABEL")  
            self.mcp_key = os.getenv("MCP_KEY")  
            self.mcp_value = os.getenv("MCP_VALUE")  
        except Exception as ex:
            print(ex)

    # function to define the toolset.
    def initiate_mcp_tool(self):
        try:
            # Initialize agent MCP tool
            self.mcp_tool = McpTool(
                server_label=self.mcp_server_label,
                server_url=self.mcp_server_url,
            )                        
        except Exception as ex:
            print(ex)
            
    # function to create an agent.
    def create_agents(self):
        try:
            # Initiate the MCP tool for the agent.
            self.initiate_mcp_tool()

            # Create a new agent with the mcp tool definitions
            self.agent = self.agent_client.create_agent(
                model=self.model_deployment,
                name=self.agent_name,
                instructions="""
                You have access to an MCP server called `microsoft.docs.mcp` - this tool allows you to 
                search through Microsoft's latest official documentation. Use the available MCP tools 
                to answer questions and perform tasks.""",
                tools=self.mcp_tool.definitions,
            )           
        except Exception as ex:
            print(ex)
    
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
                              
                # Update mcp tool headers
                self.mcp_tool.update_headers(self.mcp_key, self.mcp_value)
                # Set approval mode
                self.mcp_tool.set_approval_mode("never")

                # Create and process Agent run in thread
                print("Processing the request. Please wait.")
                # Create and process agent run in thread with MCP tools
                self.run = self.agent_client.runs.create_and_process(thread_id=self.thread.id, agent_id=self.agent.id, tool_resources=self.mcp_tool.resources)                
                # Check the run status for failures
                if self.run.status == "failed":
                    print(f"Run failed: {self.run.last_error}")  
                #display the log of the conversation.
                self.display_conversation_log()                   
        except Exception as ex:
            print(ex)

    # function to define the code interpreter.
    def display_conversation_log(self):
        try:           
            # Display run steps and tool calls
            run_steps = self.agent_client.run_steps.list(thread_id=self.thread.id, run_id=self.run.id)
            for step in run_steps:
                print(f"Step {step['id']} status: {step['status']}")

                # Check if there are tool calls in the step details
                step_details = step.get("step_details", {})
                tool_calls = step_details.get("tool_calls", [])

                if tool_calls:
                    # Display the MCP tool call details
                    print("  MCP Tool calls:")
                    for call in tool_calls:
                        print(f"    Tool Call ID: {call.get('id')}")
                        print(f"    Type: {call.get('type')}")
                        print(f"    Type: {call.get('name')}")

                print()  # add an extra newline between steps          
            
            #show the last conversation
            super().display_conversation_log()

        except Exception as ex:
            print(ex)
    
        