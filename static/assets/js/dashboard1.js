
$(document).ready(function() {

var active_question = 1;
var visualisation_data;

$(".visualise-question").on('click',function(){
    var id = $(this).attr('value');
    active_question = id;
    var option = buildVisualisationData(visualisation_data, active_question);
    BuildChart(option);

});

//function to add new question to the database
function addQuestion() {


  choice_list = []
    choice_node_list = (document.querySelectorAll(".choice"))
    choice_node_list.forEach(function(e){
      console.log(e.value);
      choice_list.push(e.value);
    })

    choice_list = JSON.stringify(choice_list);
    console.log(choice_list);
    let checkVal;


    if($("#id_is_active").is(':checked')){
         checkVal = "True";
    }
    else{
         checkVal = "False";
    }
    if($("#id_is_mandatory").is(':checked')){
         mandatoryVal = "True";
    }
    else{
         mandatoryVal = "False";
    }
    $.ajax({
      url:"addquestion/",
      type:"POST",
      data:{
        'csrfmiddlewaretoken':$("[name=csrfmiddlewaretoken]").val(),
        'question_name': $("[name=question_text]").val(),
        'is_active': checkVal,
        'is_mandatory': mandatoryVal,
        'question_type': $("[name=question_type]").val(),
        'choice_list':choice_list,
      }
    }).done(function(){
    location.reload(true);
  })



};

 $('#addquestion').click(function(e){
       e.preventDefault();
       console.log("call add question")
       addQuestion();
   });

function toggleQuestion(id){
  $.ajax({
   url: "/event/toggleactive/" +id + "/",
   type: "POST",
   data:{ question_id : id ,
   'csrfmiddlewaretoken' : $("[name=csrfmiddlewaretoken]").val()} ,
   error : function(json) {
     console.log("Error toggling question status.")
  }

})
}
$(".switch input[type='checkbox']").change(function(){
        id = $(this).attr('id')
       toggleQuestion(id)

});

function getVisualisationData() {
    $.ajax({
        url: 'questions',
        success: function(data) {
        visualisation_data = data;
        var option = buildVisualisationData(visualisation_data, active_question);
        BuildChart(option);
        }
      });
    setTimeout(getVisualisationData, 250); // you could choose not to continue on failure...
}

getVisualisationData();


var pieChart = echarts.init(document.getElementById('chart'));

function buildVisualisationData(data, question_id){

  var temp_data = []
  console.log(data)
  for (var i=0; i<data[question_id]["choices"].length; i++){
    temp_data.push({value:data[question_id]["choices"][i]["vote_count"], name: data[question_id]["choices"][i]["choice_text"]})
  }

  var option = {

      tooltip : {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
      },
      toolbox: {
          show : true,
          feature : {

              dataView : {show: true, readOnly: false},
              magicType : {
                  show: true,
                  type: ['pie', 'funnel']
              },
              restore : {show: true},
              saveAsImage : {show: true}
          }
      },
      color: ["#f62d51", "#dddddd","#ffbc34", "#7460ee","#009efb", "#2f3d4a","#90a4ae", "#55ce63"],
      calculable : true,
      series : [
          {
              type:'pie',
              radius : [20, 110],
              center : ['50%', "50%"],
              roseType : 'radius',
              width: '40%',       // for funnel
              max: 40,            // for funnel
              itemStyle : {
                  normal : {
                      label : {
                          show : true
                      },
                      labelLine : {
                          show : true
                      }
                  },
                  emphasis : {
                      label : {
                          show : true
                      },
                      labelLine : {
                          show : true
                      }
                  }
              },


              data:temp_data
          },
      ]
  };
  return option
}



function BuildChart(option){
// use configuration item and data specified to show chart
pieChart.setOption(option, true), $(function() {
  function resize() {
    setTimeout(function() {
      pieChart.resize()
    }, 1000000)
  }
  $(window).on("resize", resize), $(".sidebartoggler").on("click", resize)
});
}



});
