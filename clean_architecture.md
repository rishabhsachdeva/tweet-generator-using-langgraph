# 🎯 Clean Architecture Diagram

## 📋 Simple Flow Diagram

```
USER INPUT
    │
    ▼
┌─────────────┐
│ Flask API   │
└─────────────┘
    │
    ▼
┌─────────────┐
│ LangGraph   │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Type Router │
└─────────────┘
    │
    ▼
┌─────────────────────────────────┐
│     SELECT TWEET TYPE          │
├─────────────────────────────────┤
│                                 │
│  😄 Funny   → Funny Generator  │
│  😢 Sad     → Sad Generator    │  
│  😊 Cheerful→ Cheerful Gen.    │
│  📚 Info    → Info Generator   │
│                                 │
└─────────────────────────────────┘
    │
    ▼
┌─────────────┐
│ GENERATE    │
│ TWEET       │
└─────────────┘
    │
    ▼
┌─────────────┐
│ EVALUATE    │
│ SCORE       │
└─────────────┘
    │
    ▼
┌─────────────────┐
│  SCORE ≥ 8.0?  │
└─────────────────┘
    │
    ├── YES ──► ┌─────────────┐
    │           │ FINALIZE    │
    │           │ RETURN      │
    │           │ RESULT      │
    │           └─────────────┘
    │                 │
    │                 ▼
    │             ┌─────────┐
    │             │  END    │
    │             └─────────┘
    │
    └── NO ──► ┌─────────────┐
                │ GET         │
                │ FEEDBACK    │
                └─────────────┘
                    │
                    ▼
                ┌─────────────┐
                │ LOOP BACK   │◄───┐
                │ TO ROUTER   │    │
                └─────────────┘    │
                    │             │
                    └─────────────┘
```

## 🔄 Complete Loop View

```
START → ROUTER → GENERATOR → EVALUATOR → CHECK SCORE
    ↑                                              │
    │                                              │
    │                                              ▼
    │                                         SCORE < 8.0?
    │                                              │
    │                                              ▼
    │                                         GET FEEDBACK
    │                                              │
    │                                              ▼
    └───────────────────────◄─────── LOOP BACK ─────┘
```

## 🤖 Model Assignment

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Funny     │    │     Sad     │    │  Cheerful   │
│ Generator   │    │ Generator   │    │ Generator   │
│             │    │             │    │             │
│ Llama-3.1-70B│    │Mixtral-8x7B │    │Llama-3.1-8B │
│             │    │             │    │             │
│ Max Creative│    │Emotional    │    │Fast Positive│
└─────────────┘    └─────────────┘    └─────────────┘

┌─────────────┐
│ Informative  │
│ Generator   │
│             │
│Llama-3.1-8B │
│             │
│Factual      │
└─────────────┘
```

## 📊 Evaluation Specialists

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Comedy      │    │ Emotional   │    │ Positive    │
│ Critic      │    │ Expert      │    │ Psychology  │
│             │    │             │    │             │
│ Humor Score │    │ Empathy     │    │ Uplift      │
│ 1-10        │    │ Score 1-10  │    │ Score 1-10  │
└─────────────┘    └─────────────┘    └─────────────┘

┌─────────────┐
│ Education   │
│ Expert      │
│             │
│ Facts       │
│ Score 1-10  │
└─────────────┘
```

## 🎯 Key Components

### **1. User Interface**
- Web frontend with type selection
- Input forms and result display
- History viewer

### **2. Flask Backend**
- REST API endpoints
- Request validation
- Error handling

### **3. LangGraph System**
- Workflow orchestration
- State management with reducers
- Conditional routing

### **4. Type Router**
- Routes to appropriate generator
- Based on user selection
- 4 parallel paths available

### **5. Generators**
- Type-specific content creation
- Optimal model selection
- Word count enforcement (≤200)

### **6. Evaluators**
- Type-specific quality assessment
- Strict scoring (≥8.0 to pass)
- Detailed reasoning

### **7. Decision Logic**
- Score checking
- Retry control (max 5 attempts)
- Success/failure determination

### **8. Feedback Loop**
- Improvement suggestions
- Loop back to router
- History accumulation

## 🔧 How It Works - Step by Step

```
1. User picks type (funny/sad/cheerful/informative)
2. LangGraph routes to correct generator
3. Optimal model creates tweet
4. Specialist evaluator scores it
5. If score ≥ 8.0 → SUCCESS! Return result
6. If score < 8.0 → Get feedback and retry
7. Loop back to step 2 (max 5 times)
8. Return best result achieved
```

## 📈 State Flow

```
Initial State:
├── topic: "cats"
├── tweet_type: "funny"
├── iteration: 0
└── history: []

After Each Loop:
├── current_tweet: "Generated tweet..."
├── current_score: 7.5
├── iteration: 1
└── history: [{tweet, score, reasoning}]

Final State:
├── final_tweet: "Best tweet..."
├── final_score: 8.2
├── success: true
└── history: [all attempts]
```

## 🎮 Benefits

✅ **Clear flow** - Easy to follow the process  
✅ **Visible loops** - Retry logic is obvious  
✅ **Type specialization** - Right model for right task  
✅ **Quality control** - Strict evaluation standards  
✅ **State tracking** - Complete history preserved  
✅ **Fallback safety** - Graceful error handling  

---

**Simple, clean, and easy to understand!** 🚀
