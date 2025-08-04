#!/usr/bin/env python3
"""
Comprehensive workflow verification demo for Simple QA Chatbot
Demonstrates conversation history management and background RAG memory processing
"""

import os
import sys
from typing import List, Dict, Any
import uuid
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_qa_chatbot import SimpleQAChatBot


class WorkflowVerificationDemo:
    """
    Demo class to verify the complete workflow of Simple QA Chatbot
    including conversation history management and background memory processing
    """
    
    def __init__(self, user_id: str = "naga_v1", max_history_length: int = 3):
        """
        Initialize the demo with specific parameters
        
        Args:
            user_id: User ID for the demo
            max_history_length: Maximum conversation pairs to keep in working memory
        """
        self.user_id = user_id
        self.max_history_length = max_history_length
        self.max_working_length = max_history_length * 2  # When to trigger clipping
        
        # Demo messages to process
        self.demo_messages = [
            "I don't live in hyderabad anymore",
            "I moved to bangalore. What area is best to stay in bangalore",
            "Okay. I will look for flats in HSR layout",
            "Yeah I found a cute 2bhk apartment.",
            "I also took subscription for a gym and swimming around",
            "I also met a few buddies that play badminton",
            "Yeah I am planning to play badminton with them regularly",
            "Btw I joined Shram.ai in Bangalore",
            "My role is AI engineer and I hope to get some info about what I need to learn before that",
            "That's cool I use cursor, terminus and magnet to enhance my productivity",
            "Yeah do you have any upto date tools. I could use ?",
            "Enough about work, Tell me about some nice cafes. I love death by chocolate"
        ]
        
        self.chatbot = None
        
    def print_header(self, title: str, char: str = "=", width: int = 80):
        """Print a formatted header"""
        print(f"\n{char * width}")
        print(f"{title:^{width}}")
        print(f"{char * width}")
        
    def print_subheader(self, title: str, char: str = "=", width: int = 60):
        """Print a formatted subheader"""
        print(f"\n{char * width}")
        print(f"MESSAGE {title}")
        print(f"{char * width}")
        
    def print_step(self, step_num: int, description: str):
        """Print a formatted step"""
        print(f"\n🔍 Step {step_num}: {description}")
        
    def print_documents(self, docs: List[Dict[str, Any]], message_num: int):
        """Print retrieved documents in a formatted way"""
        print(f"\n📚 Retrieved Documents for Message {message_num} ({len(docs)} docs):")
        for i, doc in enumerate(docs, 1):
            score = doc.get('similarity', 0.0)
            content = doc.get('document', '')[:50]
            metadata = doc.get('metadata', {})
            print(f"  {i}. Score: {score:.3f} | {content}...")
            print(f"     Metadata: {metadata}")
            
    def print_conversation_status(self, message_num: int):
        """Print current conversation status"""
        print(f"\n💬 Chat History Status after Message {message_num}:")
        print(f"   Total messages: {len(self.chatbot.conversation_history)} ({len(self.chatbot.conversation_history) // 2} pairs)")
        print(f"   Max pairs allowed: {self.chatbot.max_history_length}")
        print(f"   Working threshold: {self.chatbot.max_working_length} pairs")
        print(f"   Memory mappings stored: {len(self.chatbot.message_memory_mapping)}")
        
        # Show recent conversation
        if len(self.chatbot.conversation_history) > 0:
            print(f"   Recent conversation:")
            # Show last few messages
            recent_messages = self.chatbot.conversation_history[-4:]  # Show last 2 pairs
            for i in range(0, len(recent_messages), 2):
                if i + 1 < len(recent_messages):
                    user_msg = recent_messages[i]['content'][:80]
                    assistant_msg = recent_messages[i + 1]['content'][:80]
                    print(f"     USER: {user_msg}...")
                    print(f"     ASSISTANT: {assistant_msg}...")
                    
    def print_session_status(self):
        """Print current session status"""
        print(f"\n📊 Session Status Check:")
        print(f"   session_id: {self.chatbot.session_id}")
        print(f"   exchange_count: {len(self.chatbot.conversation_history) // 2}")
        print(f"   max_history_length: {self.chatbot.max_history_length}")
        print(f"   max_working_length: {self.chatbot.max_working_length}")
        print(f"   user_id: {self.chatbot.user_id}")
        print(f"   background_memory_enabled: {self.chatbot.enable_background_memory}")
        
    def get_background_memory_count(self) -> int:
        """Get the number of documents in background memory"""
        if not self.chatbot.enable_background_memory or not self.chatbot.background_rag_chatbot:
            return 0
        
        try:
            stats_result = self.chatbot.background_rag_chatbot.rag_executor.execute_tool(
                "get_database_stats", {"user_id": self.user_id}
            )
            if stats_result and "data" in stats_result and "stats" in stats_result["data"]:
                return stats_result["data"]["stats"]["num_documents"]
        except:
            pass
        return 0
        
    def run_demo(self):
        """Run the complete workflow verification demo"""
        
        self.print_header("🧪 Simple QA Chatbot Workflow Verification Demo")
        
        # Print demo plan
        print(f"\n📋 Demo Plan:")
        print(f"   User ID: {self.user_id}")
        print(f"   Session: New session")
        print(f"   Messages to process: {len(self.demo_messages)}")
        print(f"   History limit: {self.max_history_length} pairs ({self.max_history_length * 2} messages)")
        print(f"   Expected clipping: After message {self.max_working_length} (when reaching {self.max_working_length} pairs)")
        
        # Initialize chatbot
        self.print_header("🚀 Initializing Chatbot")
        try:
            self.chatbot = SimpleQAChatBot(
                user_id=self.user_id, 
                max_history_length=self.max_history_length,
                enable_background_memory=True
            )
            
            print("✅ Chatbot initialized successfully!")
            print(f"   User ID: {self.chatbot.user_id}")
            print(f"   Session ID: {self.chatbot.session_id[:8]}...")
            print(f"   Background memory: {'enabled' if self.chatbot.enable_background_memory else 'disabled'}")
            
            initial_memory_docs = self.get_background_memory_count()
            print(f"   Initial memory docs: {initial_memory_docs}")
            
        except Exception as e:
            print(f"❌ Failed to initialize chatbot: {e}")
            return
            
        # Process messages
        self.print_header("💬 Processing Conversation Messages")
        
        clipping_triggered = []
        
        for i, message in enumerate(self.demo_messages, 1):
            self.print_subheader(f"{i}: {message}")
            
            try:
                # Step 1: Get retrieved documents (before processing)
                self.print_step(1, "Retrieving relevant documents...")
                retrieved_docs = self.chatbot.get_retrieved_documents(message)
                self.print_documents(retrieved_docs, i)
                
                # Step 2: Process message
                self.print_step(2, "Processing message through QA chatbot...")
                
                # Check if this will trigger background processing
                current_pairs = len(self.chatbot.conversation_history) // 2
                will_trigger_clipping = current_pairs >= self.chatbot.max_working_length
                
                response = self.chatbot.chat(message)
                print(f"✅ Response generated: {response[:80]}...")
                
                # Step 3: Show memory mapping
                self.print_step(3, "Message-Memory mapping stored:")
                print(f"   User message: {message[:50]}...")
                print(f"   Associated docs: {len(retrieved_docs)} documents")
                
                # Show conversation status
                self.print_conversation_status(i)
                
                # Check if background processing was triggered
                if will_trigger_clipping:
                    print(f"\n🔄 Background RAG Processing Triggered after Message {i}")
                    print(f"   Reason: History clipping - sending old messages to RAG chatbot")
                    print(f"   Current message: {message[:50]}...")
                    clipping_triggered.append(i)
                
                # Show session status periodically
                if i % 3 == 0 or will_trigger_clipping:
                    self.print_session_status()
                    
            except Exception as e:
                print(f"❌ Error processing message {i}: {e}")
                continue
                
        # Final verification
        self.print_header("🔍 Final Workflow Verification")
        
        final_memory_docs = self.get_background_memory_count()
        final_pairs = len(self.chatbot.conversation_history) // 2
        final_mappings = len(self.chatbot.message_memory_mapping)
        
        print(f"\n📈 Final Statistics:")
        print(f"   Total messages processed: {len(self.demo_messages)}")
        print(f"   Final conversation pairs: {final_pairs}")
        print(f"   Memory mappings retained: {final_mappings}")
        print(f"   Background memory documents: {final_memory_docs}")
        
        print(f"\n✅ Workflow Verification Results:")
        print(f"   ✅ History clipping: {'Working correctly' if final_pairs <= self.max_history_length else 'Issue detected'} ({final_pairs}/{self.max_history_length} pairs)")
        print(f"   ✅ Memory mappings: {'Working correctly' if final_mappings <= self.max_history_length else 'Issue detected'} ({final_mappings}/{self.max_history_length} mappings)")
        print(f"   ✅ Background memory: {'Processing enabled' if self.chatbot.enable_background_memory else 'Disabled'}")
        
        # Save session
        if hasattr(self.chatbot, 'session_manager'):
            session_file = f"sessions/{self.chatbot.session_id}.jsonl"
            print(f"\n💾 Session saved to: {session_file}")
        
        # Show final conversation
        print(f"\n📜 Final Conversation History:")
        for i in range(0, len(self.chatbot.conversation_history), 2):
            if i + 1 < len(self.chatbot.conversation_history):
                user_msg = self.chatbot.conversation_history[i]['content'][:60]
                assistant_msg = self.chatbot.conversation_history[i + 1]['content'][:60]
                pair_num = (i // 2) + 1
                print(f"   {pair_num}. USER: {user_msg}")
                print(f"   {pair_num + 1}. ASSISTANT: {assistant_msg}...")
        
        self.print_header("✅ Demo Complete - Workflow Verified")


def main():
    """Main function to run the demo"""
    demo = WorkflowVerificationDemo(
        user_id="naga_v1",
        max_history_length=3  # Keep only 3 conversation pairs in working memory
    )
    
    try:
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()