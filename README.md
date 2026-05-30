# Multi-Model LangGraph Tweet Generator

A sophisticated system that generates tweets of different types (funny, sad, cheerful, informative) using optimal Groq models and LangGraph's powerful workflow orchestration with conditional routing.

## Features

- **Multi-Model Architecture**: Different Groq models optimized for each tweet type
- **4 Tweet Types**: Funny, Sad, Cheerful, and Informative content generation
- **Conditional Routing**: Smart workflow routing based on user selection
- **Type-Specific Evaluation**: Specialized critics for each tweet type
- **LangGraph Workflow**: True iterative support with state reducers
- **Smart Retry Logic**: Automatically retries until quality threshold is met
- **State Management**: Automatic tracking of iterations, scores, and feedback
- **Web Interface**: Beautiful frontend with type selection and history viewer
- **Fallback System**: Works even without API using enhanced mock responses
- **Configurable Thresholds**: Adjustable quality thresholds (8.0) and retry limits (5)

## System Architecture

```
USER INPUT → Flask API → LangGraph → Type Router → [Conditional Routing]
                                                    ↓
┌─────────────────────────────────────────┐
│           SELECT TWEET TYPE              │
│                                         │
│  😄 Funny   → Funny Generator (70B)     │
│  😢 Sad     → Sad Generator (Mixtral)   │
│  😊 Cheerful→ Cheerful Generator (8B)    │
│  📚 Info    → Info Generator (8B)       │
└─────────────────────────────────────────┘
                                                    ↓
                                            EVALUATE SCORE
                                                    ↓
                                          SCORE ≥ 8.0?
                                                    ↓
┌─────────────────┐    ┌─────────────────┐
│  YES → FINALIZE │    │  NO → FEEDBACK  │
│  RETURN RESULT  │    │  LOOP BACK      │
└─────────────────┘    └─────────────────┘
```

## Installation

1. Clone or download the files to your project directory
2. Install required packages:
```bash
pip install requests python-dotenv langgraph flask matplotlib
```

3. Set up your environment variables:
```bash
# Create .env file
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Web Interface (Recommended)

```bash
python app.py
```

Visit `http://localhost:5000` to use the beautiful web interface with:
- Tweet type selection (funny, sad, cheerful, informative)
- Real-time generation and evaluation
- State history viewer
- Score visualization

### Command Line Usage

```bash
python groq_langgraph_system.py
```

Then enter a topic and select tweet type when prompted.

### Python API Usage

```python
from groq_langgraph_system import GroqLangGraphSystem

# Initialize the system
system = GroqLangGraphSystem(
    humor_threshold=8.0,      # Quality threshold (default)
    max_iterations=5          # Maximum retry attempts (default)
)

# Generate different tweet types
result = system.generate_tweet("cats", "funny")
result = system.generate_tweet("loss", "sad")
result = system.generate_tweet("morning", "cheerful")
result = system.generate_tweet("technology", "informative")

print(f"Tweet: {result['tweet']}")
print(f"Score: {result['score']}/10")
print(f"Success: {result['success']}")
print(f"Iterations: {result['iterations']}")
```

## API Setup

### Getting Groq API Key (Free)

1. Go to: https://console.groq.com/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

### Available Free Models

- `llama-3.1-70b-instant` (used for funny tweets - maximum creativity)
- `mixtral-8x7b-32768` (used for sad tweets - emotional depth)
- `llama-3.1-8b-instant` (used for cheerful/informative - fast & efficient)

## Multi-Model Strategy

| Tweet Type | Generator Model | Evaluator | Purpose |
|------------|-----------------|-----------|---------|
| 😄 Funny | Llama-3.1-70B | Comedy Critic | Maximum creativity |
| 😢 Sad | Mixtral-8x7B | Emotional Expert | Emotional depth |
| 😊 Cheerful | Llama-3.1-8B | Psychology Expert | Fast & positive |
| 📚 Informative | Llama-3.1-8B | Education Expert | Factual accuracy |

## How It Works

