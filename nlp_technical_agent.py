"""
AGENT 2: NLP, Data Retrieval & Process Automation Agent
Handles natural language processing, data extraction, and automation workflows
"""

import json
import re
from datetime import datetime

class NLPTechnicalAgent:
    """
    Specializes in:
    - Natural Language Processing (NLP)
    - Data retrieval from multiple sources
    - Process automation
    - Information extraction
    """
    
    def __init__(self):
        self.agent_name = "NLP & Technical Agent"
        self.capabilities = [
            "nlp_parse",
            "data_retrieval",
            "process_automation",
            "information_extraction"
        ]
        
        # Mock database - Customer info
        self.customer_db = {
            "CUST_001": {
                "customer_id": "CUST_001",
                "name": "Ali Ahmed",
                "dob": "15-Jan-1990",
                "phone": "03001234567",
                "email": "ali@example.com"
            }
        }
    
    def nlp_parse(self, user_query: str) -> dict:
        """Parse natural language query to extract intent and entities"""
        print(f"\n   🤖 [NLP AGENT] Parsing Query: '{user_query}'")
        
        # Extract bill ID
        bill_match = re.search(r"bill\s+(?:ki\s+)?id\s+(\d+)", user_query, re.IGNORECASE)
        bill_id = bill_match.group(1) if bill_match else None
        
        # Extract time (pattern: 9pm, 9PM, etc.)
        time_match = re.search(r"(\d{1,2})\s*(?:pm|PM|am|AM|bje|bjay)", user_query, re.IGNORECASE)
        time = f"{time_match.group(1)}:00 PM" if time_match else None
        
        # Extract intent
        intents = []
        if "troubleshoot" in user_query.lower() or "troubleshoot" in user_query or "theek" in user_query:
            intents.append("troubleshoot")
        if "schedule" in user_query.lower() or "scheduling" in user_query or "krdo" in user_query:
            intents.append("schedule")
        if "dob" in user_query.lower() or "batao" in user_query.lower() or "date" in user_query.lower():
            intents.append("get_personal_info")
        
        parsed = {
            "bill_id": bill_id,
            "scheduled_time": time,
            "intents": intents,
            "entities": {
                "bill_id": bill_id,
                "time": time
            }
        }
        
        print(f"      ✅ Intents Detected: {intents}")
        print(f"      ✅ Bill ID: {bill_id}")
        print(f"      ✅ Schedule Time: {time}")
        
        return parsed
    
    def data_retrieval(self, customer_id: str, data_type: str) -> dict:
        """Retrieve data from various sources"""
        print(f"\n   📊 [NLP AGENT] Retrieving Data: {data_type}")
        
        if customer_id in self.customer_db:
            customer = self.customer_db[customer_id]
            print(f"      ✅ Data Source: Customer Database")
            print(f"      ✅ Customer Found: {customer['name']}")
            
            if data_type == "dob":
                print(f"      ✅ Date of Birth: {customer['dob']}")
                return {"dob": customer['dob'], "status": "success"}
            
            elif data_type == "contact":
                print(f"      ✅ Contact: {customer['phone']}")
                return {"phone": customer['phone'], "email": customer['email'], "status": "success"}
            
            elif data_type == "profile":
                print(f"      ✅ Full Profile Retrieved")
                return customer
        
        return {"error": "Customer not found", "status": "failed"}
    
    def process_automation(self, workflow: list) -> dict:
        """Automate workflow processes"""
        print(f"\n   ⚙️  [NLP AGENT] Automating Workflow")
        
        automation_log = {
            "workflow": workflow,
            "steps_completed": [],
            "status": "in_progress"
        }
        
        for step in workflow:
            print(f"      🔄 Processing Step: {step}")
            automation_log["steps_completed"].append({
                "step": step,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            })
            print(f"      ✅ Step Complete: {step}")
        
        automation_log["status"] = "completed"
        print(f"      ✅ Workflow Automation Complete")
        
        return automation_log
    
    def information_extraction(self, query_data: dict) -> dict:
        """Extract and structure information from query"""
        print(f"\n   📝 [NLP AGENT] Extracting Information")
        
        extraction = {
            "query_intent": query_data.get("intents", []),
            "bill_id": query_data.get("bill_id"),
            "scheduled_time": query_data.get("scheduled_time"),
            "customer_id": "CUST_001",  # From parsed data
            "required_actions": []
        }
        
        # Determine required actions based on intents
        if "troubleshoot" in query_data.get("intents", []):
            extraction["required_actions"].append("resolve_billing_issue")
        if "schedule" in query_data.get("intents", []):
            extraction["required_actions"].append("schedule_appointment")
        if "get_personal_info" in query_data.get("intents", []):
            extraction["required_actions"].append("retrieve_customer_dob")
        
        print(f"      ✅ Required Actions: {extraction['required_actions']}")
        
        return extraction


def execute_nlp_agent(user_query: str) -> dict:
    """
    Execute NLP & Technical agent workflow
    """
    print("\n" + "="*100)
    print("🔬 AGENT 2: NLP & TECHNICAL AGENT")
    print("="*100)
    
    agent = NLPTechnicalAgent()
    results = {
        "agent": agent.agent_name,
        "query": user_query,
        "operations": []
    }
    
    # Operation 1: NLP Parsing
    print("\n[OPERATION 1] NLP Query Parsing")
    parsed_data = agent.nlp_parse(user_query)
    results["operations"].append({
        "operation": "nlp_parse",
        "result": parsed_data
    })
    results["parsed_data"] = parsed_data  # For use in orchestrator
    
    # Operation 2: Information Extraction
    print("\n[OPERATION 2] Information Extraction")
    extracted = agent.information_extraction(parsed_data)
    results["operations"].append({
        "operation": "information_extraction",
        "result": extracted
    })
    results["extracted_data"] = extracted
    
    # Operation 3: Data Retrieval
    print("\n[OPERATION 3] Data Retrieval")
    dob_data = agent.data_retrieval("CUST_001", "dob")
    results["operations"].append({
        "operation": "data_retrieval",
        "result": dob_data
    })
    results["dob_data"] = dob_data
    
    # Operation 4: Process Automation Planning
    print("\n[OPERATION 4] Process Automation")
    workflow = extracted.get("required_actions", [])
    automation = agent.process_automation(workflow)
    results["operations"].append({
        "operation": "process_automation",
        "result": automation
    })
    
    return results
