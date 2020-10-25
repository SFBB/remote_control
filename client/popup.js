// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

console.log("aaa");
  chrome.storage.sync.get(["url"], function(result){
    $.ajax({
      type: "POST",
      url: result.url+"video_list",
      data: JSON.stringify({type: 'current_list'}),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(response){
        console.log(response);
        var videos = response.videos;
        for(var video of videos){
          $("#tbody").append("<tr><th scope='row'>"+video.name+"</th><td>"+video.duration+"</td><td>"+video.status+"</td><td><a href='"+video.url+"'>"+video.url+"</a></td></tr>");
        }
      }
    });
  });

function start(){
  // alert("bbb!");
  // chrome.tabs.captureVisibleTab({format: "png"}, function(dataUrl){
  //   var img = document.createElement("img");
  //   img.src = dataUrl;
  //   $("#aaa")[0].appendChild(img);
  //   console.log(img);
  //   chrome.storage.sync.get(["url"], function(result){
  //     $.ajax({
  //       type: "POST",
  //       url: result.url+"upload_screenshot",
  //       data: JSON.stringify({data: dataUrl.substr(22)}),
  //       contentType: "application/json; charset=utf-8",
  //       dataType: "json",
  //       success: function(response){
  //         console.log(response);
  //         // var videos = response.videos;
  //         // for(var video of videos){
  //         //   $("#tbody").append("<tr><th scope='row'>"+video.name+"</th><td>"+video.duration+"</td><td>"+video.status+"</td><td><a href='"+video.url+"'>"+video.url+"</a></td></tr>");
  //         // }
  //       }
  //     });
  //   });
  // });
  chrome.extension.sendMessage({"screenshot": false, "started": true, "ended": false});
}

$("#start")[0].addEventListener("click", start);