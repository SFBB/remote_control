// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.set({color: '#3aa757'}, function() {
    console.log("The color is green.");
  });
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
        pageUrl: {hostEquals: 'www.17drama.net'},
      })
      ],
          actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });
});

chrome.webNavigation.onCompleted.addListener(function(details){
  console.log(details.url);
  // console.log("asdafsafasfafasf");
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
      
        if(details.url.indexOf("https://cn.92drama.com/vod/play/") != -1){
          // chrome.storage.sync.get(['src'], function(result) {
          //         console.log('src currently is ' + result.src);
          //         chrome.tabs.create({url: result.src}, function(tab){
          //           chrome.tabs.remove(details.tabId);
          //           return;
          //         });
          //       });
          chrome.tabs.executeScript({file: 'temp.js'});
        }
        return;
      }
    });
  });
});

chrome.extension.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.started){
    // alert("asdasdad!");
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
        $.ajax({
          type: "POST",
          url: result.url+"video_list",
          data: JSON.stringify({type: 'current_list'}),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function(response){
            console.log(response);
            var videos = response.videos;
            $.ajax({
              type: "POST",
              url: result.url+"current_get",
              data: JSON.stringify({type: 'normal'}),
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              success: function(response){
                console.log(response);
                var index = response.index;
                chrome.tabs.create({url: videos[index].url}, function(tab){
                  console.log(tab);
                  chrome.tabs.executeScript(tab.id, {file: 'jquery.js'});
                  chrome.tabs.executeScript(tab.id, {file: 'temp.js'});
                });
              }
            });
            return;
            }
        });
        // chrome.tabs.create({url: response.videos[0].url}, function(tab){
        //   console.log(tab);
        //   chrome.tabs.executeScript(tab.id, {file: 'temp.js'});
        // });
        // if(details.url.indexOf("https://cn.92drama.com/vod/play/") != -1){
        //   // chrome.storage.sync.get(['src'], function(result) {
        //   //         console.log('src currently is ' + result.src);
        //   //         chrome.tabs.create({url: result.src}, function(tab){
        //   //           chrome.tabs.remove(details.tabId);
        //   //           return;
        //   //         });
        //   //       });
        //   chrome.tabs.executeScript({file: 'temp.js'});
        // }
          return;
        }
    });
  });
  }
  else if(request.ended){
    chrome.tabs.remove(sender.tab.id);
  chrome.storage.sync.get(["url"], function(result){
    $.ajax({
      type: "POST",
      url: result.url+"finished",
      data: JSON.stringify({type: 'current_list'}),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(response){
        console.log(response);
        $.ajax({
          type: "POST",
          url: result.url+"video_list",
          data: JSON.stringify({type: 'current_list'}),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function(response){
            console.log(response);
            var videos = response.videos;
            $.ajax({
              type: "POST",
              url: result.url+"current_get",
              data: JSON.stringify({type: 'normal'}),
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              success: function(response){
                console.log(response);
                var index = response.index;
                chrome.tabs.create({url: videos[index].url}, function(tab){
                  console.log(tab);
                  chrome.tabs.executeScript(tab.id, {file: 'jquery.js'});
                  chrome.tabs.executeScript(tab.id, {file: 'temp.js'});
                });
              }
            });
            return;
            }
        });
        }
    });
  });
  }
  else if(request.screenshot){
    chrome.permissions.request({origins: ["<all_urls>"] }, function(granted) {
    chrome.tabs.captureVisibleTab(sender.tab.windowId, {format: "png"}, function(dataUrl){
      //   var img = document.createElement("img");
      console.log(dataUrl);
      // alert("asdadasdasdasdsadasdasd");
      chrome.storage.sync.get(["url"], function(result){
        $.ajax({
          type: "POST",
          url: result.url+"upload_screenshot",
          data: JSON.stringify({data: dataUrl.substr(22)}),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function(response){
              alert("asdasdasd");
              console.log(response);
              // setTimeout(exec_commands, 1000);
          // var videos = response.videos;
          // for(var video of videos){
          //   $("#tbody").append("<tr><th scope='row'>"+video.name+"</th><td>"+video.duration+"</td><td>"+video.status+"</td><td><a href='"+video.url+"'>"+video.url+"</a></td></tr>");
          // }
          }
      });
    });
  });
});
return;
}
})