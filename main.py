from difflib import SequenceMatcher
from gensim.summarization import keywords
import web_scrapping
import questions


stat_questions = questions.stats_questions
application_questions = questions.application_questions
waterlooworks_questions = questions.waterlooworks_questions
international_questions = questions.international_questions


def string_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()


def initial_printing(category):
    print("\n")
    print(f"Please select a question in the category of {category}")


def category_check(category):
    user_confirmation = input(f"Your question is about {category} (Y|N): ").lower()
    return 'y' in user_confirmation


def ask_question_and_keywords(category):
    real_question = input("Please type your question: \n").lower()
    question_to_search = {"question": real_question, "keyword": [category]}
    keywords_to_search = keywords(real_question, words=1, lemmatize=True)
    if len(keywords_to_search) > 0:
        correct_keyword = input(f"Is '{keywords_to_search.upper()}' the correct keyword in your sentence?\n"
                                f"If yes, type 1, if not, type the correct keyword. \n")
    else:
        correct_keyword = input("Enter an appropriate keyword for your question.  \n")
    if correct_keyword == "1":
        question_to_search["keyword"].append(keywords_to_search)
    else:
        question_to_search["keyword"].append(correct_keyword)
    return question_to_search


def show_questions(questions_cat, category):
    index = 1
    for question in questions_cat:
        print(f"   {index}: {question}")
        index += 1

    user_question = int(input(f"Please choose a question, if none responds to your question, choose {len(questions_cat)}: "))

    if 1 <= user_question <= len(questions_cat):
        if user_question != len(questions_cat):
            print(f"Answer: {list(questions_cat.items())[user_question - 1][1]}")
            print("\n")
        else:
            search_q = ask_question_and_keywords(category)
            answer = web_scrapping.google_search(search_q)
            question = search_q["question"]
            new_question = {question: answer}
            new_question.update(questions_cat)

            global stat_questions, application_questions, waterlooworks_questions, international_questions
            if questions_cat == application_questions:
              application_questions = new_question
            elif questions_cat == stat_questions:
              stat_questions = new_question
            elif questions_cat == waterlooworks_questions:
              waterlooworks_questions = new_question
            elif questions_cat == international_questions:
              international_questions == new_question
            print(answer)
    else:
        print("Invalid choice\n")


CAT_1 = "Co-op Statistics"
CAT_2 = "Application Process"
CAT_3 = "WaterlooWorks"
CAT_4 = "Working Internationally"

categories = [CAT_1, CAT_2, CAT_3, CAT_4]
print("\n")
print("Welcome to WarriorBot. You can find everything needed about co-op at the University of Waterloo.\n")

should_continue = True
while should_continue:
    print("What would you like to learn more about co-op?")
    for i in range(len(categories)):
        print(f"  {i + 1}. {categories[i]}")
    user_category = input("Please pick a category: ").lower()

    if user_category == CAT_1 or string_similarity(user_category, CAT_1) >= 0.8 or user_category == "1":
        if user_category != CAT_1.lower():
            usr_confirmation = category_check(CAT_1)
            if usr_confirmation:
                initial_printing(CAT_1)
                show_questions(stat_questions, CAT_1)
            else:
                print("Error, please try again\n")
        else:
            initial_printing(CAT_1)
            show_questions(stat_questions, CAT_1)

    elif user_category == CAT_2 or string_similarity(user_category, CAT_2) >= 0.8 or user_category == "2":
        if user_category != CAT_2.lower():
            usr_confirmation = category_check(CAT_2)
            if usr_confirmation:
                initial_printing(CAT_2)
                show_questions(application_questions, CAT_2)
            else:
                print("Error, please try again\n")
        else:
            initial_printing(CAT_2)
            show_questions(application_questions, CAT_2)

    elif user_category == CAT_3 or string_similarity(user_category, CAT_3) >= 0.8 or user_category == "3":
        if user_category != CAT_3.lower():
            usr_confirmation = category_check(CAT_3)
            if usr_confirmation:
                initial_printing(CAT_3)
                show_questions(waterlooworks_questions, CAT_3)
            else:
                print("Error, please try again\n")
        else:
            initial_printing(CAT_3)
            show_questions(waterlooworks_questions, CAT_3)

    elif user_category == CAT_4 or string_similarity(user_category, CAT_4) >= 0.8 or user_category == "4":
        if user_category != CAT_4.lower():
            usr_confirmation = category_check(CAT_4)
            if usr_confirmation:
                initial_printing(CAT_4)
                show_questions(international_questions, CAT_4)
            else:
                print("Error, please try again\n")
        else:
            initial_printing(CAT_4)
            show_questions(international_questions, CAT_4)
    else:
        print("Invalid Choice!\n")

    to_continue = input("Do you have another question? (Y|N)").lower()
    if 'y' not in to_continue:
        should_continue = False
        print("\n")
        print("Thank you for using WarriorBot")
        rating = int(input("How would rate this experience on a scale of 1-10:  "))
        if 0 <= rating <= 10:
            with open("rating.txt", "a") as r:
                r.write(f"{rating}\n")



