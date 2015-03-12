<!DOCTYPE html>
<html>
<head lang="zh">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <link href="http://libs.useso.com/js/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.useso.com/js/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://libs.useso.com/js/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <title>加入</title>
    <script>
        status="idle";
        document.addEventListener('DOMContentLoaded',function(){
            window.join_btn=document.getElementById("join_btn");
            window.okay_btn=document.getElementById("okay_btn");
            window.plist=document.getElementById("plist");
            window.nickname=document.getElementById("nickname");
            setInterval(function(){
                var xhr=new XMLHttpRequest();
                xhr.open("post","/ping",false);
                xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded;");
                xhr.send(
                    "status="+status+"&"+
                    "name="+encodeURIComponent(nickname.value)
                );
                var pdata=JSON.parse(xhr.responseText);
                plist.innerHTML="";
                for(var pos=0;pos<pdata.length;pos++) {
                    var tmp=document.createElement("span");
                    tmp.className="label label-"+(pdata[pos]["okay"]?"success":"default");
                    tmp.innerText=pdata[pos]["name"];
                    plist.appendChild(tmp);
                }
            },1500)
        });
        function join() {
            if(status!="idle") {
                join_btn.innerText="加入";
                status="idle";
                okay_btn.setAttribute('disabled','disabled');
            }
            else {
                join_btn.innerText="取消加入";
                status="join";
                okay_btn.removeAttribute("disabled");
            }
        }
        function okay() {
            if(status!="okay") {
                okay_btn.innerText="取消准备";
                status="okay";
                join_btn.setAttribute('disabled','disabled');
            }
            else {
                okay_btn.innerText="准备";
                status="join";
                join_btn.removeAttribute("disabled");
            }
        }
    </script>
</head>
<body><div class="container">
    <div class="well well-sm">
        <input placeholder="昵称" class="form-control" style="width: 200px; display: inline !important;" id="nickname">
        <button type="button" class="btn btn-primary" id="join_btn" onclick="join()">加入</button>
        <button type="button" class="btn btn-success" id="okay_btn" onclick="okay()" disabled="disabled">准备</button>
    </div>
    <div class="well well-sm" id="plist"></div>
</div></body>
</html>