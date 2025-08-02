import os
from azure.ai.agents.models import ListSortOrder

from aif_agent import AIF_Agent
from aif_agent_client import AIF_AgentClient

# Agent Triage for Multi-Agent solution using Azure AI Foundary.
class AIF_AgentTriageClient(AIF_AgentClient):
    def __init__(self, name, support_level):
        try:
            type = os.getenv("TRIAGE_AGENT_NAME")
            super().__init__(name, type)            
            self.support_level = support_level
                
            # Priority agent definition
            self.priority_agent_name = "priority_agent"
            self.priority_agent_desc = "Assess the priority of a ticket"
            self.priority_agent_instructions = """
            Assess how urgent a ticket is based on its description.

            Respond with one of the following levels:
            - High: User-facing or blocking issues
            - Medium: Time-sensitive but not breaking anything
            - Low: Cosmetic or non-urgent tasks

            Only output the urgency level and a very brief explanation.
            """

            # Team agent definition
            self.team_agent_name = "team_agent"
            self.team_agent_desc = "Determines which team should take the ticket"
            self.team_agent_instructions = """
            Decide which team should own each ticket.

            Choose from the following teams:
            - Frontend
            - Backend
            - Infrastructure
            - Marketing

            Base your answer on the content of the ticket. Respond with the team name and a very brief explanation.
            """

            # Effort agent definition
            self.effort_agent_name = "effort_agent"
            self.effort_agent_desc = "Determines the effort required to complete the ticket"
            self.effort_agent_instructions = """
            Estimate how much work each ticket will require.

            Use the following scale:
            - Small: Can be completed in a day
            - Medium: 2-3 days of work
            - Large: Multi-day or cross-team effort

            Base your estimate on the complexity implied by the ticket. Respond with the effort level and a brief justification.
            """
            # Instructions for the primary agent        
            self.triage_agent_instructions = """
            Triage the given ticket. Use the connected tools to determine the ticket's priority, 
            which team it should be assigned to, and how much effort it may take.
            """
        except Exception as ex:
            print(ex)

    # create triage agent.
    def create_triage_agent(self):
        try:
            self.agent = self.agent_client.create_agent(
                model=self.model_deployment,
                name=self.agent_name,
                instructions=self.triage_agent_instructions,
                tools=[
                    self.priority_agent.agent_tool.definitions[0],
                    self.team_agent.agent_tool.definitions[0],
                    self.effort_agent.agent_tool.definitions[0]
                ]
            )
        except Exception as ex:
            print(ex)

    # function to create multiple agents.
    def create_agents(self):
        try:            
            # Create the priority agent and connected tool using Azure AI agent service
            self.priority_agent = AIF_Agent (self.agent_client, self.priority_agent_name, self.priority_agent_instructions,self.priority_agent_desc)            
            # Create the team agent and connected tool using Azure AI agent service            
            self.team_agent = AIF_Agent (self.agent_client, self.team_agent_name, self.team_agent_instructions,self.team_agent_desc)
            # Create the effort agent and connected tool using Azure AI agent service
            self.effort_agent = AIF_Agent (self.agent_client, self.effort_agent_name, self.effort_agent_instructions,self.effort_agent_desc)
            # Create a main agent with the Connected Agent tools
            self.create_triage_agent()            
        except Exception as ex:
            print(ex)
            
    # function to display the log of the conversation.
    def display_conversation_log(self):
        try:
            # Get the conversation history
            print("\nConversation Log:\n")
            messages = self.agent_client.messages.list(thread_id=self.thread.id, order=ListSortOrder.ASCENDING)
            for message in messages:
                if message.text_messages:
                    last_msg = message.text_messages[-1]
                    print(f"{message.role}: {last_msg.text.value}\n")            
        except Exception as ex:
            print(ex)
    
    #delete agents
    def disconnect(self):
        try:
            # Delete the agent when done            
            self.agent_client.delete_agent(self.agent.id)            
            # Delete the connected agents when done
            self.agent_client.delete_agent(self.priority_agent.agent.id)            
            self.agent_client.delete_agent(self.team_agent.agent.id)            
            self.agent_client.delete_agent(self.effort_agent.agent.id)            
        except Exception as ex:
            print(ex)