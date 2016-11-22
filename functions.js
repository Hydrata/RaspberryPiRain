/*
 Supporting functions to simulate rainfall and rain gauge tipping.
 */

/* global variables and initalizations */
var MAX_DROPS = 50,
    DROP_TIMEOUT = 2000,
    TIPPING_SPEEDINDEX = 50,
    bucket_tips = 0,
    tipped_left = 1,
    rainInterval = 0,
    gaugeInterval = 0,
    drops = [];

/* update status upon rainfall range changes */
function changeRainfallAmount(value) {
  MAX_DROPS = value;
  $('#rainfall').val(value);

  drops.length = 0;
  $('.drop').remove();
  
  clearInterval(rainInterval);
  rainInterval = setInterval(function() {
     updateRain();
  }, DROP_TIMEOUT/MAX_DROPS);

  clearInterval(gaugeInterval);
  gaugeInterval = setInterval(function() {
     updateGauge();
  }, (DROP_TIMEOUT*TIPPING_SPEEDINDEX)/MAX_DROPS);
}

/* helper function for random coordinates for rain drops */
function getRandomValueFromRange(minNum, maxNum) {
  return (Math.floor(Math.random() * (maxNum - minNum + 1)) + minNum);
}

/* create new drop */
function createDrop() {
  var top = getRandomValueFromRange(95, 110);
  var left = getRandomValueFromRange(40, 200);
  var created = +new Date()/1000;
  drops.push(created);

  /* add rain drop */
  $('.rain').append('<div class="drop"></div>');
  $('.drop:last()').css('left', left);
  $('.drop:last()').css('top', top);
}

/* create and/or remove rain drops as time elapses
   and as per set rainfall amount */
function updateRain() {
  /* don't create drops if max reached */
  if (drops.length < MAX_DROPS) {
    createDrop();
  }
  
  /* check the timeout on each drop and remove stale drops */
  var diff = +new Date()/1000 - drops[0];
  if (diff >= DROP_TIMEOUT/1000) {
    $('.drop:first()').remove();
    drops.shift();
  }
}

/* tip the gauge bucket as rain accumulates */
function updateGauge() {
  /* tip the bucket on each update */
  bucket_tips++;
  if (tipped_left) {
    $('.tipping_bucket').css('transform', 'rotate(14deg)');
    $('.tipping_bucket_bottom').css('transform', 'rotate(14deg)');
    tipped_left = 0;
  } else {
    $('.tipping_bucket').css('transform', 'rotate(-14deg)');
    $('.tipping_bucket_bottom').css('transform', 'rotate(-14deg)');
    tipped_left = 1;
  }
}

/* create new drops and remove stale ones in a regular interval
   update the gauge status */
$(document).ready(function(){
  rainInterval = setInterval(function() {
     updateRain();
  }, DROP_TIMEOUT/MAX_DROPS);

  gaugeInterval = setInterval(function() {
     updateGauge();
  }, (DROP_TIMEOUT*TIPPING_SPEEDINDEX)/MAX_DROPS);
});
