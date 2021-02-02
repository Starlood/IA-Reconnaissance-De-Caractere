   window.onload = function() {
      var textes = ["IA","Images","Reconnaissance","Cyril","Théo"];
      var mouse = {
        x: -100,
        y: -100
      }
      var canvas = document.createElement("canvas");
      var ctx = canvas.getContext("2d");
      var retina = window.devicePixelRatio > 1 ? true : false;

      function setConvasSize() {
        if (retina) {
          canvas.width = window.innerWidth * 2;
          canvas.height = window.innerHeight * 2;
        } else {
          canvas.width = window.innerWidth;
          canvas.height = window.innerHeight;
        }
        canvas.style.width = window.innerWidth+"px";
        canvas.style.height = window.innerHeight+"px";
      }
      setConvasSize()
      window.onresize = setConvasSize;

      document.body.appendChild(canvas);
      ctx.fillStyle = "#2A2025";
      ctx.fillRect(0,0,canvas.width, canvas.height);
      var particles = [];
      var patriclesNum = 500;
      var rad = 2;
      if (retina) {
        patriclesNum *= 2;
        rad++;
      }
      for(var i = 0; i<patriclesNum; i++)
        particles.push(new multi_part());
      function multi_part(){
        this.x = Math.random()*canvas.width;
        this.y = Math.random()*canvas.height;
        this.vx = Math.random()*0.88-0.44;
        this.vy = Math.random()*0.88-0.44;
        this.rad = Math.floor(Math.random()*200)/100+1;
      }
      function move_part(){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for(var i = 0;i < patriclesNum; i++){
          var temp = particles[i];
          var distParticule = findDistance(temp, mouse);
          if (textes[i]) {
            ctx.font = retina ? "200 22px sans-serif" : "100 11px sans-serif";
            ctx.textAlign = "right";
            ctx.globalAlpha = 0.5;
            ctx.fillStyle = '#FFF';
            ctx.fillText(textes[i], temp.x-10, temp.y);
          };


           var distretina = retina ? 150 : 100;
          if(distParticule<distretina){
            createLine(temp, mouse, distParticule);
          }
          for(var j = 0; j<patriclesNum; j++){
            var temp2 = (temp != particles[j]) ? particles[j] : false;
            ctx.linewidth = 1;
            if (temp2) {
              var distParticule = findDistance(temp, temp2);
              if(distParticule<distretina){
                createLine(temp, temp2, distParticule);
              }
            };
          }
          ctx.fillStyle = '#9C957C';
          ctx.beginPath();
          ctx.globalAlpha = 1;
          ctx.arc(temp.x, temp.y, temp.rad, 0, Math.PI*2, true);
          ctx.fill();
          ctx.closePath();
          temp.x += temp.vx;
          temp.y += temp.vy;
          if(temp.x > canvas.width) temp.x = 0;
          if(temp.x < 0) temp.x = canvas.width;
          if(temp.y > canvas.height) temp.y = 0;
          if(temp.y < 0) temp.y = canvas.height;
        }
      }
      function createLine(p1, p2, d) {
        ctx.strokeStyle = '#4f5b60';
        ctx.globalAlpha = 50/d-0.3;
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
      }
      function findDistance(p1,p2){
        return Math.sqrt( Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2) );;
      }
      if (window.Event)
        document.captureEvents(Event.MOUSEMOVE);
      document.onmousemove = mouseMoveCanvas;
      function mouseMoveCanvas(e) {
        mouseX = (window.Event) ? e.pageX : event.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft);
        mouseY = (window.Event) ? e.pageY : event.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop);
        mouse = {
          x: mouseX,
          y: mouseY
        }
      }
      setInterval(move_part, 33);
    };