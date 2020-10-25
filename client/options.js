// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

function get_setup(){
      chrome.storage.sync.get(["url"], function(result){
        if(result.url == undefined) result.url = "";
        console.log(result.url);
        document.getElementById("url").setAttribute("value", result.url);
      });
    }
get_setup();

function save_setup(){
  chrome.storage.sync.set({"url": document.getElementById("url").value}, function(){
    alert("Setup Saved!");
  });
}
document.getElementById("button_1").addEventListener('click',
    save_setup);