//GoodNight Activate
$(function() {
$('#goodNight').on('click', function() {
$.getJSON('/bulbsetbackground_proc', {
    onoffVal: ('Off')
  },
  function(data) {
      $("#result2").text(data.result);
  });
$.getJSON('/blindsetbackground_proc', {
      blindVal: ('10')
   },
   function(data) {
        $("#result2").text(data.result);
});
  return false;
});
});

//GoodMorning Activate
$(function() {
$('#goodMorning').on('click', function() {
$.getJSON('/bulbsetbackground_proc', {
    colourVal: ('White'),
    onoffVal: ('On')
  },
  function(data) {
      $("#result2").text(data.result);
  });
$.getJSON('/blindsetbackground_proc', {
      blindVal: ('0'),
   },
   function(data) {
        $("#result2").text(data.result);
});
  return false;
});
});

//Party Mode Activate
function PartyModeAct(){
    //Cycle Colours
    $.getJSON('/bulbsetbackground_proc', {
        colourVal: ('Rainbow'),
        onoffVal: ('On')
      },
      function(data) {
          $("#result2").text(data.result);
      });    
    $.getJSON('/picturebackground_proc', {
        picVal: (1),
     },
     function(data) {
        $("#result2").text(data.result);
     });

}