1. **Input**: User provides topic and selects tweet type
2. **Route**: LangGraph routes to optimal generator based on type
3. **Generate**: Specialized model creates type-appropriate tweet
4. **Evaluate**: Type-specific expert scores quality (1-10)
5. **Check**: Is score ≥ 8.0?
   - **YES**: Success! Return best tweet
   - **NO**: Get feedback and retry (max 5 attempts)
6. **Output**: Best tweet + score + complete iteration history

## Example Output

### Web Interface
```
🎭 LangGraph Tweet Generator
==================================================
Topic: cats
Tweet Type: 😄 Funny

🤖 Used llama-3.1-70b-instant for funny
📝 Generated: "My cat thinks it's in charge, my wallet thinks it's empty..."
🎭 Score: 8.2/10 ✅ Success!

📢 Final Tweet: "My cat thinks it's in charge, my wallet thinks it's empty, but we all know the real boss is the couch. Who else is guilty of being a slave to their feline overlord? #CatLife #FelineOverlords"

📊 Quality Score: 8.2/10
🔄 Attempts: 1
✅ Success: Yes
🔧 Workflow: LangGraph with Reducers (Groq)
```

### Command Line
```
🤖 LangGraph Tweet Generator with State Reducers
==================================================
Enter a topic: dogs

Tweet Types:
1. funny - Humorous and clever
2. sad - Emotional and touching  
3. cheerful - Positive and uplifting
4. informative - Educational and factual

Select tweet type (1-4): 2

🚀 Generating sad tweet about: 'dogs'
🤖 Used mixtral-8x7b-32768 for sad
📝 Generated: "Sometimes the hardest goodbyes are the ones we never saw coming..."
🎭 Score: 8.7/10 ✅ Success!

📢 Final Tweet: "Sometimes the hardest goodbyes are the ones we never saw coming. Missing you more today than yesterday. #Grief #Loss #MissingYou"

📊 Quality Score: 8.7/10
🔄 Attempts: 2
✅ Success: Yes
🔧 Workflow: LangGraph with Reducers (Groq)
```

## Configuration Options

- `humor_threshold`: Quality threshold (default: 8.0)
- `max_iterations`: Maximum retry attempts (default: 5)
- `tweet_types`: Available types (funny, sad, cheerful, informative)
- `word_limit`: Maximum words per tweet (default: 200)
- `score_precision`: Decimal places for scores (1 decimal)

## File Structure

```
├── groq_langgraph_system.py    # Main multi-model system
├── app.py                      # Flask web application
├── templates/
│   └── index.html             # Web frontend
├── test_system.py             # Testing script
├── clean_architecture.md      # Clean architecture diagram
├── .env                       # API keys
├── .env.example               # Environment template
└── README.md                  # This file
```

## Why Multi-Model LangGraph?

This system combines the power of multiple Groq models with LangGraph's advanced workflow orchestration:

### **Multi-Model Benefits**
- **Optimal Model Selection**: Right model for right task (70B for creativity, 8B for efficiency)
- **Type Specialization**: Different models excel at different content types
- **Performance Optimization**: Faster processing for simple tasks, more power for complex ones

### **LangGraph Advantages**
- **True Iterative Support**: Built specifically for workflows with loops and retries
- **Conditional Routing**: Smart decision-making based on evaluation results
- **State Management**: Automatic tracking of iterations, scores, and feedback with reducers
- **Workflow Visualization**: Clear architecture and debugging capabilities

### **Combined Power**
- **Smart Routing**: Automatic workflow selection based on user needs
- **Quality Control**: Type-specific evaluators ensure high standards
- **Scalable Architecture**: Easy to add new tweet types and models
- **Production Ready**: Robust error handling and fallback systems

## Troubleshooting

### API Issues
- **No API key**: System will fall back to mock responses
- **API errors**: Automatic fallback to enhanced responses
- **Rate limits**: Built-in retry logic with exponential backoff

### Common Issues
- **Module not found**: Run `pip install requests python-dotenv langgraph`
- **API key not working**: Check key format and network connection
- **Low humor scores**: Try different topics or adjust threshold

## Contributing

This project uses:
- **Groq**: Free LLM API with Llama models
- **LangGraph**: Workflow orchestration framework
- **Python**: Simple, clean implementation

## License

Free to use with Groq's free tier API.
