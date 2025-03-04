import datetime
import random
import math
from datetime import date
import flask
from flask import Flask, request, render_template, jsonify
from turtledemo.clock import current_day

random.seed(43459864368)

bigMacCalories = 580
bigMacGrams = 220
bigMacHeightFeet = 3.35/12
footballFieldLengthFeet = 360
footballFieldWidthFeet = 160
costcoHotDogPrice = 1.5
costcoHotDogCalories = 570
theGodFatherMinutes = 175
fordF1502025Price = 38810

currentYear = (int(str(datetime.datetime.now())[0:4]))
currentMonth = (int(str(datetime.datetime.now())[5:7]))
currentDay = (int(str(datetime.datetime.now())[8:10]))
currentDay = 14
currentDate = date(currentYear,currentMonth, currentDay)
startDate = date(2025, 2, 15)

def numOfDays(date1, date2):
    #check which date is greater to avoid days output in -ve number
    if date2 > date1:
        return (date2-date1).days
    else:
        return (date1-date2).days

def extract_quoted_substring(filepath, line_number, quote_pair_number):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()

        if line_number <= 0 or line_number > len(lines):
            print(f"Error: Line number {line_number} is out of range.")
            return None

        target_line = lines[line_number - 1]  # Adjust for 0-based indexing

        quote_indices = []
        start_index = 0
        while True:
            start_quote_index = target_line.find('"', start_index)
            if start_quote_index == -1:
                break
            end_quote_index = target_line.find('"', start_quote_index + 1)
            if end_quote_index == -1:
                break
            quote_indices.append((start_quote_index, end_quote_index))
            start_index = end_quote_index + 1

        if not quote_indices or quote_pair_number <= 0 or quote_pair_number > len(quote_indices):
            print(f"Error: Quote pair number {quote_pair_number} not found on line {line_number}.")
            return None

        start, end = quote_indices[quote_pair_number - 1]  # Adjust for 0-based indexing
        return target_line[start + 1:end]

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def getDailyQuestion():
    modes = 4
    gameType = currentDay % modes
    gameNo = numOfDays(startDate, currentDate)
    cycle = math.floor(gameNo/4) + 1
    if (gameType == 0):
        answerPath = "./answers/size.txt"
        runDailyQuestion(answerPath, cycle)
    elif (gameType == 1):
        answerPath = "./answers/energy.txt"
        runDailyQuestion(answerPath, cycle)
    elif (gameType == 2):
        answerPath = "./answers/time.txt"
        runDailyQuestion(answerPath, cycle)
    elif (gameType == 3):
        answerPath = "./answers/money.txt"
        runDailyQuestion(answerPath, cycle)

def runDailyQuestion(answerPath, cycle):
    print(extract_quoted_substring(answerPath, cycle, 1))
    i = 0
    gotAnswer = 0
    answerSteps = extract_quoted_substring(answerPath, cycle, 2)
    citation = extract_quoted_substring(answerPath, cycle, 3)
    correctAnswer = int(eval(answerSteps))
    while (i < 6 or gotAnswer == 0):
        guess = int(input("Guess Here:"))
        if (guess >= (correctAnswer * .95)) and (guess <= (correctAnswer * 1.05)):
            print(f"yay you got it right! Correct answer was {correctAnswer}. Citation: {citation}")
            gotAnswer = 1
        elif guess < correctAnswer*.1:
            i+=1
            print("your guess was lower by more than a factor of 10.")
        elif guess > correctAnswer*10:
            i+=1
            print("your guess was higher by more than a factor of 10.")
        elif guess >= correctAnswer*.1 and guess < correctAnswer*.8:
            i+=1
            print("your guess was lower by less than a factor of 10.")
        elif guess >= correctAnswer*.1 and guess < correctAnswer*.8:
            i+=1
            print("your guess was greater by less than a factor of 10.")
        elif guess <= correctAnswer*10 and guess > correctAnswer*1.2:
            i+=1
            print("your guess is within 20% of the answer, you guessed low.")
        elif guess >= correctAnswer*1.11 and guess <= correctAnswer*1.2:
            i+=1
            print("your guess is within 20% of the answer, you guessed high.")
        elif guess >= correctAnswer*.9 and guess <= correctAnswer*.95:
            i+=1
            print("your guess is within 10% of the answer, you guessed low.")
        elif guess >= correctAnswer*1.05 and guess <= correctAnswer*1.1:
            i+=1
            print("your guess is within 10% of the answer, you guessed high.")
        if (6-i > 0):
            print(f"You have {6-i} guesses remaining")
        elif (6-i == 0):
            print("Game over")
            return


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  # Allow both GET and POST
def index():
    if request.method == 'POST':
        # Get data from the form (if using form data)
        data_from_form = request.form.get('my_data')

        # Get data from JSON payload (if using JSON)
        data_from_json = request.get_json()

        # Process the data (example: just print it)
        print("Data from form:", data_from_form)
        print("Data from JSON:", data_from_json)

        # You can return data to the HTML page
        # Option 1: Render a template with the data
        return render_template('index.html', received_data=data_from_form or data_from_json)  #Pass data to template

        # Option 2: Return JSON response (useful for AJAX)
        # return jsonify({'message': 'Data received', 'data': data_from_form or data_from_json})

    return render_template('index.html')  # Render the HTML form on GET request


if __name__ == '__main__':
    app.run(debug=True)  # Run in debug mode for development

getDailyQuestion()
