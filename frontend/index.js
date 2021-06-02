// const host = "https://artificial-non-intelligence.herokuapp.com"
const host = "http://127.0.0.1:8000"

var currentQuestionId = null
var score = 0

window.addEventListener('load', function () {

    document.getElementById("score").innerHTML = score

    getNewQuestion()

    document.querySelectorAll('.button').forEach(button => {
        button.addEventListener('click', function (event) {
            sendAnswer(currentQuestionId, button.id)
            getNewQuestion()
        })
    })

})

function getNewQuestion() {

    const url = new URL(host + "/get-new-comment")

    return fetch(url)
        .then((response) => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error("API error")
            }
        })
        .then((responseJson) => {
            currentQuestionId = responseJson.id
            document.getElementById("question-wrapper").innerHTML = responseJson.content
        })
        .catch((error) => {

            // Mock data, to be removed once it's connected to prod
            responseJson = { "id": 124, "content": "She is as dirty as they come  and that crook Rengel  the Dems are so fucking corrupt it's a joke." }
            currentQuestionId = responseJson.id
            document.getElementById("question-wrapper").innerHTML = responseJson.content

            throw new Error("API error")
        })

}

function sendAnswer(questionId, answer) {

    const url = new URL(host + "/verify-answer")
    let params = {
        questionId: questionId,
        answer: answer
    }
    url.search = new URLSearchParams(params).toString()

    return fetch(url)
        .then((response) => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error("API error")
            }
        })
        .then((responseJson) => {
            console.log(responseJson)
            score = score - responseJson.answer
            document.getElementById("score").innerHTML = score
        })
        .catch((error) => {

            // Mock data, to be removed once it's connected to prod
            responseJson = { "id": 124, "answer": 1 }
            score = score - responseJson.answer
            document.getElementById("score").innerHTML = score

            throw new Error("API error")
        })

}
