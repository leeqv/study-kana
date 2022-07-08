import { show, hide } from './helpers-display.js';
import { removeAllChildNodes, getCookie } from './helpers-others.js'

var QUIZ_INFOS = {};

function quizHandler() {        
    (function() {   
        const { groups: { kana, quizNumber } } = /^\/(quiz)\/((?<kana>[HK])-(?<quizNumber>\d+)*)+\/$/.exec(window.location.pathname);  
        this.getQuizInfo = () => {return {kana, quizNumber}};

        var index, 
            currentQuestion, 
            score = 0,
            questions, 
            numOfQuestions;
        
        this.incrementScore = () => { score++ };
        this.getScore = () => score;
        
        this.getIndex = () => index;
        this.updateCurrentQuestion = () => {
            index = (index == undefined) ? 0 : ++index;    
            currentQuestion = questions[index];
        };
        this.getCurrentQuestion = () => currentQuestion;    

        this.getQuestions = () => questions;
        this.setQuestions = (qsObj) => {
            questions = qsObj;
            numOfQuestions = Object.keys(qsObj).length;
        };
        this.getNumOfQuestions = () => numOfQuestions;      
    }).apply(QUIZ_INFOS);

    fetch(`/load_quiz/${QUIZ_INFOS.getQuizInfo().kana}/${QUIZ_INFOS.getQuizInfo().quizNumber}/`)
    .then(response => response.json())
    .then(quiz => { QUIZ_INFOS.setQuestions(quiz.questions); })
    .then(() => { QUIZ_INFOS.updateCurrentQuestion(); })
    .then(() => {
        // Visuals
        (function showFirstQuestion() {
            showQuestion();
            document.getElementById('question-total').innerText = QUIZ_INFOS.getNumOfQuestions();
            //document.getElementById('question-id').innerText = QUIZ_INFOS.getIndex() + 1;
        })();

        // Next Question Btn handler
        document.getElementById('nextQuestionBtn').addEventListener('click', function() {
            if (QUIZ_INFOS.getIndex() < QUIZ_INFOS.getNumOfQuestions()) {
                showQuestion();
            } else { // last question
                showFinalScore();
            }
        });

        // Skip Button handler
        document.getElementById('skipBtn').addEventListener('click', function(){           
            checkAnswer(null, QUIZ_INFOS.getCurrentQuestion().question);
            QUIZ_INFOS.updateCurrentQuestion();
        });
    });
}

function showQuestion() {
    const question = QUIZ_INFOS.getCurrentQuestion().question;
    hide(document.getElementById('resultContainer'), document.getElementById('finalScoreDiv'));
    show(document.getElementById('js-quiz__body'), document.getElementById('skipBtn'));

    (function updateQuestion() {
        document.getElementById('questionDiv').innerText = question;
        document.getElementById('question-id').innerText = QUIZ_INFOS.getIndex() + 1;
    })();        

    (function showOptions() {
        const answersDiv = document.getElementById('answersDiv');
        // Clear previous options
        removeAllChildNodes(answersDiv);
        // Show new options
        let answers = QUIZ_INFOS.getCurrentQuestion().answers;
        [...answers].forEach(answer => {
            let optionBtn = document.createElement("button");
            optionBtn.innerText = answer;
            optionBtn.classList.add('c-quiz__option-btn', 'o-btn');
            optionBtn.setAttribute("data-answer", answer);
            optionBtn.setAttribute("type", "button");
            answersDiv.append(optionBtn);
        });
    })();
    
    (function optionBtnHandler() {
        let options = document.getElementsByClassName('c-quiz__option-btn');
        [...options].forEach(option => {
            option.addEventListener('click', function() {
                checkAnswer(option.dataset.answer, question);
                QUIZ_INFOS.updateCurrentQuestion();
            });
        });
    })();
}

function checkAnswer(answer, question) {
    fetch(`/check_answer/${QUIZ_INFOS.getQuizInfo().kana}/${QUIZ_INFOS.getQuizInfo().quizNumber}/`, {
        method: "POST",
        mode: 'same-origin',  
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            question: question,
            answer: answer,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) QUIZ_INFOS.incrementScore();
        return result;
    }).then( result => {
        // Save score to db if last question
        if (QUIZ_INFOS.getIndex() === QUIZ_INFOS.getNumOfQuestions()) {  
            saveScore();   
        }
        showResult(result);
    });    
}

