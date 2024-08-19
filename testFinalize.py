# Import libraries
import telegram
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Define NLP functions
def tokenize_and_stem(text):
    # Tokenize the input text
    tokens = word_tokenize(text)

    # Stem each token using Porter Stemmer
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    return stemmed_tokens

# Define chatbot functions
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(
    f"Hi {user.first_name}, I am your heart health self-management chatbot. How can I assist you today?\n"
    "Prompt /help for assistance."
    )

# Define the function to handle /help command
def help_command(update: Update, context: CallbackContext) -> None:
    help_message = """
    Welcome to the Heart Health Chatbot!

    Feel free to choose:
    1. /symptoms: Use this command to discover the probability of having heart disease.
    2. /habit: Use command to discover the solution that causes heart disease.
    3. /prevention: Use this command to learn about ways to prevent heart disease and maintain a healthy heart.
    4. /treatment: Use this command to discover the recommended treatment for your condition.
    5. /medicine: Use this command to discover medicine for heart disease.
    """
    update.message.reply_text(help_message)

def process_input(update: Update, context: CallbackContext) -> None:
    
    # Replace 'your_excel_file.xlsx' with the actual path to your Excel file
    excel_file_path = 'C:/Users/LENOVO/Downloads/code/test1.xlsx'
    df = pd.read_excel(excel_file_path)
    
    user_input = update.message.text.lower()
    
    # Implement logic based on user input
    if user_input.startswith('/symptoms'):

        # Ask the user for their current symptom
        update.message.reply_text('Please tell me your current symptom.')

        # Listen for the user's response
        context.user_data['waiting_for_symptoms'] = True

    elif context.user_data.get('waiting_for_symptoms', False):
        # User has provided their current symptom
        context.user_data['waiting_for_symptoms'] = False

        # Pass the user's input to the tokenize_and_stem function
        processed_input = tokenize_and_stem(user_input)

        # Access the 'symptoms' column (corrected name)
        symptom_words = df['symptoms'].tolist()

        # Check if the processed input contains relevant keywords (pre-processing)
        if any(keyword in processed_input for keyword in symptom_words):
            update.message.reply_text('This is the probability of having a heart disease. Please consult with your healthcare provider.')
    
            # Ask about solution
            update.message.reply_text('Now, tell me about your habit or background history. This information will be collected to identify your specific solution to reduce your symptoms?')

            # Set a flag for waiting for solution
            context.user_data['waiting_for_solution'] = True

        else:
            update.message.reply_text('No relevant symptom identified. Prompt /help for assistance.')


    elif context.user_data.get('waiting_for_solution', False):
        # User is providing information about habit
        context.user_data['waiting_for_solution'] = False
    
        # Process the user's input for solution
        processed_solution = tokenize_and_stem(user_input)

        # Access the 'habit' column (assuming both habit and solution are in the same column)
        solution_data = df[['habit', 'solution']].values
    
        # Check if the processed input contains relevant keywords
        detected_solution = None
        for habit, solution in solution_data:
            solution_words = tokenize_and_stem(habit)
            if any(keyword in processed_solution for keyword in solution_words):
                detected_solution = solution
                break

        if detected_solution:
            update.message.reply_text(f'Your solution is {detected_solution}.')
        else:
            update.message.reply_text('No specific symptom identified.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    elif user_input.startswith('/habit'):
        # Ask about habit
        update.message.reply_text('Can you tell me about your habit or background history? This information will be collected to identify your specific solution and the probability of having a heart disease.')

        # Listen for the user's response
        context.user_data['waiting_for_solution1'] = True

    elif context.user_data.get('waiting_for_solution1', False):
        # User is providing information about habit
        context.user_data['waiting_for_solution1'] = False

        # Process the user's input for solution
        processed_solution1 = tokenize_and_stem(user_input)

        # Access the 'habit' and 'probability' columns
        habits_and_probabilities = df[['habit', 'probability', 'solution1']].values

        # Initialize variables to store detected values
        detected_solution1 = None
        detected_probability = None

        for habit, probability, solution1 in habits_and_probabilities:
            habit_words = tokenize_and_stem(habit)

            # Check if the processed input contains relevant keywords for both habit and probability
            if any(keyword in processed_solution1 for keyword in habit_words):
                detected_solution1 = solution1
                detected_probability = probability

            # Break out of the loop if both values are found
            if detected_solution1 is not None and detected_probability is not None:
                break

        if detected_solution1 is not None:
            # Check if both solution and probability are detected
            if detected_probability is not None:
                update.message.reply_text(f'Your solution is {detected_solution1}. ')
                update.message.reply_text(f'Your probability of having heart disease is {detected_probability}.')
                
            else:
                update.message.reply_text(f'Your solution is {detected_solution1}. Probability information not available.')
        else:
            # Handle the case when no solution is detected
            update.message.reply_text('I couldn\'t detect a solution based on your input. Please provide more information.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Implement logic based on user input
    elif user_input.startswith('/prevention'):
        # Ask if the user wants tips on prevention
        update.message.reply_text('Would you like to know preventive measures to reduce the risk of heart disease? (Yes/No)')
        context.user_data['waiting_for_preventive'] = True

    elif context.user_data.get('waiting_for_preventive', False):
        # User is responding to the preventive measures question
        context.user_data['waiting_for_preventive'] = False

        if user_input.lower().strip().startswith('yes'):
            # User wants personalized recommendations
            # Ask the user to provide information about their stages condition
            update.message.reply_text('What do you like to know in detail to prevent heart disease? Please choose either Lifestyle/Diet/Exercise')

            # Set a flag for waiting for the user's information
            context.user_data['waiting_for_information'] = True

        else:
            # User does not want personalized recommendations
            update.message.reply_text('If you have any inquiries, feel free to ask.')

    elif context.user_data.get('waiting_for_information', False):
        # User is providing information about their preventive measures choice
        context.user_data['waiting_for_information'] = False

        # Process the user's input for personalized recommendations
        processed_preventive = tokenize_and_stem(str(user_input))  # Convert to string before tokenization

        # Access the relevant columns in your DataFrame (e.g., 'information', 'preventive')
        preventive_data = df[['preventive', 'information']].values

        # Check if the processed input contains relevant keywords
        detected_information = None
        for preventive, information in preventive_data:
            preventive_words = tokenize_and_stem(str(preventive))  # Convert to string before tokenization
            if any(keyword in processed_preventive for keyword in preventive_words):
                detected_information = information
                break

        if detected_information:
            update.message.reply_text(f'Based on your choices, here are some personalized preventive recommendations: {detected_information}.')
        else:
            update.message.reply_text('No specific preventive recommendations identified.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Implement logic based on user input
    elif user_input.startswith('/treatment'): 
        # Ask if the user wants personalized recommendations
        update.message.reply_text('Would you like personalized treatment recommendations based on your health condition? (Yes/No)')
        context.user_data['waiting_for_treatment'] = True

    elif context.user_data.get('waiting_for_treatment', False):
        # User is responding to the personalized treatment question
        context.user_data['waiting_for_treatment'] = False

        if user_input.lower().strip().startswith('yes'):
            # User wants personalized recommendations
            # Ask the user to provide information about their stages condition
            update.message.reply_text('Please provide your stages condition (one/two/three/four).')

            # Set a flag for waiting for the user's stages information
            context.user_data['waiting_for_stages'] = True

        else:
            # User does not want personalized recommendations
            update.message.reply_text('If you have any inquiries, feel free to ask. We kindly advise consulting with your healthcare provider for personalized guidance.')

    elif context.user_data.get('waiting_for_stages', False):
        # User is providing information about their stages condition
        context.user_data['waiting_for_stages'] = False

        # Process the user's input for personalized recommendations
        processed_stages = tokenize_and_stem(user_input)


        # Access the relevant columns in your DataFrame (e.g., 'stages_condition', 'treatment')
        treatment_data = df[['stages', 'treatment']].values

        # Check if the processed input contains relevant keywords
        detected_treatment = None
        for stages, treatment in treatment_data:
            stages_words = tokenize_and_stem(stages)
            if any(keyword in processed_stages for keyword in stages_words):
                detected_treatment = treatment
                break

        if detected_treatment:
            update.message.reply_text(f'Based on your stages condition, the recommended treatment is {detected_treatment}.')
        else:
            update.message.reply_text('No specific treatment recommendation identified.')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Implement logic based on user input
    elif user_input.startswith('/medicine'):
        # Ask about symptoms or problems
        update.message.reply_text('Please tell me your symptoms or problems, and I will provide appropriate medicine.')

        # Listen for the user's response
        context.user_data['waiting_for_medicine'] = True

    elif context.user_data.get('waiting_for_medicine', False):
        # User is providing information about symptoms or problems
        context.user_data['waiting_for_medicine'] = False

        # Process the user's input for symptoms or problems
        processed_medicine = tokenize_and_stem(user_input)

        # Access the 'medicine', 'problem', and 'effect' columns
        problem_data = df[['problem', 'medicine', 'effect']].values

        # Initialize variables to store detected values
        detected_medicine = None
        detected_effect = None

        for problem, medicine, effect in problem_data:
            medicine_words = tokenize_and_stem(problem)

            # Check if the processed input contains relevant keywords
            if any(keyword in processed_medicine for keyword in medicine_words):
                detected_medicine = medicine
                detected_effect = effect

            # Break out of the loop if all values are found
            if detected_medicine is not None and detected_effect is not None:
                break

        if detected_medicine is not None:
            # Check if all values are detected
            update.message.reply_text(f'Based on your symptoms, the recommended medicine is {detected_medicine}.')
            update.message.reply_text(f'The medication may cause the following side effects: {detected_effect}.')
        else:
            # Handle the case when no medicine is detected
            update.message.reply_text('I couldn\'t detect a suitable medicine based on your input. Please provide more information.')


    else:
        update.message.reply_text('Invalid command. Type /help for assistance.') 


# Integrate with Telegram
def main():
    bot_token = '6744118023:AAEB27jCurAx4PCi1u_XR1rQzC0QX5GFt0Q'  # Replace with your actual bot token
    updater = Updater(bot_token)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(None, process_input))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

# Step 8: Execute the main function
if __name__ == '__main__':
    main()