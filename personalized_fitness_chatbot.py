import nltk
from nltk.corpus import stopwords   #import stop words
import json    #json files
import re      # regular expressions
from thefuzz import fuzz     # for mispelled words

# Read Readme.md and install dependencies pip install requirements.txt

# stop words
nltk.download('stopwords', quiet=True)

# open json file
with open("workout_plans.json", "r") as f:
    workout_plans = json.load(f)
with open("diet_plans.json", "r") as f:
    diet_plans = json.load(f)
with open("responses.json", "r") as f:
    responses = json.load(f)

## Similarity threshold for fuzzy matching
SIMILARITY = 85

def process_text(text):
    #Converts text to lowercase, removes non-alpha chars, splits and removes stopwords.
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word and word not in stop_words] # to check if word is not empty
    return words

# Input functions
def get_fitness_goals():
    # Gets the user's fitness goal
    weight_loss_keywords = ["lose", "loss", "fat", "slim", "slimming", "reduce", "lean", "shed", "weightloss"]
    muscle_gain_keywords = ["muscle", "bulk", "strength", "strong", "build", "gains", "bigger", "toned", "big"]
    general_keywords = ["fit", "healthy", "tone", "active", "general", "maintain", "wellbeing", "overall"]

    while True:
        print("\n" + responses.get("ask_goal"))
        user_input = input("Tell me your goal: ")
        tokens = process_text(user_input)

        found_weight_loss = any(fuzz.ratio(token, keyword) >= SIMILARITY
                                for token in tokens for keyword in weight_loss_keywords)
        found_muscle_gain = any(fuzz.ratio(token, keyword) >= SIMILARITY
                                for token in tokens for keyword in muscle_gain_keywords)
        found_general = any(fuzz.ratio(token, keyword) >= SIMILARITY
                            for token in tokens for keyword in general_keywords)
        print()

        if found_weight_loss and found_muscle_gain:
             print("Got it! You want to lose weight & build muscle. We'll focus on building muscle while managing diet.")
        elif found_weight_loss:
            print("Okay! Your goal is weight loss. Let’s work on that!")
            return "weight loss"
        elif found_muscle_gain:
            print("Awesome! You’re looking to build muscle/strength. Let’s get those gains!")
            return "muscle gain"
        elif found_general:
             print("Great! You’re aiming for general fitness and well-being. Let’s make you feel amazing!")
             if "general fitness" in workout_plans:
                 return "general fitness"
             else:
                 return "weight loss"
        else:
            print(responses.get('error'))
            continue

def get_diet_preference():
    # Gets the user's diet preference.
    vegetarian_keywords = ["vegetarian", "veggie", "veg", "no meat", "meatless"]
    vegan_keywords = ["vegan", "plant-based", "no animal", "plants only"]
    no_pref_keywords = ["everything", "normal", "all", "any", "meat", "no restrictions", "anything", "regular", "no pref", "no preference"]

    while True:
        print("\n" + responses.get("ask_diet", "Do you have any dietary preferences? (e.g., vegetarian, vegan, no preference)"))
        user_input = input("Tell me about your diet: ")
        tokens = process_text(user_input)

        is_vegetarian = any(fuzz.ratio(token, keyword) >= SIMILARITY
                            for token in tokens for keyword in vegetarian_keywords)
        is_vegan = any(fuzz.ratio(token, keyword) >= SIMILARITY
                       for token in tokens for keyword in vegan_keywords)
        is_no_pref = any(fuzz.ratio(token, keyword) >= SIMILARITY
                         for token in tokens for keyword in no_pref_keywords)

        print()
        if is_vegan:
            print("Gotcha! You’re vegan. I’ll make sure your meals are plant-based.")
            return "vegan"
        elif is_vegetarian:
            return "vegetarian"
        elif is_no_pref and not (is_vegan or is_vegetarian):
             return "no preference"
        else:
            print(responses.get('error'))
            continue

def get_equipment():
    #Gets the user's available equipment.
    dumbbells_keywords = ["dumbbells", "weights", "free weights", "dumbell", "dbs"]
    bands_keywords = ["bands", "resistance", "resistance bands", "elastic bands"]
    gym_keywords = ["gym", "machines", "fitness center", "full equipment", "access to everything"]
    no_equipment_keywords = ["nothing", "no", "bodyweight", "home", "no equipment", "body weight", "none"]
    EQUIPMENT_SIMILARITY = 70

    while True:
        print("\n" + responses.get("ask_equipment", "What equipment do you have access to? (e.g., dumbbells, bands, gym, none)"))
        user_input = input("Tell me what equipment you have: ")
        tokens = process_text(user_input)

        has_dumbbells = any(fuzz.ratio(token, keyword) >= EQUIPMENT_SIMILARITY
                            for token in tokens for keyword in dumbbells_keywords)
        has_bands = any(fuzz.ratio(token, keyword) >= EQUIPMENT_SIMILARITY
                        for token in tokens for keyword in bands_keywords)
        has_gym = any(fuzz.ratio(token, keyword) >= EQUIPMENT_SIMILARITY
                      for token in tokens for keyword in gym_keywords)
        has_no_equipment = any(fuzz.ratio(token, keyword) >= EQUIPMENT_SIMILARITY
                               for token in tokens for keyword in no_equipment_keywords) \
                           or any(fuzz.ratio(user_input.lower(), keyword) >= 90 for keyword in ["none", "no equipment", "nothing"])

        print()
        if has_gym:
            print("Perfect! You have access to a gym, Let’s work with that.")
            return "gym workout"
        elif has_dumbbells:
            print("Cool! You’ve got dumbbells. Let’s work with that.")
            return "dumbbells"
        elif has_bands:
            print("Nice! You’ve got Resistance bands. I can create a workout with those.")
            return "resistance bands"
        elif has_no_equipment:
            print("No equipment? No problem! We can do bodyweight exercises right at home.")
            return "no equipment"
        else:
             print(responses.get('error'))
             continue

