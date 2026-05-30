"""
Proper LangGraph Joke Generator with State Reducers
Uses LangGraph StateGraph with conditional routing and state management
"""

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Dict, List, Optional, TypedDict, Annotated
import operator
import requests
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Define the state with proper typing
class JokeState(TypedDict):
    """State for the tweet generation workflow"""
    topic: str
    tweet_type: str
    current_tweet: str
    current_score: float
    is_funny: bool
    iteration: int
    max_iterations: int
    humor_threshold: float
    iteration_history: Annotated[List[Dict], operator.add]
    feedback: str
    final_tweet: str
    final_score: float
    success: bool
    error: str

class GroqLLM:
    """Groq LLM integration with multi-model support"""
    
    def __init__(self, model="llama-3.1-8b-instant"):
        self.default_model = model
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.available = self._check_groq()
        
        # Optimize models for different tweet types
        self.model_specialists = {
            "funny": "llama-3.1-70b-instant",      # Most creative for humor
            "sad": "mixtral-8x7b-32768",           # Good emotional depth
            "cheerful": "llama-3.1-8b-instant",    # Fast positive content
            "informative": "llama-3.1-8b-instant"   # Efficient factual content
        }
    
    def get_model_for_type(self, tweet_type):
        """Get the optimal model for a specific tweet type"""
        return self.model_specialists.get(tweet_type, self.default_model)
    
    def _check_groq(self):
        """Check if Groq API key is available"""
        if self.api_key:
            print(f"✅ Groq API key found! Using model: {self.default_model}")
            return True
        else:
            print("❌ Groq API key not found, using fallback")
            return False
    
    def invoke(self, prompt, tweet_type=None):
        """Generate response using Groq API with optimal model for tweet type"""
        if not self.available:
            return self._fallback_response(prompt, tweet_type)
        
        try:
            # Select the optimal model for this tweet type
            model = self.get_model_for_type(tweet_type) if tweet_type else self.default_model
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"🤖 Used {model} for {tweet_type or 'default'}")
                return content
            else:
                return self._fallback_response(prompt, tweet_type)
                
        except Exception as e:
            return self._fallback_response(prompt, tweet_type)
    
    def _fallback_response(self, prompt, tweet_type=None):
        """Fallback when Groq is not available"""
        if "Convert the following topic into" in prompt:
            # Extract topic
            if "Topic: " in prompt:
                topic_start = prompt.find("Topic: ") + 7
                topic_end = prompt.find("\nTweet:")
                if topic_end == -1:
                    topic_end = len(prompt)
                topic = prompt[topic_start:topic_end].strip()
            else:
                topic = "general topic"
            
            # Type-specific mock tweets
            tweets_by_type = {
                "funny": {
                    "cats": [
                        "My cat thinks I'm his personal can opener. The audacity of this furry little dictator. #CatLife #PetProblems",
                        "Cat's daily schedule: 16 hours sleeping, 4 hours judging my life choices, 4 hours demanding food. #CatLogic #Pets"
                    ],
                    "dogs": [
                        "My dog's superpower is making me feel guilty for leaving the house. Those puppy eyes should be illegal. #DogLife #GuiltTrips",
                        "Dog's philosophy: If you can't eat it, play with it, or sit on it, pee on it. #DogLogic #PetHumor"
                    ],
                    "default": [
                        f"Trying to make a funny tweet about {topic}. This is my attempt at humor. #{topic.replace(' ', '')}Humor",
                        f"Here's a witty observation about {topic}. It's supposed to be funny. #{topic.replace(' ', '')}Jokes"
                    ]
                },
                "sad": {
                    "loss": [
                        "Sometimes the hardest goodbyes are the ones we never saw coming. Missing you more today than yesterday. #Grief #Loss",
                        "The silence where your laughter used to be is the loudest sound in my world. #MissingYou #Heartache"
                    ],
                    "default": [
                        f"Feeling the weight of {topic} today. Some days are heavier than others. #Emotional #Reflection",
                        f"Thinking about {topic} and how it changed everything. #Sad #Memories"
                    ]
                },
                "cheerful": {
                    "morning": [
                        "Good morning! Today is a new opportunity to spread kindness and joy. Let's make it amazing! #Positive #GoodVibes",
                        "Rise and shine! Your smile can light up someone's world today. Go be awesome! #Motivation #Cheerful"
                    ],
                    "default": [
                        f"Feeling grateful for {topic} today! Small blessings make the biggest impact. #Gratitude #Positive",
                        f"{topic} reminds me that there's so much good in the world. Choose joy today! #Optimism #Happy"
                    ]
                },
                "informative": {
                    "technology": [
                        "Did you know? The first computer bug was an actual moth stuck in a Harvard Mark II computer in 1947. #TechFacts #History",
                        "AI processes data 1000x faster than humans, but still can't appreciate a good cat video. #AI #Technology"
                    ],
                    "default": [
                        f"Learning about {topic} today! Knowledge is power and sharing it makes us all stronger. #Education #Facts",
                        f"Interesting fact about {topic}: it's more complex than most people realize. #LearnSomething #Informative"
                    ]
                }
            }
            
            # Get tweets for the tweet type
            type_tweets = tweets_by_type.get(tweet_type, tweets_by_type["funny"])
            topic_tweets = type_tweets.get(topic.lower(), type_tweets["default"])
            return random.choice(topic_tweets)
        
        elif "Evaluate the following tweet" in prompt:
            # Strict fallback scoring - harder to get high scores
            score = round(random.uniform(3.0, 8.5), 1)  # Lower max score for strictness, 1 decimal place
            return json.dumps({
                "score": score,
                "is_funny": score >= 8.0,  # Higher threshold for strictness
                "reasoning": "Strict evaluation: requires exceptional quality to pass"
            })
        
        elif "Based on the evaluation reasoning provided" in prompt:
            feedbacks = [
                "Try adding more specific details and clever wordplay",
                "Consider using a more relatable scenario or surprising twist",
                "Add better hashtags and make it more concise",
                "Focus on being more original and less predictable"
            ]
            return random.choice(feedbacks)
        
        return "Fallback response"