function showResult(result) {    
    hide(document.getElementById('js-quiz__body'), document.getElementById('skipBtn'), document.getElementById('finalScoreDiv'));
    show(document.getElementById('resultContainer'));

    (function updateCorrectDiv() {
        document.getElementById('kana').innerText = result.correct["kana"];
        document.getElementById('romaji').innerText = result.correct["romaji"].toLowerCase();
        document.getElementById('ex-emoji').innerText = result.correct["ex_emoji"];
        document.getElementById('ex-english').innerText = result.correct["ex_english"].toLowerCase();
        document.getElementById('ex-romaji').innerText = result.correct["ex_romaji"].toLowerCase();
        document.getElementById('ex-kana').innerText = result.correct["ex_kana"];
    })();

    if (result.success) {
        showCorrectDiv();
    } else if (result.answered) {
        updateWrongDivInfo();
        showWrongDiv();
    } else {
        updateSkippedInfo();
        showWrongDiv();
    }

    function showCorrectDiv() {
        show(document.getElementById('check-span'));
        hide(document.getElementById('wrongDiv'), document.getElementById('correctDiv-header'));
    }

    function showWrongDiv() {
        hide(document.getElementById('check-span'));
        show(document.getElementById('wrongDiv'), document.getElementById('correctDiv-header'));
    }

    function updateWrongDivInfo() {
        document.getElementById('wrongDiv-header').innerText = 'You answered:';
        document.getElementById('answered-kana').innerText = result.answered["kana"];
        document.getElementById('answered-romaji').innerText = result.answered["romaji"].toLowerCase();
        document.getElementById('answered-ex-emoji').innerText = result.answered["ex_emoji"];
        document.getElementById('answered-ex-english').innerText = result.answered["ex_english"].toLowerCase();
        document.getElementById('answered-ex-romaji').innerText = result.answered["ex_romaji"].toLowerCase();
        document.getElementById('answered-ex-kana').innerText = result.answered["ex_kana"];
    }

    function updateSkippedInfo() {
        let wrongDivChildren = document.getElementById('wrongDiv-body').childNodes;
        [...wrongDivChildren].forEach(child => {
            child.innerText = '';
        });

        document.getElementById('wrongDiv-header').innerText = 'You skipped this question 🤷‍♀️';
    }
}

function saveScore() {
    var percentage = (QUIZ_INFOS.getScore() / QUIZ_INFOS.getNumOfQuestions())*100;
    fetch(`/save_score/${QUIZ_INFOS.getQuizInfo().kana}/${QUIZ_INFOS.getQuizInfo().quizNumber}/`, {
        method: "POST",
        mode: 'same-origin',  
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            score: percentage,
        })
    }).then(response => response.json())
    .then(result => {
        const nextDiv = document.getElementById('nextDiv'),
            backDiv = document.getElementById('backDiv');

        if (result.passed) {
            if (result.last_quiz) {
                nextDiv.innerHTML = 'Finished all lessons! Congrats!';
            } else {
                show(nextDiv);
                hide(backDiv);
            }
        } else {
            hide(nextDiv);
            show(backDiv);
        }

        // Show trophy
        if (result.added_trophy) {
            const trophyDiv = document.getElementById('trophyDiv');
            const numOfTrophies = result.added_trophy.length;

            if (numOfTrophies > 1){
                trophyDiv.innerText = "New trophies: ";
                show(trophyDiv);
            } else if (numOfTrophies === 1) {
                trophyDiv.innerText = "New trophy: ";
                show(trophyDiv);
            }

            for (let i = 0; i < result.added_trophy.length; i++) {
                let trophy = result.added_trophy[i];
                if (i > 0) {
                    trophyDiv.innerText += ", " + " 🏆 " + trophy;
                } else {
                    trophyDiv.innerText += "🏆 " + trophy;
                }
            }
        }
    });
}

function showFinalScore() {
    var finalScore = QUIZ_INFOS.getScore();
    hide(document.getElementById('quizDiv'), document.getElementById('resultContainer'));
    show(document.getElementById('finalScoreDiv'));
    
    const finalScoreSpan = document.getElementById('finalScore');
    finalScoreSpan.innerText = finalScore;
    finalScoreSpan.className = 'highlighted';

    var totalQuestions = QUIZ_INFOS.getNumOfQuestions();
    document.getElementById('totalQuestions').innerText = totalQuestions;
    
    const emojiDiv = document.getElementById('finalscore-emoji');
    let emoji;
    if (finalScore === totalQuestions){
        emoji = "😲👏";
        finalScoreSpan.classList.add('u-text-orange');      
    } else if (finalScore >= (totalQuestions * 0.6)){
        emoji = "😊👍";
    } else {
        emoji = "😞";
        finalScoreSpan.classList.add('u-text-gray');
    }
    emojiDiv.innerText = emoji;
}

export { quizHandler };