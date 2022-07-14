function delete_comment() {
    return confirm('Do you want to delete the comment?');
}

function toggleCommentsQuestion() {
  let x = document.getElementById("comments_question");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function toggleCommentsAnswer() {
  let x = document.getElementById("comments_answer");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function toggleProfileQuestion() {
  let x = document.getElementById("hide_profile_questions");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function toggleProfileAnswer() {
  let x = document.getElementById("hide_profile_answers");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function toggleProfileQuestionComments() {
  let x = document.getElementById("hide_profile_question_comments");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function toggleProfileAnswerComments() {
  let x = document.getElementById("hide_profile_answer_comments");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}