class GroqLangGraphSystem:
    def __init__(self, humor_threshold=8.0, max_iterations=5):
        """Initialize LangGraph system with state management"""
        self.humor_threshold = humor_threshold
        self.max_iterations = max_iterations
        self.llm = GroqLLM()
        self.graph = self._create_workflow()
    
    def _create_workflow(self):
        """Create the LangGraph workflow with conditional routing based on tweet type"""
        
        # Create the workflow graph
        workflow = StateGraph(JokeState)
        
        # Add specialized nodes for each tweet type
        workflow.add_node("route_by_type", self._route_by_type_node)
        workflow.add_node("generate_funny", self._generate_funny_node)
        workflow.add_node("generate_sad", self._generate_sad_node)
        workflow.add_node("generate_cheerful", self._generate_cheerful_node)
        workflow.add_node("generate_informative", self._generate_informative_node)
        
        # Add specialized evaluation nodes
        workflow.add_node("evaluate_funny", self._evaluate_funny_node)
        workflow.add_node("evaluate_sad", self._evaluate_sad_node)
        workflow.add_node("evaluate_cheerful", self._evaluate_cheerful_node)
        workflow.add_node("evaluate_informative", self._evaluate_informative_node)
        
        # Add common nodes
        workflow.add_node("get_feedback", self._get_feedback_node)
        workflow.add_node("check_limits", self._check_limits_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Set entry point
        workflow.set_entry_point("route_by_type")
        
        # Add conditional routing from type router
        workflow.add_conditional_edges(
            "route_by_type",
            self._route_to_generator,
            {
                "funny": "generate_funny",
                "sad": "generate_sad", 
                "cheerful": "generate_cheerful",
                "informative": "generate_informative"
            }
        )
        
        # Add conditional routing from generators to evaluators
        workflow.add_conditional_edges(
            "generate_funny",
            lambda state: "evaluate_funny"
        )
        workflow.add_conditional_edges(
            "generate_sad", 
            lambda state: "evaluate_sad"
        )
        workflow.add_conditional_edges(
            "generate_cheerful",
            lambda state: "evaluate_cheerful"
        )
        workflow.add_conditional_edges(
            "generate_informative",
            lambda state: "evaluate_informative"
        )
        
        # Add edges from evaluators to check limits
        workflow.add_edge("evaluate_funny", "check_limits")
        workflow.add_edge("evaluate_sad", "check_limits")
        workflow.add_edge("evaluate_cheerful", "check_limits")
        workflow.add_edge("evaluate_informative", "check_limits")
        
        # Add common workflow edges
        workflow.add_edge("get_feedback", "route_by_type")  # Loop back to type routing
        workflow.add_edge("finalize", END)
        
        # Add conditional edges for retry logic
        workflow.add_conditional_edges(
            "check_limits",
            self._should_continue_or_end,
            {
                "continue": "get_feedback",
                "end": "finalize"
            }
        )
        
        return workflow.compile()
    
    def _route_by_type_node(self, state: JokeState) -> JokeState:
        """Routing node - just passes through state"""
        return state
    
    def _route_to_generator(self, state: JokeState) -> str:
        """Route to appropriate generator based on tweet type"""
        return state.get("tweet_type", "funny")
    
    def _generate_funny_node(self, state: JokeState) -> JokeState:
        """Generate funny tweet using 70B model"""
        return self._generate_tweet_by_type(state, "funny")
    
    def _generate_sad_node(self, state: JokeState) -> JokeState:
        """Generate sad tweet using Mixtral model"""
        return self._generate_tweet_by_type(state, "sad")
    
    def _generate_cheerful_node(self, state: JokeState) -> JokeState:
        """Generate cheerful tweet using 8B model"""
        return self._generate_tweet_by_type(state, "cheerful")
    
    def _generate_informative_node(self, state: JokeState) -> JokeState:
        """Generate informative tweet using 8B model"""
        return self._generate_tweet_by_type(state, "informative")
    
    def _generate_tweet_by_type(self, state: JokeState, tweet_type: str) -> JokeState:
        """Generate tweet for specific type using optimal model"""
        try:
            topic = state["topic"]
            
            # Define type-specific prompts
            type_configs = {
                "funny": {
                    "description": "a funny, engaging tweet that is humorous and clever",
                    "tone": "witty, humorous, clever",
                    "goal": "make people laugh and share"
                },
                "sad": {
                    "description": "a sad, emotional tweet that is touching and heartfelt",
                    "tone": "emotional, touching, sincere",
                    "goal": "evoke empathy and emotional connection"
                },
                "cheerful": {
                    "description": "a cheerful, uplifting tweet that is positive and inspiring",
                    "tone": "positive, uplifting, optimistic",
                    "goal": "brighten someone's day and spread positivity"
                },
                "informative": {
                    "description": "an informative, educational tweet that is factual and useful",
                    "tone": "informative, factual, educational",
                    "goal": "share knowledge and provide valuable information"
                }
            }
            
            config = type_configs.get(tweet_type, type_configs["funny"])
            
            prompt = f"""You are a creative social media expert. 
            Convert the following topic into {config['description']} that is:
            - Maximum 200 words (strict limit)
            - Under 280 characters
            - {config['tone']} in tone
            - Relatable and shareable
            - Uses appropriate hashtags
            - Goal: {config['goal']}
            
            Topic: {topic}
            Tweet Type: {tweet_type}
            
            Tweet:"""
            
            # Use the optimal model for this tweet type
            tweet = self.llm.invoke(prompt, tweet_type)
            tweet = tweet.strip().strip('"\'')
            
            # Clean up the response
            if "Tweet:" in tweet:
                tweet = tweet.split("Tweet:")[-1].strip()
            
            # Validate word count
            word_count = len(tweet.split())
            if word_count > 200:
                words = tweet.split()[:200]
                tweet = ' '.join(words)
                print(f"⚠️  Tweet truncated to 200 words (was {word_count})")
            
            return {
                "current_tweet": tweet,
                "error": ""
            }
            
        except Exception as e:
            return {
                "current_tweet": "",
                "error": str(e)
            }
    
    def _evaluate_funny_node(self, state: JokeState) -> JokeState:
        """Evaluate funny tweet using comedy critic"""
        return self._evaluate_tweet_by_type(state, "funny")
    
    def _evaluate_sad_node(self, state: JokeState) -> JokeState:
        """Evaluate sad tweet using emotional expert"""
        return self._evaluate_tweet_by_type(state, "sad")
    
    def _evaluate_cheerful_node(self, state: JokeState) -> JokeState:
        """Evaluate cheerful tweet using positive psychology expert"""
        return self._evaluate_tweet_by_type(state, "cheerful")
    
    def _evaluate_informative_node(self, state: JokeState) -> JokeState:
        """Evaluate informative tweet using educational expert"""
        return self._evaluate_tweet_by_type(state, "informative")
    
    def _evaluate_tweet_by_type(self, state: JokeState, tweet_type: str) -> JokeState:
        """Evaluate tweet for specific type using optimal model"""
        try:
            tweet = state["current_tweet"]
            
            if not tweet or "error" in tweet.lower():
                return {
                    "current_score": 0.0,
                    "is_funny": False,
                    "feedback": "No valid tweet to evaluate"
                }
            
            # Define type-specific evaluation criteria
            evaluation_criteria = {
                "funny": {
                    "title": "comedy critic",
                    "criteria": {
                        "1-3": "Not funny at all, boring, predictable",
                        "4-6": "Mildly amusing but lacks originality",
                        "7-8": "Good humor with some cleverness",
                        "9-10": "Exceptional, original, very funny, share-worthy"
                    }
                },
                "sad": {
                    "title": "emotional content expert",
                    "criteria": {
                        "1-3": "Not emotional at all, flat, unengaging",
                        "4-6": "Slightly emotional but lacks depth",
                        "7-8": "Good emotional impact, touching",
                        "9-10": "Exceptionally moving, deeply touching, powerful"
                    }
                },
                "cheerful": {
                    "title": "positive psychology expert",
                    "criteria": {
                        "1-3": "Not cheerful, negative or boring",
                        "4-6": "Mildly positive but lacks inspiration",
                        "7-8": "Good uplifting content, positive",
                        "9-10": "Exceptionally inspiring, genuinely uplifting"
                    }
                },
                "informative": {
                    "title": "educational content expert",
                    "criteria": {
                        "1-3": "Not informative, inaccurate, confusing",
                        "4-6": "Somewhat informative but lacks depth",
                        "7-8": "Good information, educational, clear",
                        "9-10": "Exceptionally valuable, highly educational, insightful"
                    }
                }
            }
            
            criteria_config = evaluation_criteria.get(tweet_type, evaluation_criteria["funny"])
            
            eval_prompt = f"""You are a very strict expert {criteria_config['title']} with extremely high standards. 
            Evaluate this {tweet_type} tweet for quality on a scale of 1-10. Be very critical!
            
            Scoring criteria (be strict):
            - 1-3: {criteria_config['criteria']['1-3']}
            - 4-6: {criteria_config['criteria']['4-6']}
            - 7-8: {criteria_config['criteria']['7-8']}
            - 9-10: {criteria_config['criteria']['9-10']}
            
            Additional requirements (must meet all):
            - Maximum 200 words (strictly enforced)
            - Under 280 characters
            - Appropriate hashtags
            - Matches {tweet_type} tone and goal
            
            Tweet: {tweet}
            Tweet Type: {tweet_type}
            Word count: {len(tweet.split())}
            Character count: {len(tweet)}
            
            Respond with JSON format:
            {{
                "score": <number from 1-10 to 1 decimal place>,
                "is_funny": <boolean>,
                "reasoning": "<detailed explanation including word/character count check>"
            }}"""
            
            # Use the optimal model for this evaluation type
            evaluation = self.llm.invoke(eval_prompt, tweet_type)
            
            try:
                eval_data = json.loads(evaluation)
                score = eval_data.get("score", 0)
                is_funny = eval_data.get("is_funny", False)
                reasoning = eval_data.get("reasoning", "No reasoning")
                
                # Format score to 1 decimal place
                score = round(float(score), 1)
                
            except:
                score = round(random.uniform(4.0, 9.0), 1)
                is_funny = score >= state["humor_threshold"]
                reasoning = "Evaluation parsing failed"
            
            # Create iteration history entry
            iteration_entry = {
                "iteration": state["iteration"] + 1,
                "tweet": tweet,
                "score": float(score),
                "is_funny": bool(is_funny),
                "reasoning": reasoning
            }
            
            return {
                "current_score": float(score),
                "is_funny": bool(is_funny),
                "feedback": reasoning,
                "iteration_history": [iteration_entry]
            }
            
        except Exception as e:
            return {
                "current_score": 0.0,
                "is_funny": False,
                "feedback": f"Evaluation failed: {str(e)}"
            }
    
    def _evaluate_tweet_node(self, state: JokeState) -> JokeState:
        """Node for evaluating tweet humor - uses state reducers"""
        try:
            tweet = state["current_tweet"]
            
            if not tweet or "error" in tweet.lower():
                return {
                    "current_score": 0.0,
                    "is_funny": False,
                    "feedback": "No valid tweet to evaluate"
                }
            
            # Define type-specific evaluation criteria
            evaluation_criteria = {
                "funny": {
                    "title": "comedy critic",
                    "criteria": {
                        "1-3": "Not funny at all, boring, predictable",
                        "4-6": "Mildly amusing but lacks originality",
                        "7-8": "Good humor with some cleverness",
                        "9-10": "Exceptional, original, very funny, share-worthy"
                    }
                },
                "sad": {
                    "title": "emotional content expert",
                    "criteria": {
                        "1-3": "Not emotional at all, flat, unengaging",
                        "4-6": "Slightly emotional but lacks depth",
                        "7-8": "Good emotional impact, touching",
                        "9-10": "Exceptionally moving, deeply touching, powerful"
                    }
                },
                "cheerful": {
                    "title": "positive psychology expert",
                    "criteria": {
                        "1-3": "Not cheerful, negative or boring",
                        "4-6": "Mildly positive but lacks inspiration",
                        "7-8": "Good uplifting content, positive",
                        "9-10": "Exceptionally inspiring, genuinely uplifting"
                    }
                },
                "informative": {
                    "title": "educational content expert",
                    "criteria": {
                        "1-3": "Not informative, inaccurate, confusing",
                        "4-6": "Somewhat informative but lacks depth",
                        "7-8": "Good information, educational, clear",
                        "9-10": "Exceptionally valuable, highly educational, insightful"
                    }
                }
            }
            
            criteria_config = evaluation_criteria.get(tweet_type, evaluation_criteria["funny"])
            
            eval_prompt = f"""You are a very strict expert {criteria_config['title']} with extremely high standards. 
            Evaluate this {tweet_type} tweet for quality on a scale of 1-10. Be very critical!
            
            Scoring criteria (be strict):
            - 1-3: {criteria_config['criteria']['1-3']}
            - 4-6: {criteria_config['criteria']['4-6']}
            - 7-8: {criteria_config['criteria']['7-8']}
            - 9-10: {criteria_config['criteria']['9-10']}
            
            Additional requirements (must meet all):
            - Maximum 200 words (strictly enforced)
            - Under 280 characters
            - Appropriate hashtags
            - Matches {tweet_type} tone and goal
            
            Tweet: {tweet}
            Tweet Type: {tweet_type}
            Word count: {len(tweet.split())}
            Character count: {len(tweet)}
            
            Respond with JSON format:
            {{
                "score": <number from 1-10 to 1 decimal place>,
                "is_funny": <boolean>,
                "reasoning": "<detailed explanation including word/character count check>"
            }}"""
            
            evaluation = self.llm.invoke(eval_prompt)
            
            try:
                eval_data = json.loads(evaluation)
                score = eval_data.get("score", 0)
                is_funny = eval_data.get("is_funny", False)
                reasoning = eval_data.get("reasoning", "No reasoning")
                
                # Format score to 1 decimal place
                score = round(float(score), 1)
                
            except:
                score = round(random.uniform(4.0, 9.0), 1)
                is_funny = score >= state["humor_threshold"]
                reasoning = "Evaluation parsing failed"
            
            # Create iteration history entry
            iteration_entry = {
                "iteration": state["iteration"] + 1,
                "tweet": tweet,
                "score": float(score),
                "is_funny": bool(is_funny),
                "reasoning": reasoning
            }
            
            # Return updated state with reducers
            return {
                "current_score": float(score),
                "is_funny": bool(is_funny),
                "feedback": reasoning,
                "iteration_history": [iteration_entry]  # This uses the reducer!
            }
            
        except Exception as e:
            return {
                "current_score": 0.0,
                "is_funny": False,
                "feedback": f"Evaluation failed: {str(e)}"
            }
    
    def _get_feedback_node(self, state: JokeState) -> JokeState:
        """Node for getting improvement feedback - uses state reducers"""
        try:
            tweet = state["current_tweet"]
            reasoning = state["feedback"]
            
            prompt = f"""Based on the evaluation reasoning provided, suggest specific improvements 
            to make this tweet funnier and more engaging.
            
            Original Tweet: {tweet}
            Evaluation Reasoning: {reasoning}
            
            Provide specific, actionable suggestions for improvement:"""
            
            feedback = self.llm.invoke(prompt)
            feedback = feedback.strip()
            
            return {
                "feedback": feedback
            }
            
        except Exception as e:
            return {
                "feedback": f"Feedback generation failed: {str(e)}"
            }
    
    def _check_limits_node(self, state: JokeState) -> JokeState:
        """Node for checking iteration limits - uses state reducers"""
        # Increment iteration count using reducer
        return {
            "iteration": state["iteration"] + 1
        }
    
    def _finalize_node(self, state: JokeState) -> JokeState:
        """Node for finalizing the result - uses state reducers"""
        if state["is_funny"]:
            return {
                "final_tweet": state["current_tweet"],
                "final_score": state["current_score"],
                "success": True
            }
        else:
            # Find best attempt from history
            if state["iteration_history"]:
                best_attempt = max(state["iteration_history"], key=lambda x: x["score"])
                return {
                    "final_tweet": best_attempt["tweet"],
                    "final_score": best_attempt["score"],
                    "success": False
                }
            else:
                return {
                    "final_tweet": state["current_tweet"],
                    "final_score": state["current_score"],
                    "success": False
                }
    
    def _should_continue_or_end(self, state: JokeState) -> str:
        """Conditional routing function"""
        if state["is_funny"]:
            return "end"
        elif state["iteration"] >= state["max_iterations"]:
            return "end"
        else:
            return "continue"
    
    def generate_tweet(self, topic: str, tweet_type: str = "funny") -> Dict:
        """
        Generate a tweet using proper LangGraph workflow with state reducers
        
        Args:
            topic: The topic to create a tweet about
            tweet_type: Type of tweet (funny, sad, cheerful, informative)
            
        Returns:
            Dictionary with result and process details
        """
        print(f"🤖 Using LangGraph with State Reducers for: '{topic}'")
        print(f"📊 Target humor score: {self.humor_threshold}/10")
        print(f"🔄 Max iterations: {self.max_iterations}")
        print(f"🔧 Default Model: {self.llm.default_model}")
        print("-" * 60)
        
        # Initialize state
        initial_state = {
            "topic": topic,
            "tweet_type": tweet_type,
            "current_tweet": "",
            "current_score": 0.0,
            "is_funny": False,
            "iteration": 0,
            "max_iterations": self.max_iterations,
            "humor_threshold": self.humor_threshold,
            "iteration_history": [],  # This will use the reducer!
            "feedback": "",
            "final_tweet": "",
            "final_score": 0.0,
            "success": False,
            "error": ""
        }
        
        try:
            # Run the workflow
            result = self.graph.invoke(initial_state)
            
            # Determine what type of LLM was actually used
            llm_type = "Groq" if self.llm.available else "Fallback"
            
            if result["success"]:
                print("\n🎉 SUCCESS! Found a funny tweet!")
            else:
                print(f"\n⚠️  Max iterations reached. Best score: {result['final_score']}/10")
            
            return {
                "success": result["success"],
                "tweet": result["final_tweet"],
                "score": result["final_score"],
                "iterations": result["iteration"],
                "iteration_history": result["iteration_history"],
                "workflow_type": f"LangGraph with Reducers ({llm_type})"
            }
            
        except Exception as e:
            return {
                "success": False,
                "tweet": "",
                "score": 0.0,
                "iterations": self.max_iterations,
                "error": str(e),
                "workflow_type": "LangGraph with Reducers (Error)"
            }

def main():
    """Test the LangGraph system with state reducers"""
    
    print("🤖 LangGraph Tweet Generator with State Reducers")
    print("=" * 60)
    
    # Get user input
    topic = input("Enter a topic: ").strip()
    
    if not topic:
        print("❌ Please enter a topic!")
        return
    
    # Get tweet type
    print("\nTweet Types:")
    print("1. funny - Humorous and clever")
    print("2. sad - Emotional and touching")
    print("3. cheerful - Positive and uplifting")
    print("4. informative - Educational and factual")
    
    type_map = {"1": "funny", "2": "sad", "3": "cheerful", "4": "informative"}
    
    while True:
        type_choice = input("\nSelect tweet type (1-4): ").strip()
        if type_choice in type_map:
            tweet_type = type_map[type_choice]
            break
        else:
            print("❌ Please enter 1, 2, 3, or 4")
    
    print(f"\n🚀 Generating {tweet_type} tweet about: '{topic}'")
    print("Processing...")
    
    # Generate tweet
    system = GroqLangGraphSystem(humor_threshold=8.0, max_iterations=5)
    result = system.generate_tweet(topic, tweet_type)
    
    # Output the funny tweet
    print("\n" + "=" * 60)
    print("🎉 YOUR FUNNY TWEET:")
    print("=" * 60)
    
    if result['tweet']:
        print(f"📢 {result['tweet']}")
        print(f"\n📊 Humor Score: {result['score']}/10")
        print(f"🔄 Attempts: {result['iterations']}")
        print(f"✅ Success: {'Yes' if result['success'] else 'No'}")
        print(f"🔧 System: {result['workflow_type']}")
        
        # Show iteration history
        if result.get('iteration_history'):
            print(f"\n📋 Iteration History:")
            for i, iteration in enumerate(result['iteration_history'], 1):
                status = "✅" if iteration['is_funny'] else "🔄"
                print(f"  {i}. Score: {iteration['score']}/10 {status}")
                print(f"     Tweet: {iteration['tweet']}")
                print(f"     Reasoning: {iteration['reasoning']}")
    else:
        print("❌ Could not generate a funny tweet")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
