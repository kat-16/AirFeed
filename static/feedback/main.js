String.prototype.format = function () {
        var args = [].slice.call(arguments);
        return this.replace(/(\{\d+\})/g, function (a){
            return args[+(a.substr(1,a.length-2))||0];
        });
};

$(document).ready(function() {
  var active_question;
  var data;
  var questionTitle = '<div class="card-header"><h4 class="m-b-0 text-white">{0} </h4></div>';
  var choicesForm = '<div class="card-body"><form class="form p-t-20">{0}<div class="text-left"><button type="submit" id="skip_question" class="btn btn-inverse waves-effect waves-light">Skip</button><button type="submit" id="submit_question" class="btn btn-success waves-effect waves-light m-r-10">Submit</button></div></form></div>'
  var multiChoice = '<div class="form-group"><div class="checkbox checkbox-success"><input id="{0}" type="checkbox"><label for="{0}">{1}</label></div></div>'
  var singleChoice = '<div class="form-group"><label class="custom-control custom-radio"><input id="{0}" name="radio" class="custom-control-input" type="radio"><span class="custom-control-label">{1}</span></label></div>'
  // Correctly decide between ws:// and wss://
  roomId = $("#room_id").text().trim();
  var ws_scheme = window.location.protocol == "https:"
    ? "wss"
    : "ws";
  var ws_path = ws_scheme + '://' + window.location.host + "/feedback/stream/";
  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  // Helpful debugging
  socket.onopen = function() {
    console.log("Connected to chat socket");
    socket.send(JSON.stringify({"command": "join", "room": roomId}));
    $("#event-details").hide();


  };
  socket.onclose = function() {
    console.log("Disconnected from chat socket");
  };

  socket.onmessage = function(message) {
    // Decode the JSON
    console.log("Got websocket message " + message.data);
    data = JSON.parse(message.data);
    // Handle errors
    if (data.error) {
      alert(data.error);
      return;
    }
    // Handle joining
    if (data.join) {
      console.log("Joining room " + data.join);
        // socket.send(JSON.stringify({"command": "send", "room": data.join, "message": "test"}));
      // Handle leaving
    } else if (data.leave) {
      console.log("Leaving room " + data.leave);
    } else if (data.message || data.msg_type != 0) {
      console.log("Message", data.message)
      if (data.message == null || data.message.length == 0){
        $("#question").hide();
        $("#no-questions").show();

      }
      else{

        if (localStorage) {
          // LocalStorage is supported!

          console.log("localStorage available");
           active_question = updateQuestion();
           console.log(active_question)
          // localStorage.setItem("names", JSON.stringify(answeredQuestions));
        } else {
          alert("Please upgrade your browser.")
          // No support. Use a fallback such as browser cookies or store on the server.
        }

      }

    } else {
      console.log("Cannot handle message!");
    }
  };

 function updateQuestion(){
   var answeredQuestions = JSON.parse(localStorage.getItem("answeredQuestions"));
   console.log("updating", answeredQuestions)
   if (answeredQuestions == null){
     answeredQuestions = [];
   }

   filtered_questions = []
   for(var i=0; i<data.message.length; i++){
     for(var j=0; j<answeredQuestions.length; j++){
       if (data.message[i]["id"] == answeredQuestions[j]){
         break;

       }
       if (j == answeredQuestions.length - 1){
         filtered_questions.push(data.message[i])
       }
     }
   }

   if(answeredQuestions.length == 0){
     filtered_questions = data.message;
   }
   if (filtered_questions.length >0){


   console.log("filtered_questions", filtered_questions)
   console.log("answeredQuestions", answeredQuestions)
   console.log("data", data)

   var question;
   question = filtered_questions[Math.floor(Math.random()*filtered_questions.length)];

   // 2 for multiple choice and 1 for single choice
   choiceHtmlStr = ""
   if (question["question_type"] == 2){
     for(var i=0; i<question["choices"].length; i++){
       choiceHtmlStr += multiChoice.format(question["choices"][i]["id"], question["choices"][i]["choice_text"])
     }
   }
   if (question["question_type"] == 1){
     for(var i=0; i<question["choices"].length; i++){
       choiceHtmlStr += singleChoice.format(question["choices"][i]["id"], question["choices"][i]["choice_text"])
     }
   }
   var htmlStr = questionTitle.format([question["question_text"]]) + choicesForm.format([choiceHtmlStr])



   // console.log(htmlStr)
   $("#question").html(htmlStr)

   $("#submit_question").click(function(event){
    event.preventDefault();
    choice_list = []

   $('.form-group input[type=checkbox]:checked, .form-group input[name=radio]:checked').each(function(index){
    console.log($(this).attr('id'));
    choice_list.push($(this).attr('id'));
   })
   choice_list = JSON.stringify(choice_list);
   $.ajax({
    url: "/event/question/vote/",
    type: "POST",
    data:{ 'csrfmiddlewaretoken' : $("[name=csrf_token]").val() , 'choice_list':choice_list},
    error : function(json) {
     console.log("Error toggling question status.")
   },
    success : function(){
      submit_question(active_question);
    }
   });

   });

   $("#skip_question").click(function(){
     skip_question(active_question);
   });


   $("#no-questions").hide();
   $("#question").show();

   return question;

 }
 else{
   $("#no-questions").show();
   $("#question").hide();

   return null;
 }
 }

function submit_question(question){

    var answeredQuestions = JSON.parse(localStorage.getItem("answeredQuestions"));
    if (answeredQuestions == null){
      answeredQuestions = [];
    }
    console.log(answeredQuestions)
    answeredQuestions.push(question["id"]);
    console.log(JSON.stringify(answeredQuestions))
    localStorage.setItem("answeredQuestions", JSON.stringify(answeredQuestions));
    active_question = updateQuestion()
}

function skip_question(question){

  var answeredQuestions = JSON.parse(localStorage.getItem("answeredQuestions"));
  if (answeredQuestions == null){
    answeredQuestions = [];
  }

  if (question["is_mandatory"] != true){
    answeredQuestions.push(question["id"])
  }

  localStorage.setItem("answeredQuestions", JSON.stringify(answeredQuestions));
  console.log("question skipped");
  active_question = updateQuestion();

}




});
