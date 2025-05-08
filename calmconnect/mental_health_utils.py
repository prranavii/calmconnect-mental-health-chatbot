import random

# Mental Health Resources
CRISIS_RESOURCES = {
    "National Suicide Prevention Lifeline": "1-800-273-8255",
    "Crisis Text Line": "Text HOME to 741741",
    "SAMHSA's National Helpline": "1-800-662-4357",
    "National Alliance on Mental Illness": "1-800-950-6264",
    "Emergency": "911"
}

COPING_STRATEGIES = {
    "anxiety": [
        "Try the 4-7-8 breathing technique",
        "Ground yourself using the 5-4-3-2-1 method",
        "Progressive muscle relaxation",
        "Take a short walk if possible",
        "Write down your worries"
    ],
    "depression": [
        "Set a small, achievable goal for today",
        "Try to get some sunlight",
        "Reach out to one person",
        "Do one act of self-care",
        "Write down three things you're grateful for"
    ],
    "stress": [
        "Take a 5-minute meditation break",
        "Listen to calming music",
        "Try some gentle stretching",
        "Write in your journal",
        "Take a break from screens"
    ]
}

MOOD_BOOSTERS = [
    "You're stronger than you know",
    "Take it one moment at a time",
    "Your feelings are valid",
    "You don't have to face this alone",
    "Small steps lead to big changes"
]

DAILY_AFFIRMATIONS = [
    "I am worthy of love and respect",
    "I choose to be confident and self-assured",
    "I am in charge of my own happiness",
    "I am becoming stronger every day",
    "I deserve peace and happiness",
    "I am capable of handling challenges",
    "My potential is limitless",
    "I choose to be positive today",
    "I trust in my journey",
    "I am enough just as I am"
]

MINDFULNESS_EXERCISES = [
    {
        "name": "Body Scan",
        "duration": "5 minutes",
        "instructions": "Start from your toes and slowly move your attention up through your body, noticing any sensations without judgment."
    },
    {
        "name": "Mindful Breathing",
        "duration": "3 minutes",
        "instructions": "Focus on your breath. Notice the sensation of air moving in and out of your body."
    },
    {
        "name": "5-4-3-2-1 Grounding",
        "duration": "2 minutes",
        "instructions": "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
    }
]

def get_random_affirmation():
    return random.choice(DAILY_AFFIRMATIONS)

def get_coping_strategies(mood):
    return COPING_STRATEGIES.get(mood.lower(), COPING_STRATEGIES['stress'])

def get_random_mood_booster():
    return random.choice(MOOD_BOOSTERS)

def get_mindfulness_exercise():
    return random.choice(MINDFULNESS_EXERCISES)

def generate_mental_health_prompt(user_input):
    """Generate a context-aware mental health prompt based on user input"""
    base_prompt = """You are a compassionate mental health support assistant. 
    Your role is to provide empathetic, supportive responses while:
    1. Actively listening and validating feelings
    2. Offering practical coping strategies when appropriate
    3. Encouraging professional help when needed
    4. Maintaining boundaries and ethical guidelines
    5. Using a warm, understanding tone
    
    Remember to:
    - Validate emotions without judgment
    - Focus on empowerment and hope
    - Provide actionable suggestions
    - Be clear about your role as a supportive AI, not a replacement for professional help
    """
    
    return base_prompt + f"\n\nUser message: {user_input}" 