// <!-- Update temp on page load-->
    $(function() {
     $('a#CurrentTemp').ready(function() {
      $.getJSON('/tempbackground_proc',
        function(data) {
            $("#CurrentTemp").text(data.result);
        });
        return false;
    });
});

// <!-- Update temp on refresh button-->
    $(function() {
     $('a#tempUpdate').bind('click',function() {
      $.getJSON('/tempbackground_proc',
        function(data) {
            $("#CurrentTemp").text(data.result);
        });
        return false;
    });
});

// <!-- Update blind on page load/refresh button-->
    $(function() {
     $('a#CurrentBlind').ready(function() {
      $.getJSON('/blindbackground_proc',
        function(data) {
            $("#CurrentBlind").text(data.result);
        });
        return false;
    });
});
    $(function() {
     $('a#blindUpdate').bind('click', function() {
      $.getJSON('/blindbackground_proc',
        function(data) {
            $("#CurrentBlind").text(data.result);
        });
        return false;
    });
});

// <!-- Update bulb on page load/refresh button-->
    $(function() {
     $('a#CurrentLight').ready(function() {
      $.getJSON('/bulbbackground_proc',
        function(data) {
            $("#CurrentLight").text(data.result);
        });
        return false;
    });
});
    $(function() {
     $('a#lightUpdate').bind('click', function() {
      $.getJSON('/bulbbackground_proc',
        function(data) {
            $("#CurrentLight").text(data.result);
        });
        return false;
    });
});

// <!--- Simple Function for Slider Display --->
function outputUpdate(vol) {
    if(vol == '0'){
        document.querySelector('#blindSliderLabel').value = 'Fully Open';
    } else if (vol == '10'){
        document.querySelector('#blindSliderLabel').value = 'Fully Closed';
    } else {
        document.querySelector('#blindSliderLabel').value = vol + '0% Closed';
    }
}


//Function for bulb control with buttons
$(function() {
$('.ButtonTest').on('click', function() {
$.getJSON('/bulbsetbackground_proc', {
    colourVal: $(this).attr('value'),
    onoffVal: ('on')
  },
  function(data) {
      $("#result2").text(data.result);
  });
  return false;
});
});

//Function for bulb control off button
$(function() {
$('#Coff').on('click', function() {
$.getJSON('/bulbsetbackground_proc', {
    colourVal: $('button[name="changeColour"]').val(),
    onoffVal: $('button[name="onoffValue"]').val()
  },
  function(data) {
      $("#result2").text(data.result);
  });
  return false;
});
});

//Function for blind control slider
$(function() {
$('a#blindSlider').on('click', function() {
$.getJSON('/blindsetbackground_proc', {
    blindVal: $('input[name="blindValue"]').val(),
  },
  function(data) {
      $("#result2").text(data.result);
  });
  return false;
});
});

//Function for picture control
$(function() {
$('#pSend').on('click', function() {
$.getJSON('/picturebackground_proc', {
    picVal: $('input[id="picture"]').val(),
  },
  function(data) {
      $("#result2").text(data.result);
  });
  return false;
});
});

//Function for video control
$(function() {
$('#vSend').on('click', function() {
$.getJSON('/videobackground_proc', {
    vidVal: $('input[id="video"]').val(),
  },
  function(data) {
      $("#result2").text(data.result);
  });
  return false;
});
});

// <!-- Update camera pic on page load-->
    $(function() {
     $('a#LastCamera').ready(function() {
      $.getJSON('/lastpicbackground_proc',
        function(data) {
            $("#LastCamera").text(data.result);
        });
        return false;
    });
});
