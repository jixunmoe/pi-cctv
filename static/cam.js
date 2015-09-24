$(function () {
  var $container = $('#cam-container');
  var canvas = document.getElementById('canvas');
  var ctx = canvas.getContext('2d');
  
  var $img = new Image();
  var $cam = $($img);
  var $window = $(window);
  
  function loadImage(){
    $img.src = '/capture?_=' + Math.random()
  }
  
  var loadFailed = true;
  function drawFrame(){
    ctx.drawImage($img, 0, 0, canvas.width, canvas.height);
    
    if (loadFailed) {
      drawErrorMessage();
    }
  }
  function drawErrorMessage() {
    ctx.fillStyle = 'rgba(0,0,0,0.3)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = 'rgb(255,255,255)';
    var w = 300;
    var h = 80;
    
    // Draw this box in the center.
    ctx.fillRect((canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
    ctx.textAlign = 'center';
    ctx.fillStyle = '#555';
    
    var t = (canvas.height - h) / 2;
    ctx.textBaseline = 'top';
    ctx.font = '30pt Calibri';
    ctx.fillText('Network Error', canvas.width / 2, t);
    ctx.font = '12pt Calibri';
    ctx.fillText('Click here to reload.', canvas.width / 2, t + 50);
  }
  
  $img.onload = function () {
    loadFailed = false;
    drawFrame();
    requestAnimationFrame(loadImage);
  };
  
  $img.onerror = function () {
    loadFailed = true;
    drawErrorMessage();
  };
  loadImage();
  
  $window.resize(function () {
    var w = canvas.width = $container.width();
    canvas.height = w / 720 * 576;
    drawFrame();
  });
  
  // Resize twice :3
  $window.resize();
  setTimeout(function () {
    $window.resize();
  }, 50);
  
  window.fff = function () {
    $img.onload = null;
    $img.onerror();
  };
  
  canvas.onclick = function () {
    if (loadFailed)
      loadImage();
  };
});
