"""
PRODUCTION-GRADE AGENT - ReAct + Function Calling Loop
Implements proper multi-step tool chaining with while loop architecture
Correct OpenAI message handling and system prompt guidance

🔥 KEY IMPROVEMENTS:
- ✅ Fixed duplicate message bug
- ✅ Proper content parsing
- ✅ System prompt for guided reasoning
- ✅ Multi-step tool chaining with while loop
- ✅ Correct message loop (no reconstruction)
- ✅ Better model choice (gpt-4o)
"""

import json
import os
from typing import Any, Optional
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class ProductionLLMAgent:
    """
    Production-grade agent implementing:
    - ReAct (Reasoning + Acting) Pattern
    - Proper tool calling with multi-step chaining
    - Correct OpenAI message loop
    - System prompt for guided reasoning
    """
    
    def __init__(self, model: str = "gpt-4.1"):
        # Better model choice: gpt-4o for complex reasoning
        self.model = model
        self.max_iterations = 10  # Prevent infinite loops
        self.tools = self._define_tools()
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """System prompt to guide LLM for multi-step reasoning"""
        return """You are an intelligent reasoning agent.
Your task is to:
1. Break down problems into logical steps
2. Use available tools sequentially when needed
3. Continue using tools until the problem is fully solved
4. Only stop when you have the complete answer

Always think step-by-step:
- What is needed to solve this?
- Which tools should I use?
- Do I need to chain multiple tools?
- What is the final answer?

Be precise and complete in your reasoning."""
    
    def _define_tools(self) -> list:
        """Define available tools in OpenAI format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_numbers",
                    "description": "Add two numbers and return the result",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "number1": {
                                "type": "number",
                                "description": "The first number to add"
                            },
                            "number2": {
                                "type": "number",
                                "description": "The second number to add"
                            }
                        },
                        "required": ["number1", "number2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "multiply_numbers",
                    "description": "Multiply two numbers and return the result",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "number1": {
                                "type": "number",
                                "description": "The first number"
                            },
                            "number2": {
                                "type": "number",
                                "description": "The second number"
                            }
                        },
                        "required": ["number1", "number2"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "subtract_numbers",
                    "description": "Subtract two numbers (number1 - number2) and return the result",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "number1": {
                                "type": "number",
                                "description": "The number to subtract from"
                            },
                            "number2": {
                                "type": "number",
                                "description": "The number to subtract"
                            }
                        },
                        "required": ["number1", "number2"]
                    }
                }
            }
        ]
    
    def add_numbers(self, number1: float, number2: float) -> dict:
        """Execute addition"""
        result = number1 + number2
        return {
            "operation": "addition",
            "number1": number1,
            "number2": number2,
            "result": result,
            "status": "success"
        }
    
    def multiply_numbers(self, number1: float, number2: float) -> dict:
        """Execute multiplication"""
        result = number1 * number2
        return {
            "operation": "multiplication",
            "number1": number1,
            "number2": number2,
            "result": result,
            "status": "success"
        }
    
    def subtract_numbers(self, number1: float, number2: float) -> dict:
        """Execute subtraction"""
        result = number1 - number2
        return {
            "operation": "subtraction",
            "number1": number1,
            "number2": number2,
            "result": result,
            "status": "success"
        }
    
    def execute_tool(self, tool_name: str, tool_input: dict) -> dict:
        """Execute the requested tool"""
        print(f"\n   ⚙️  EXECUTING: {tool_name}")
        print(f"      Input: {json.dumps(tool_input, indent=2)}")
        
        if tool_name == "add_numbers":
            result = self.add_numbers(tool_input["number1"], tool_input["number2"])
        elif tool_name == "multiply_numbers":
            result = self.multiply_numbers(tool_input["number1"], tool_input["number2"])
        elif tool_name == "subtract_numbers":
            result = self.subtract_numbers(tool_input["number1"], tool_input["number2"])
        else:
            result = {"error": f"Unknown tool: {tool_name}", "status": "failed"}
        
        print(f"      ✅ Result: {result['result'] if 'result' in result else result}")
        return result
    
    def process_query(self, user_query: str) -> dict:
        """
        Process user query with multi-step tool chaining
        Implements proper ReAct + Function Calling Loop
        """
        print(f"\n{'='*100}")
        print(f"🤖 PRODUCTION AGENT - ReAct + Function Calling Loop")
        print(f"{'='*100}")
        print(f"\n📝 Query: {user_query}")
        print(f"🧠 Model: {self.model}")
        print(f"📋 Available Tools: {[tool['function']['name'] for tool in self.tools]}")
        
        # Initialize message history with system prompt
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        all_tool_calls = []
        iteration = 0
        final_response_text = ""
        
        # 🔄 MAIN AGENT LOOP - Multi-step tool chaining
        print(f"\n{'─'*100}")
        print("🔄 STARTING AGENT LOOP (while loop for multi-step chaining)")
        print(f"{'─'*100}")
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n[ITERATION {iteration}]")
            
            # Step 1: Call LLM
            print(f"   📞 Calling LLM...")
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    max_tokens=1024,
                    tools=self.tools,
                    tool_choice="auto",
                    messages=messages
                )
            except Exception as e:
                print(f"   ❌ LLM Error: {str(e)}")
                break
            
            # Step 2: Check finish reason
            finish_reason = response.choices[0].finish_reason
            print(f"   📌 Finish reason: {finish_reason}")
            
            # Step 3: ✅ FIXED - Extract model response text (CORRECT parsing)
            model_text = response.choices[0].message.content or ""
            if model_text:
                print(f"   💬 Model says: {model_text}")
                final_response_text = model_text
            
            # Step 4: Check for tool calls
            tool_calls = response.choices[0].message.tool_calls
            
            # If no tool calls and finish reason is "stop", we're done
            if not tool_calls or finish_reason == "stop":
                print(f"   ✅ No more tool calls - Agent complete")
                break
            
            # Step 5: ✅ FIXED - CORRECT MESSAGE HANDLING (No Duplication!)
            # Simply append the assistant's message (DO NOT reconstruct)
            messages.append(response.choices[0].message)
            
            # Step 6: Execute tool calls
            print(f"   🔧 Found {len(tool_calls)} tool call(s)")
            
            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)
                tool_id = tool_call.id
                
                print(f"\n      Tool: {tool_name}")
                result = self.execute_tool(tool_name, tool_input)
                
                tool_results.append({
                    "tool_call_id": tool_id,
                    "result": result
                })
                
                all_tool_calls.append({
                    "iteration": iteration,
                    "tool": tool_name,
                    "input": tool_input,
                    "output": result
                })
            
            # Step 7: ✅ FIXED - CORRECT MESSAGE LOOP (Clean, no duplicates!)
            # Append tool results - that's it!
            for tool_result in tool_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_result["tool_call_id"],
                    "content": json.dumps(tool_result["result"])
                })
            
            print(f"\n   ✅ Tool results added to message history")
        
        # Final Summary
        print(f"\n{'─'*100}")
        print(f"🏁 AGENT LOOP COMPLETE (Iterations: {iteration})")
        print(f"{'─'*100}")
        
        final_output = {
            "status": "completed",
            "query": user_query,
            "model": self.model,
            "iterations": iteration,
            "total_tool_calls": len(all_tool_calls),
            "tool_calls_log": all_tool_calls,
            "final_response": final_response_text
        }
        
        print(f"\n📊 Final Output:")
        print(json.dumps(final_output, indent=2))
        
        return final_output


# Main execution
def main():
    """Run the production-grade agent"""
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not set!")
        print("   Set it with: $env:OPENAI_API_KEY = 'sk-...'")
        return
    
    agent = ProductionLLMAgent(model="gpt-4o")
    
    # Test queries - including multi-step reasoning
    queries = [
        "8 aur 20 ko jama kro,and multiply krro 10"
         
    ]
    
    for query in queries:
        try:
            print("\n" + "="*100)
            response = agent.process_query(query)
            print(f"\n✅ SUCCESS\n")
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")


if __name__ == "__main__":
    main()