def get_motivation_reason():
    # Gets the user's motivation
    confidence_keywords = ["confidence", "confident", "self-esteem", "feel better", "look better", "appearance", "attractive"]
    energy_keywords = ["energy", "energetic", "tired", "active", "stamina", "less tired", "vitality"]
    health_keywords = ["health", "healthy", "wellbeing", "wellness", "sick", "disease", "longevity", "prevent", "doctor"]
    stress_keywords = ["stress", "anxious", "anxiety", "relief", "relax", "calm", "mental health", "clear head", "mood"]

    print("\n" + responses.get("ask_motivation", "What's your main reason for wanting to get fit? (e.g., more energy, confidence, health, stress relief)"))
    user_input = input("Tell me your reason: ")
    tokens = process_text(user_input)
    print()

    if health_keywords:
        print("That’s a great reason! Let’s focus on improving your health and well-being.")
    elif energy_keywords:
        print("Let’s boost your stamina!")
    elif stress_keywords:
        print("Fitness is a great way to relieve stress and feel more relaxed.")
    elif confidence_keywords:
        print("Awesome! Let’s make that happen!, After workout, you get wiings!")
    else:
        print("That sounds like a good reason! We'll focus on overall fitness.")

def get_fitness_level():
    # Gets the user's fitness level.
    beginner_keywords = ["beginner", "new", "starting", "just starting", "noob", "basic", "unfit", "not fit", "out of shape", "first time"]
    intermediate_keywords = ["intermediate", "average", "some experience", "moderate", "regularly", "somewhat fit", "medium", "used to", "decent shape"]
    advanced_keywords = ["advanced", "expert", "pro", "experienced", "athlete", "veteran", "very fit", "high level", "elite", "train hard", "competitive"]

    while True:
        print("\n" + responses.get("ask_level", "What's your current fitness level? (e.g., beginner, intermediate, advanced)"))
        user_input = input("Tell me your fitness level: ")
        tokens = process_text(user_input)


        is_beginner = any(fuzz.ratio(token, keyword) >= SIMILARITY
                          for token in tokens for keyword in beginner_keywords)
        is_intermediate = any(fuzz.ratio(token, keyword) >= SIMILARITY
                              for token in tokens for keyword in intermediate_keywords)
        is_advanced = any(fuzz.ratio(token, keyword) >= SIMILARITY
                          for token in tokens for keyword in advanced_keywords)

        print()
        if is_advanced:
             print("Nice! You're experienced. I’ve got some challenging workouts for you!")
             return "advanced"
        elif is_intermediate:
             if is_beginner:
                 print("It sounds like you might be between beginner and intermediate. Let's start with intermediate, but feel free to adjust!")
                 return "intermediate"
             else:
                 print("Great! You’ve got some experience. Let’s step it up!")
                 return "intermediate"
        elif is_beginner:
             print("Got it! You’re starting out or getting back into it. We’ll go at your pace.")
             return "beginner"
        else:
            print(responses.get('error'))
            return "beginner"


def generate_combined_workout_plan(goal, level, equipment):
    #Generates a workout plan list based on inputs using the JSON structure.
    workout = workout_plans.get(goal, {}).get(level, {}).get(equipment, [])
    return workout


def generate_diet_plan(diet_preference):
    # Generates a diet plan based on preference, with fallbacks."""
    default_plan = {
        "breakfast": ["Oatmeal with berries and nuts", "Scrambled eggs (or tofu) with spinach and whole-wheat toast"],
        "lunch": ["Large salad with grilled chicken/beans, lots of veggies, and vinaigrette", "Lentil soup with a side salad"],
        "dinner": ["Baked salmon (or tempeh) with roasted broccoli and quinoa", "Chicken (or chickpea) stir-fry with brown rice"],
        "snacks": ["Apple slices with almond butter", "Greek yogurt (or soy yogurt) with berries", "Handful of nuts"]
    }
    diet_plan = diet_plans.get(diet_preference, diet_plans.get("no preference", default_plan))
    return diet_plan

# Main function
def run_chatbot():
    print(responses.get("greeting", "Hello! I'm your AI Fitness Friend. Let's get you set up!"))

    goal = get_fitness_goals()

    diet = get_diet_preference()

    motivation = get_motivation_reason()

    level = get_fitness_level()

    equipment = get_equipment()

    print("\nOkay, generating your personalized plans...")
    workout_plan = generate_combined_workout_plan(goal, level, equipment)
    diet_plan_data = generate_diet_plan(diet)

    print("\n Your Personalized Workout Plan ")

    print(f"(Based on: {goal.title()}, {level.title()}, {equipment.title})")
    for i, exercise in enumerate(workout_plan, 1):
        print(f"{i}. {exercise}")

    print("\n Your Personalized Diet Plan Suggestions ")
    for meal_category, meals in diet_plan_data.items():
        print(f"\n {meal_category}:")
        for meal in meals:
            print(f"- {meal}")

    print("Remember to consult with a healthcare professional before starting any new fitness or diet program. Enjoy your journey!")

if __name__ == "__main__":
    run_chatbot()
