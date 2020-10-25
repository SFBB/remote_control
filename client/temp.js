// alert("aaa!");
try{
    var video = document.getElementsByTagName("video")[0];
    video.play();
}
catch{
    chrome.extension.sendMessage({"screenshot": false, "started": false, "ended": true});
}
function update_progress(){
    chrome.storage.sync.get(["url"], function(result){
        $.ajax({
            type: "POST",
            url: result.url+"update_current",
            data: JSON.stringify({current_time: parseInt(video.currentTime)}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
            console.log(response);
            if(video.ended) chrome.extension.sendMessage({"started": false, "ended": true});
                setTimeout(update_progress, 1000);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                setTimeout(update_progress, 1000);
            }
        });
    });
}
setTimeout(update_progress, 1000);
function exec_commands(){
    // console.log("1111111");
    var video = document.getElementsByTagName("video")[0];
    chrome.storage.sync.get(["url"], function(result){
        $.ajax({
          type: "POST",
          url: result.url+"get_commands",
          data: JSON.stringify({data: ""}),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function(response){
            response = JSON.parse(response)
            console.log(response);
            // alert("sadasd");
            if(response.stop) {console.log(video); video.pause();}
            else if(response.play) {video.play();}
            else if(response.screenshot){
                chrome.extension.sendMessage({"screenshot": true, "started": false, "ended": false});
            }
            // var videos = response.videos;
            // for(var video of videos){
            //   $("#tbody").append("<tr><th scope='row'>"+video.name+"</th><td>"+video.duration+"</td><td>"+video.status+"</td><td><a href='"+video.url+"'>"+video.url+"</a></td></tr>");
            // }
            setTimeout(exec_commands, 1000);
          },
          error: function (jqXHR, textStatus, errorThrown) {
            setTimeout(exec_commands, 1000);
          }
        });
      });
}
setTimeout(exec_commands, 1000);
// chrome.extension.sendMessage({"started": false, "ended": true});