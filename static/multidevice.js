//GoodNight Activate
$(function() {
$('#goodNight').on('click', function() {
$.getJSON('/bulbsetbackground_proc', {
    onoffVal: ('off')
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
    colourVal: ('white'),
    onoffVal: ('on')
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


var colours = ["red", "green", "blue", "magenta", "yellow", "cyan", "white"];
function setNightmare(){
    var x = Math.floor((Math.random()*7) + 0);
    var y = Math.floor((Math.random()*11) + 0);
    var z = Math.floor((Math.random()*3) + 1);
        //Sets Bulb random colour
        $.getJSON('/bulbsetbackground_proc', {
            colourVal: (colours[x]),
            onoffVal: ('on')
          },
          function(data) {
              $("#result2").text(data.result);
          });
          //Sets Blind random height (0-10)
        $.getJSON('/blindsetbackground_proc', {
            blindVal: (y),
         },
         function(data) {
              $("#result2").text(data.result);
          });
          //Takes 1-3 pictures with camera
        $.getJSON('/picturebackground_proc', {
            picVal: (z),
         },
         function(data) {
            $("#result2").text(data.result);
         });
}
//Party Mode Activate
function PartyModeAct(){
    for (var i = 0; i < 1; i++) {

        setInterval(setNightmare, 5000);

    }

}
