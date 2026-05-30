"""
Flask Frontend for LangGraph Joke Generator
Web interface with user input, score display, and state history viewer
"""

from flask import Flask, render_template, request, jsonify
from groq_langgraph_system import GroqLangGraphSystem
import threading
import time

app = Flask(__name__)

# Global variable to store the system and results
joke_system = GroqLangGraphSystem(humor_threshold=8.0, max_iterations=5)
current_result = None
generating = False

@app.route('/')
def index():
    """Main page with joke generator interface"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_tweet():
    """Generate tweet endpoint"""
    global current_result, generating
    
    if generating:
        return jsonify({"error": "Already generating a tweet. Please wait."})
    
    data = request.get_json()
    topic = data.get('topic', '').strip()
    tweet_type = data.get('tweet_type', 'funny').strip()
    
    if not topic:
        return jsonify({"error": "Please enter a topic"})
    
    valid_types = ['funny', 'sad', 'cheerful', 'informative']
    if tweet_type not in valid_types:
        return jsonify({"error": f"Invalid tweet type. Must be one of: {', '.join(valid_types)}"})
    
    generating = True
    
    try:
        # Generate the tweet
        result = joke_system.generate_tweet(topic, tweet_type)
        current_result = result
        
        return jsonify({
            "success": True,
            "tweet": result.get('tweet', ''),
            "score": result.get('score', 0),
            "iterations": result.get('iterations', 0),
            "success_status": result.get('success', False),
            "workflow_type": result.get('workflow_type', ''),
            "iteration_history": result.get('iteration_history', []),
            "tweet_type": tweet_type
        })
        
    except Exception as e:
        return jsonify({"error": str(e)})
    
    finally:
        generating = False

@app.route('/history')
def get_history():
    """Get current result history"""
    global current_result
    
    if current_result and current_result.get('iteration_history'):
        return jsonify({
            "success": True,
            "history": current_result['iteration_history']
        })
    
    return jsonify({"success": False, "error": "No history available"})

@app.route('/status')
def get_status():
    """Get generation status"""
    global generating, current_result
    
    return jsonify({
        "generating": generating,
        "has_result": current_result is not None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
