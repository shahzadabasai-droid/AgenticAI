"""
AGENT 1: Billing, Troubleshooting, Scheduling & Decision-Making Agent
Handles business logic, billing operations, issue resolution, and scheduling
"""

import json
from datetime import datetime

class BillingAgent:
    """
    Specializes in:
    - Billing operations
    - Issue troubleshooting
    - Scheduling appointments/tasks
    - Decision making
    """
    
    def __init__(self):
        self.agent_name = "Billing & Operations Agent"
        self.capabilities = [
            "billing_lookup",
            "troubleshoot_issue",
            "schedule_appointment",
            "make_decision"
        ]
        
        # Mock database
        self.billing_db = {
            "2": {
                "bill_id": "2",
                "amount": 5000,
                "status": "pending",
                "issue": "Payment failed",
                "customer_id": "CUST_001"
            }
        }
        
        self.scheduling_db = {}
    
    def billing_lookup(self, bill_id: str) -> dict:
        """Look up billing information"""
        print(f"\n   💳 [BILLING AGENT] Looking up Bill ID: {bill_id}")
        
        if bill_id in self.billing_db:
            bill_info = self.billing_db[bill_id]
            print(f"      ✅ Bill Found:")
            print(f"         - Amount: Rs. {bill_info['amount']}")
            print(f"         - Status: {bill_info['status']}")
            print(f"         - Issue: {bill_info['issue']}")
            return bill_info
        else:
            print(f"      ❌ Bill not found")
            return {"error": "Bill not found"}
    
    def troubleshoot_issue(self, bill_id: str) -> dict:
        """Troubleshoot billing issue"""
        print(f"\n   🔧 [BILLING AGENT] Troubleshooting Bill ID: {bill_id}")
        
        if bill_id in self.billing_db:
            issue = self.billing_db[bill_id]["issue"]
            print(f"      🔍 Identified Issue: {issue}")
            print(f"      ✅ Resolution: Retrying payment gateway...")
            print(f"      ✅ Status Update: Issue Resolved")
            
            self.billing_db[bill_id]["status"] = "resolved"
            return {
                "bill_id": bill_id,
                "issue": issue,
                "resolution": "Payment retry successful",
                "new_status": "resolved"
            }
        return {"error": "Bill not found"}
    
    def schedule_appointment(self, bill_id: str, time: str) -> dict:
        """Schedule appointment/payment"""
        print(f"\n   📅 [BILLING AGENT] Scheduling for Bill ID: {bill_id}")
        print(f"      ⏰ Scheduled Time: {time}")
        
        self.scheduling_db[bill_id] = {
            "bill_id": bill_id,
            "scheduled_time": time,
            "scheduled_date": datetime.now().strftime("%Y-%m-%d"),
            "type": "payment_follow_up"
        }
        
        print(f"      ✅ Scheduled Successfully")
        return self.scheduling_db[bill_id]
    
    def make_decision(self, context: dict) -> dict:
        """Make business decision based on context"""
        print(f"\n   ⚖️  [BILLING AGENT] Making Decision")
        print(f"      📊 Context: {json.dumps(context, indent=3)}")
        
        decision = {
            "action": "proceed_with_billing",
            "priority": "high",
            "next_steps": [
                "1. Resolve billing issue",
                "2. Schedule payment reminder",
                "3. Send notification to customer"
            ]
        }
        
        print(f"      ✅ Decision: {decision['action']}")
        return decision


def execute_billing_agent(user_query: str, extracted_data: dict) -> dict:
    """
    Execute billing agent workflow
    """
    print("\n" + "="*100)
    print("👤 AGENT 1: BILLING & OPERATIONS AGENT")
    print("="*100)
    
    agent = BillingAgent()
    results = {
        "agent": agent.agent_name,
        "query": user_query,
        "operations": []
    }
    
    # Extract bill_id and time from data
    bill_id = extracted_data.get("bill_id")
    scheduled_time = extracted_data.get("scheduled_time")
    
    # Operation 1: Lookup billing
    print("\n[OPERATION 1] Billing Lookup")
    billing_info = agent.billing_lookup(bill_id)
    results["operations"].append({
        "operation": "billing_lookup",
        "result": billing_info
    })
    
    # Operation 2: Troubleshoot
    print("\n[OPERATION 2] Troubleshooting")
    troubleshoot_result = agent.troubleshoot_issue(bill_id)
    results["operations"].append({
        "operation": "troubleshoot",
        "result": troubleshoot_result
    })
    
    # Operation 3: Schedule
    print("\n[OPERATION 3] Scheduling")
    schedule_result = agent.schedule_appointment(bill_id, scheduled_time)
    results["operations"].append({
        "operation": "schedule",
        "result": schedule_result
    })
    
    # Operation 4: Decision
    print("\n[OPERATION 4] Decision Making")
    decision = agent.make_decision({
        "bill_id": bill_id,
        "troubleshoot_status": "resolved",
        "scheduled": True
    })
    results["operations"].append({
        "operation": "decision",
        "result": decision
    })
    
    return results
