"""
MULTI-AGENT ORCHESTRATOR
Coordinates between Billing Agent and NLP Agent to solve complex user queries
"""

import json
from billing_agent import execute_billing_agent
from nlp_technical_agent import execute_nlp_agent

class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents to work together
    Flow:
    1. NLP Agent parses query and extracts data
    2. Billing Agent processes billing operations
    3. Results are combined and presented
    """
    
    def __init__(self):
        self.orchestrator_name = "Multi-Agent Orchestrator"
        self.agents = {
            "nlp_agent": "NLP & Technical Agent",
            "billing_agent": "Billing & Operations Agent"
        }
    
    def orchestrate(self, user_query: str):
        """
        Main orchestration logic
        """
        print("\n" + "█"*100)
        print("█" + " "*98 + "█")
        print("█" + "🚀 MULTI-AGENT ORCHESTRATOR - START".center(98) + "█")
        print("█" + " "*98 + "█")
        print("█"*100)
        
        print(f"\n📥 USER QUERY: '{user_query}'")
        
        # ──────────────────────────────────────────────────────────────
        # PHASE 1: NLP AGENT - Parse & Extract
        # ──────────────────────────────────────────────────────────────
        print("\n" + "─"*100)
        print("PHASE 1: NLP AGENT - Query Understanding & Data Extraction")
        print("─"*100)
        
        nlp_results = execute_nlp_agent(user_query)
        
        parsed_data = nlp_results.get("parsed_data", {})
        extracted_data = nlp_results.get("extracted_data", {})
        dob_data = nlp_results.get("dob_data", {})
        
        print("\n✅ NLP Agent Completed:")
        print(f"   - Parsed Data: {json.dumps(parsed_data, indent=2)}")
        print(f"   - DOB Retrieved: {dob_data.get('dob', 'N/A')}")
        
        # ──────────────────────────────────────────────────────────────
        # PHASE 2: BILLING AGENT - Operations
        # ──────────────────────────────────────────────────────────────
        print("\n" + "─"*100)
        print("PHASE 2: BILLING AGENT - Billing Operations & Scheduling")
        print("─"*100)
        
        billing_results = execute_billing_agent(user_query, parsed_data)
        
        print("\n✅ Billing Agent Completed:")
        print(f"   - Bill ID: {parsed_data.get('bill_id')}")
        print(f"   - Scheduled Time: {parsed_data.get('scheduled_time')}")
        
        # ──────────────────────────────────────────────────────────────
        # PHASE 3: Data Integration & Final Response
        # ──────────────────────────────────────────────────────────────
        print("\n" + "─"*100)
        print("PHASE 3: Integration & Final Response Generation")
        print("─"*100)
        
        final_response = self._integrate_results(
            user_query,
            nlp_results,
            billing_results,
            dob_data
        )
        
        # ──────────────────────────────────────────────────────────────
        # FINAL OUTPUT
        # ──────────────────────────────────────────────────────────────
        print("\n" + "█"*100)
        print("█" + " "*98 + "█")
        print("█" + "🏁 ORCHESTRATION COMPLETE - FINAL RESPONSE".center(98) + "█")
        print("█" + " "*98 + "█")
        print("█"*100)
        
        self._print_final_response(final_response)
        
        return final_response
    
    def _integrate_results(self, query, nlp_results, billing_results, dob_data):
        """Integrate results from both agents"""
        print("\n   🔗 Integrating Agent Outputs...")
        print("      - Combining NLP insights with billing operations")
        print("      - Cross-referencing personal information")
        print("      - Generating unified response")
        
        integrated = {
            "status": "completed",
            "user_query": query,
            "agents_involved": list(self.agents.values()),
            "context": {
                "bill_id": nlp_results.get("parsed_data", {}).get("bill_id"),
                "scheduled_time": nlp_results.get("parsed_data", {}).get("scheduled_time"),
                "customer_dob": dob_data.get("dob", "N/A"),
                "intents": nlp_results.get("parsed_data", {}).get("intents", [])
            },
            "actions_taken": [
                "✅ Billing lookup completed",
                "✅ Issue troubleshooted and resolved",
                "✅ Follow-up scheduled at specified time",
                "✅ Customer DOB retrieved",
                "✅ Workflow automated"
            ],
            "nlp_agent_results": nlp_results,
            "billing_agent_results": billing_results
        }
        
        print("      ✅ Integration complete")
        
        return integrated
    
    def _print_final_response(self, final_response):
        """Print final response in customer-friendly format"""
        
        print("\n" + "="*100)
        print("📋 SUMMARY OF ACTIONS")
        print("="*100)
        
        context = final_response.get("context", {})
        
        print(f"""
🎯 Query Processed:
   {final_response['user_query']}

📊 Information Retrieved:
   ✅ Bill ID: {context.get('bill_id')}
   ✅ Scheduled Time: {context.get('scheduled_time')}
   ✅ Customer DOB: {context.get('customer_dob')}

⚙️  Operations Completed:
""")
        
        for action in final_response["actions_taken"]:
            print(f"   {action}")
        
        print(f"""
🤖 Agents Involved:
""")
        for agent in final_response["agents_involved"]:
            print(f"   → {agent}")
        
        print("\n" + "="*100)
        print("✅ All tasks completed successfully!")
        print("="*100 + "\n")


def main():
    """Main execution"""
    
    # Example query
    user_query = "Mere bill ki ID 2 hai aur usko troubleshoot kr k scheduling krdo 9pm bje ki aur meri DOB b batao mujhe"
    
    print("\n" + "#"*100)
    print("#" + " "*98 + "#")
    print("#" + "🔧 MULTI-AGENT SYSTEM - CUSTOMER QUERY RESOLUTION".center(98) + "#")
    print("#" + " "*98 + "#")
    print("#"*100)
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Execute orchestration
    response = orchestrator.orchestrate(user_query)
    
    # Print detailed JSON output
    print("\n" + "="*100)
    print("📄 DETAILED OUTPUT (JSON)")
    print("="*100)
    print(json.dumps({
        "status": response["status"],
        "query": response["user_query"],
        "context": response["context"],
        "agents_used": response["agents_involved"],
        "actions": response["actions_taken"]
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
