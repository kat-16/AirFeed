$(document).ready(function() {
    $('input[type=text],input[type=number],textarea').addClass('form-control');
    $('input[type=checkbox]').css('opacity','1');





    var i = 0;
    $("#id_question_type").change(function () {

        removeAllNodes();

        var question_type = $("#id_question_type option:selected").html();

        if(question_type=="Single Choice" || question_type=="Multiple Choice"){

            var btn  = document.createElement("button");

            var t = document.createTextNode("Add Choice");

            btn.setAttribute("type", "button");
            btn.setAttribute("class", "btn btn-info");

            btn.appendChild(t);


            btn.onclick = function(){

                addInputField();

            }

            document.getElementById("choice_div").appendChild(btn);
            document.getElementById("choice_div").appendChild(document.createElement("br"));
            document.getElementById("choice_div").appendChild(document.createElement("br"));

            addInputField();

        }else{
        }


        function addInputField(){

            i++;

            var input_a  = document.createElement("input");

            input_a.placeholder =  "Enter Choice";

            input_a.setAttribute("class", "form-control form-control-line choice");
            input_a.setAttribute("required", "");
            input_a.setAttribute("name", "choice_"+i);
            input_a.style.width = '80%';
            input_a.style.float = 'left';


            var btn  = document.createElement("button");

            var t = document.createTextNode("REMOVE");

            var br_a = document.createElement("br");
            var br_b = document.createElement("br");

            btn.onclick = function(){
                input_a.remove();
                btn.remove();
                br_a.remove();
                br_b.remove();
            }

            btn.setAttribute("type", "button");
            btn.setAttribute("class", "btn btn-danger");
            btn.style.width = '20%';

            btn.style.float = 'right';

            btn.appendChild(t);

            var div_main = document.createElement("div");

            div_main.appendChild(input_a);
            div_main.appendChild(btn);
            div_main.appendChild(br_a);
            div_main.appendChild(br_b);
            document.getElementById("choice_div").appendChild(div_main);
        }

        function removeAllNodes(){
            document.getElementById("choice_div").innerHTML = "";
        };

    });
});
