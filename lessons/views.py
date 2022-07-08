from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.models import User
from results.models import UserProfile
from .models import HiraganaLesson, HiraganaLetter, KatakanaLesson, KatakanaLetter
from quizzes.models import HiraganaQuiz, KatakanaQuiz
from questions.models import HiraganaQuestion, KatakanaQuestion
from results.models import HiraganaResult, KatakanaResult, Trophy
import json
from django.http import JsonResponse
import random
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/study')
    return HttpResponseRedirect('/about')

def about(request):
    return render(request, 'lessons/index.html')

def register(request):
    if request.user.is_authenticated:
       return HttpResponseRedirect('/study')

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lessons/register.html", {
                "message": "Passwords must match."
            })
        # Ensure all fields are filled in    
        if (len(username) == 0) or (len(email) == 0) or len(password) == 0 or (len(confirmation) == 0):
            return render(request, "lessons/register.html", {
                "message": "Please fill in all fields."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
            # Create userprofile
            new_profile = UserProfile(user=user)
            new_profile.current_H_lesson = HiraganaLesson.objects.get(order=1)
            new_profile.current_K_lesson = KatakanaLesson.objects.get(order=1)
            new_profile.save()
                   
        except IntegrityError:
            return render(request, "lessons/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))   
        
    else:
        return render(request, "lessons/register.html")

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/study')
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/study")
        else:
            return render(request, "lessons/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lessons/login.html")

@login_required(login_url='/login')
def menu_view(request, menu):
    userprofile = UserProfile.objects.get(user=request.user)
    if menu == 'study':
        H_lesson = userprofile.current_H_lesson
        K_lesson = userprofile.current_K_lesson
    elif menu == 'review':
        H_lesson = userprofile.finished_H_lessons.all()
        K_lesson = userprofile.finished_K_lessons.all()
    elif menu == 'watchlist':
        H_lesson = userprofile.hiragana_watchlist.all()
        K_lesson = userprofile.katakana_watchlist.all()

    return render(request, f'lessons/menu_{menu}.html', {
        "userprofile": userprofile,
        "lessonsDict": [['Hiragana', H_lesson], ['Katakana', K_lesson]]
    })

@login_required(login_url='/login')
def profile_view(request):
    userprofile = UserProfile.objects.get(user=request.user)

    hiragana_scores = HiraganaResult.objects.filter(user=request.user)
    hiragana_passed = len(HiraganaResult.objects.filter(user=request.user, score__gte = 60))
    hiragana_total_quizzes = len(HiraganaQuiz.objects.all())
    hiragana_percent_progress = (hiragana_passed/hiragana_total_quizzes)*100

    katakana_scores = KatakanaResult.objects.filter(user=request.user)
    katakana_passed = len(KatakanaResult.objects.filter(user=request.user, score__gte = 60))
    katakana_total_quizzes = len(KatakanaQuiz.objects.all())
    katakana_percent_progress = (katakana_passed/katakana_total_quizzes)*100

    trophy_list = Trophy.objects.all()

    return render(request, 'lessons/profile.html', {
        "userprofile": userprofile,
        "hiragana_scores": hiragana_scores,
        "hiragana_percent_progress": hiragana_percent_progress,
        "katakana_scores": katakana_scores,
        "katakana_percent_progress": katakana_percent_progress,
        "trophy_list": trophy_list,
    })


@login_required(login_url='/login')
def lesson_view(request, menu, kana, lesson_number, **kwargs):
    letter = kwargs.get('letter', "")
    user_profile = UserProfile.objects.get(user=request.user)
    # Check if lesson exists
    try:
        if kana == "H":
            lesson = HiraganaLesson.objects.get(order=lesson_number)
            current_lesson = user_profile.current_H_lesson
            finished_lessons = user_profile.finished_H_lessons.all()
        elif kana == "K":
            lesson = KatakanaLesson.objects.get(order=lesson_number)
            current_lesson = user_profile.current_K_lesson
            finished_lessons = user_profile.finished_K_lessons.all()
    except:
        return HttpResponseRedirect('/study')

    # Check where this lesson is stored in user's profile
    if lesson == current_lesson:
        status = "current"
    else:
        if lesson in finished_lessons:
            status = "finished"
        else:
            status = "unfinished"

    # Check if letter is in lesson
    lesson_letters = []
    for lesson_letter in lesson.get_letters():
        lesson_letters.append(lesson_letter.romaji)

    # Redirect to lesson's first letter if no letter in URL
    if (len(letter) == 0) and (status != "unfinished"):
        letter = lesson_letters[0]
        return HttpResponseRedirect(f'/{menu}/{kana}-{lesson_number}/{letter}')

    # Check if .../fin (all letters already shown)
    if letter == "fin":
        if menu == "study":
            return render(request, 'lessons/endoflesson.html', {
                "kana": kana,
                "lesson": lesson,
                "lesson_letters": lesson_letters,
                "current_lesson": current_lesson,
            })
        elif menu == "review":
            return HttpResponseRedirect(f'/review/{kana}-{lesson_number}/')

    if letter not in lesson_letters:
        return HttpResponseRedirect('/study')

    if kana == "H":
        letter_db = HiraganaLetter.objects.get(romaji=letter)
        # Check if letter is in watchlist
        in_watchlist = UserProfile.objects.filter(user=request.user, hiragana_watchlist=letter_db).exists()    
    elif kana == "K":
        letter_db = KatakanaLetter.objects.get(romaji=letter)
        # Check if letter is in watchlist
        in_watchlist = UserProfile.objects.filter(user=request.user, katakana_watchlist=letter_db).exists()  
    


    # Redirect to respective pages
    if (status == "current" and menu == "study") or (status == "finished" and menu == "review"):
        return render(request, 'lessons/lesson.html', {
            "letter": letter_db,
            "lesson_letters": lesson_letters,
            "kana" : kana,
            "in_watchlist": in_watchlist,
        })
    elif status == "unfinished":
        return HttpResponseRedirect('/study')
    else:
        # Redirect to other menu
        menu_choices = ["study", "review"]
        menu_choices.remove(menu)
        return HttpResponseRedirect(f'/{menu_choices[0]}/{kana}-{lesson_number}/{letter}')

@login_required(login_url='/login')
def quiz_view(request, kana, quiz_number):
	# Pass questions to JS
    next_lesson = int(quiz_number) + 1

    return render(request, 'lessons/quiz.html', {
        "kana": kana,
        "quiz_number": quiz_number
    })

def create_questions_dict(dict, question_id, questions):
    random_id_array = list(range(0, len(questions)))
    random.shuffle(random_id_array)

    for i in range(0,len(questions),1):
        # Show options
        answers = []
        for answer in questions[random_id_array[i]].get_answers():
            answers.append(answer.text.romaji)
        random.shuffle(answers)

        # Create dictionary for questions and answers
        item = {'question': questions[random_id_array[i]].text.kana, 'answers': answers}
        dict[question_id] = item

        question_id += 1

    return dict

def load_quiz(request, kana, quiz_number):
    # Check if quiz exists
    user_profile = UserProfile.objects.get(user=request.user)
    try:
        if kana == "H":
            quiz = HiraganaQuiz.objects.get(order=quiz_number)
            current_lesson = user_profile.current_H_lesson
            # Get failed questions, if there's any
            failed_questions = user_profile.failed_H_questions.all()
        elif kana == "K":
            quiz = KatakanaQuiz.objects.get(order=quiz_number)
            current_lesson = user_profile.current_K_lesson
            failed_questions = user_profile.failed_K_questions.all()
    except:
        return HttpResponseRedirect('/study')

    # Check if lesson is NOT related to quiz is the current_lesson 
    if quiz.lesson != current_lesson:
        return HttpResponseRedirect("/study")

	# Get questions
    questions = quiz.get_questions()
    
    # Create a dictionary of questions from current quiz
    questions_dict = {}
    question_id = 0
    create_questions_dict(questions_dict, question_id, questions)

    # Append questions from failed questions
    question_id = len(questions)
    create_questions_dict(questions_dict, question_id, failed_questions)

    json_dump = json.dumps(questions_dict)
    json_load = json.loads(json_dump)

    # Pass questions to JS
    return JsonResponse({"questions": json_load}, status=201)

def check_answer(request, kana, quiz_number):
    data = json.loads(request.body)    
    question = data.get('question')
    answer = data.get('answer')

    userprofile = UserProfile.objects.get(user=request.user)
    user = request.user

    # Find answer for this question
    if kana == "H":
        question_letter = HiraganaLetter.objects.get(kana=question)
        correct_answer = HiraganaQuestion.objects.get(text=question_letter).get_correct_answer().text.romaji
        try:
            answered_letter = HiraganaLetter.objects.get(romaji=answer)
        except ObjectDoesNotExist:
            return JsonResponse({
                "success": False,
                "correct": {
                    "kana": question_letter.kana,
                    "romaji": question_letter.romaji,
                    "ex_emoji": question_letter.ex_emoji,
                    "ex_english": question_letter.ex_english,
                    "ex_romaji": question_letter.ex_romaji,
                    "ex_kana": question_letter.ex_kana,
                }
            })

    elif kana == "K":
        question_letter = KatakanaLetter.objects.get(kana=question)
        correct_answer = KatakanaQuestion.objects.get(text=question_letter).get_correct_answer().text.romaji

        try:
            answered_letter = KatakanaLetter.objects.get(romaji=answer)
        except ObjectDoesNotExist:
            return JsonResponse({
                "success": False,
                "correct": {
                    "kana": question_letter.kana,
                    "romaji": question_letter.romaji,
                    "ex_emoji": question_letter.ex_emoji,
                    "ex_english": question_letter.ex_english,
                    "ex_romaji": question_letter.ex_romaji,
                    "ex_kana": question_letter.ex_kana,
                }
            })
        

    # Check if correct answer
    success = False
    if correct_answer == answer:
        success = True
        remove_from_failed_questions(question, kana, userprofile, user)
    else:
        # Add to failed questions list
        add_to_failed_questions(question, kana, userprofile, user)

    return JsonResponse({
        "success": success,
        "correct": {
            "kana": question_letter.kana,
            "romaji": question_letter.romaji,
            "ex_emoji": question_letter.ex_emoji,
            "ex_english": question_letter.ex_english,
            "ex_romaji": question_letter.ex_romaji,
            "ex_kana": question_letter.ex_kana,
        },
        "answered": {
            "kana": answered_letter.kana,
            "romaji": answered_letter.romaji,
            "ex_emoji": answered_letter.ex_emoji,
            "ex_english": answered_letter.ex_english,
            "ex_romaji": answered_letter.ex_romaji,
            "ex_kana": answered_letter.ex_kana,
        }

        
    })

def remove_from_failed_questions(question, kana, userprofile, user):
    if kana == "H":
        question_letter = HiraganaLetter.objects.get(kana=question)
        question_db = HiraganaQuestion.objects.get(text=question_letter)
        if UserProfile.objects.filter(user=user, failed_H_questions=question_db).exists():
            # Remove from failed questions list
            userprofile.failed_H_questions.remove(question_db.pk)            

    else:
        question_letter = KatakanaLetter.objects.get(kana=question)
        question_db = KatakanaQuestion.objects.get(text=question_letter)
        if UserProfile.objects.filter(user=user, failed_K_questions=question_db).exists():
            # Remove from failed questions list
            userprofile.failed_K_questions.remove(question_db.pk) 

def add_to_failed_questions(question, kana, userprofile, user):
    if kana == "H":
        question_letter = HiraganaLetter.objects.get(kana=question)
        question_db = HiraganaQuestion.objects.get(text=question_letter)
        if not UserProfile.objects.filter(user=user, failed_H_questions=question_db).exists():
            # Add to failed questions list
            userprofile.failed_H_questions.add(question_db.pk)            

    else:
        question_letter = KatakanaLetter.objects.get(kana=question)
        question_db = KatakanaQuestion.objects.get(text=question_letter)
        if not UserProfile.objects.filter(user=user, failed_K_questions=question_db).exists():
            # Add to failed questions list
            userprofile.failed_K_questions.add(question_db.pk)

def save_score(request, kana, quiz_number):
    data = json.loads(request.body)    
    score = data.get('score')

    userprofile = UserProfile.objects.get(user=request.user)
    passed = False
    added_trophy = []

    if kana == "H":
        quiz = HiraganaQuiz.objects.get(order=quiz_number)

        # Check if last quiz
        last_quiz_db = HiraganaQuiz.objects.order_by('-order')[0]
        if quiz == last_quiz_db:
            last_quiz = True
        else:
            last_quiz = False
        
        # User's re-take quiz
        if (HiraganaResult.objects.filter(user=request.user, quiz=quiz).exists()):
            # Update score
            result = HiraganaResult.objects.get(quiz=quiz, user=request.user)
            result.score = score
            result.save()
        # User's first time taking the quiz
        else:
            # Create new HiraganaResult instance
            result = HiraganaResult(quiz=quiz, user=request.user, score=score)
            result.save()

        # If score is >60: 
        if score >= 60:
            passed = True

            # add this lesson to finished lessons
            lesson = HiraganaLesson.objects.get(order=quiz_number)
            userprofile.finished_H_lessons.add(lesson)

            # change current lesson to quiz_number + 1
            if last_quiz == False:
                new_lesson = HiraganaLesson.objects.get(order=int(quiz_number)+1)
                userprofile.current_H_lesson = new_lesson
            else:
                userprofile.current_H_lesson = None
            userprofile.save()

            # Check for trophy (done-trophy)
            trophy_list = [1,5,10]
            if int(quiz_number) in trophy_list:
                trophy = Trophy.objects.get(code=f"H-Done-{str(quiz_number).zfill(2)}")
                has_trophy = UserProfile.objects.filter(user=request.user, trophies=trophy).exists()

                if has_trophy==False:
                    UserProfile.objects.get(user=request.user).trophies.add(trophy)
                    added_trophy.append(trophy.name)

        # Check for trophy
        if score == 100:
            # Create perfect quizzes array (including this quiz)
            perfect_quizzes = []
            for perfect_quiz in HiraganaResult.objects.filter(user=request.user, score=100):
                perfect_quizzes.append(perfect_quiz.quiz.order)

            # Create trophy list
            trophy_list = [1,2,3,5,10]
                
            # For perfect trophy > 1
            if len(perfect_quizzes) in trophy_list:       
                trophy = Trophy.objects.get(code=f"H-Perfect-{str(len(perfect_quizzes)).zfill(2)}")
                has_trophy = UserProfile.objects.filter(user=request.user, trophies=trophy).exists()

                if has_trophy==False:
                    UserProfile.objects.get(user=request.user).trophies.add(trophy)
                    added_trophy.append(trophy.name)


    elif kana == "K":
        quiz = KatakanaQuiz.objects.get(order=quiz_number)

        # Check if last quiz (quiz variable CAN USE)
        last_quiz_db = KatakanaQuiz.objects.order_by('-order')[0]
        if quiz == last_quiz_db:
            last_quiz = True
        else:
            last_quiz = False
        
        # User's re-take quiz
        if (KatakanaResult.objects.filter(user=request.user, quiz=quiz).exists()):
            # Update score
            result = KatakanaResult.objects.get(quiz=quiz, user=request.user)
            result.score = score
            result.save()
        # User's first time taking the quiz
        else:
            # Create new KatakanaResult instance
            result = KatakanaResult(quiz=quiz, user=request.user, score=score)
            result.save()

        # If score is >60: 
        if score >= 60:
            passed = True

            # add this lesson to finished lessons
            lesson = KatakanaLesson.objects.get(order=quiz_number)
            userprofile.finished_K_lessons.add(lesson)

            # change current lesson to quiz_number + 1
            if last_quiz == False:
                new_lesson = KatakanaLesson.objects.get(order=int(quiz_number)+1)
                userprofile.current_K_lesson = new_lesson
                userprofile.save()
            else:
                userprofile.current_K_lesson = None
                userprofile.save()

            # Check for trophy (done-trophy)
            trophy_list = [1,5,10]
            if int(quiz_number) in trophy_list:
                trophy = Trophy.objects.get(code=f"K-Done-{str(quiz_number).zfill(2)}")
                has_trophy = UserProfile.objects.filter(user=request.user, trophies=trophy).exists()

                if has_trophy==False:
                    UserProfile.objects.get(user=request.user).trophies.add(trophy)
                    added_trophy.append(trophy.name)

        # Check for trophy
        if score == 100:
            # Create perfect quizzes array (including this quiz)
            perfect_quizzes = []
            for perfect_quiz in KatakanaResult.objects.filter(user=request.user, score=100):
                perfect_quizzes.append(perfect_quiz.quiz.order)

            # Create trophy list
            trophy_list = [1,2,3,5,10]

            if len(perfect_quizzes) in trophy_list:       
                trophy = Trophy.objects.get(code=f"K-Perfect-{str(len(perfect_quizzes)).zfill(2)}")
                has_trophy = UserProfile.objects.filter(user=request.user, trophies=trophy).exists()

                if has_trophy==False:
                    UserProfile.objects.get(user=request.user).trophies.add(trophy)
                    added_trophy.append(trophy.name)

    return JsonResponse({"passed": passed, "last_quiz": last_quiz, "added_trophy": added_trophy})

def update_watchlist(request):
    data = json.loads(request.body)    
    letter_kana = data.get('letter')

    # Check if hiragana or katakana
    if HiraganaLetter.objects.filter(kana=letter_kana).exists():
        letter = HiraganaLetter.objects.get(kana=letter_kana)
        writing = "H"
        # Check if in user's watchlist
        in_watchlist = UserProfile.objects.filter(user=request.user, hiragana_watchlist=letter).exists()
    elif KatakanaLetter.objects.filter(kana=letter_kana).exists():
        letter = KatakanaLetter.objects.get(kana=letter_kana)
        writing = "K"
        # Check if in user's watchlist
        in_watchlist = UserProfile.objects.filter(user=request.user, katakana_watchlist=letter).exists()

    userprofile = UserProfile.objects.get(user=request.user)
    
    # Add or remove
    update = "added"
    if writing == "H":
        if in_watchlist:
            userprofile.hiragana_watchlist.remove(letter.pk)
            update = "removed"
        else:
            userprofile.hiragana_watchlist.add(letter.pk)
    else:
        if in_watchlist:
            userprofile.katakana_watchlist.remove(letter.pk)
            update = "removed"
        else:
            userprofile.katakana_watchlist.add(letter.pk)

    return JsonResponse({"update": update})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def error_404(request, exception):
    return render(request,'lessons/404.html')

def error_500(request):
    return render(request,'lessons/500.html')