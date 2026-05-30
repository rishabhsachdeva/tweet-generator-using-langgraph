"""
Test script for the multi-model LangGraph system
"""

from groq_langgraph_system import GroqLangGraphSystem

def test_funny_tweet():
    """Test funny tweet generation"""
    print("🧪 Testing Funny Tweet Generation")
    print("=" * 50)
    
    system = GroqLangGraphSystem(humor_threshold=8.0, max_iterations=3)
    result = system.generate_tweet("cats", "funny")
    
    print(f"✅ Success: {result['success']}")
    print(f"📢 Tweet: {result['tweet']}")
    print(f"📊 Score: {result['score']}/10")
    print(f"🔄 Iterations: {result['iterations']}")
    print(f"🔧 Workflow: {result['workflow_type']}")
    
    if result['iteration_history']:
        print("\n📋 Iteration History:")
        for iteration in result['iteration_history']:
            print(f"  {iteration['iteration']}. Score: {iteration['score']}/10 - {iteration['tweet'][:50]}...")

def test_sad_tweet():
    """Test sad tweet generation"""
    print("\n🧪 Testing Sad Tweet Generation")
    print("=" * 50)
    
    system = GroqLangGraphSystem(humor_threshold=8.0, max_iterations=3)
    result = system.generate_tweet("loss", "sad")
    
    print(f"✅ Success: {result['success']}")
    print(f"📢 Tweet: {result['tweet']}")
    print(f"📊 Score: {result['score']}/10")
    print(f"🔄 Iterations: {result['iterations']}")
    print(f"🔧 Workflow: {result['workflow_type']}")

def test_cheerful_tweet():
    """Test cheerful tweet generation"""
    print("\n🧪 Testing Cheerful Tweet Generation")
    print("=" * 50)
    
    system = GroqLangGraphSystem(humor_threshold=8.0, max_iterations=3)
    result = system.generate_tweet("morning", "cheerful")
    
    print(f"✅ Success: {result['success']}")
    print(f"📢 Tweet: {result['tweet']}")
    print(f"📊 Score: {result['score']}/10")
    print(f"🔄 Iterations: {result['iterations']}")
    print(f"🔧 Workflow: {result['workflow_type']}")

def test_informative_tweet():
    """Test informative tweet generation"""
    print("\n🧪 Testing Informative Tweet Generation")
    print("=" * 50)
    
    system = GroqLangGraphSystem(humor_threshold=8.0, max_iterations=3)
    result = system.generate_tweet("technology", "informative")
    
    print(f"✅ Success: {result['success']}")
    print(f"📢 Tweet: {result['tweet']}")
    print(f"📊 Score: {result['score']}/10")
    print(f"🔄 Iterations: {result['iterations']}")
    print(f"🔧 Workflow: {result['workflow_type']}")

if __name__ == "__main__":
    print("🚀 Testing Multi-Model LangGraph System")
    print("=" * 60)
    
    # Test all tweet types
    test_funny_tweet()
    test_sad_tweet()
    test_cheerful_tweet()
    test_informative_tweet()
    
    print("\n✅ All tests completed!")
