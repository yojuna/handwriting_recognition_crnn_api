      var canvas = document.getElementById('myCanvas');
      var ctx = canvas.getContext('2d');
      
      var predict_button = document.getElementById('pred_button').addEventListener('click', sendReq);
       
      var painting = document.getElementById('paint');
      var paint_style = getComputedStyle(painting);
      canvas.width = parseInt(paint_style.getPropertyValue('width'));
      canvas.height = parseInt(paint_style.getPropertyValue('height'));

      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      var mouse = {x: 0, y: 0};

      function sendReq(){
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:8888/predict', true);

        xhr.onload = function(){
          if(this.status == 200){
            document.getElementById('number').innerHTML = this.responseText;
            console.log('api response: ', this.responseText);
          }
          else{
            console.log(error.log)
          }
        };
        console.log('is here');
        xhr.setRequestHeader("Content-Type", "application/json");
        // xhr.send({data: canvas.toDataURL("image/png")});
        xhr.send({data: canvas.toDataURL("image/png")});
      };

      // function sendReq(){
      //   fetch("http://localhost:8888/predict", { 
              
      //       // Adding method type 
      //       method: "POST", 
              
      //       // Adding body or contents to send 
      //       body: JSON.stringify({data: canvas.toDataURL("image/png")}), 
              
      //       // Adding headers to the request 
      //       headers: { 
      //           "Content-type": "application/json; charset=UTF-8"
      //       } 
      //   }) 
      //   // Converting to JSON 
      //   .then(response => console.log(response.json()))
      //   .then(response => document.getElementById("#number").innerHTML = response.json())
      // };


      // function sendReq(){
      //   $.post("http://localhost:8888/predict", {data: canvas.toDataURL("image/png")}).done(function(data) {
      //     $("#number").html(data);
      //   });
      // };

      canvas.addEventListener('mousemove', function(e) {
        mouse.x = e.pageX - this.offsetLeft;
        mouse.y = e.pageY - this.offsetTop;
      }, false);

      ctx.lineWidth =5;
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';
      ctx.strokeStyle = '#000000';
       
      canvas.addEventListener('mousedown', function(e) {
          ctx.beginPath();
          ctx.moveTo(mouse.x, mouse.y);
       
          canvas.addEventListener('mousemove', onPaint, false);
      }, false);
       
      canvas.addEventListener('mouseup', function() {
          canvas.removeEventListener('mousemove', onPaint, false);
      }, false);
       
      var onPaint = function() {
          ctx.lineTo(mouse.x, mouse.y);
          ctx.stroke();
      };