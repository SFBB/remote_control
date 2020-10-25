// // sleep 6;
// // alert("Hello!");
// function do_next_video(){
// 	a = document.getElementsByClassName("MacPlayer")[0];
// 	b = a.getElementsByTagName("table")[0];
// 	c = b.getElementsByTagName("iframe")[0];
// 	src = c.src;
// 	chrome.storage.sync.set({"src": src}, function() {
//           console.log('src is set to ' + src);
//         });
// 	// video = document.getElementById("video");
// 	// video = video.getElementsByClassName("dplayer-video-wrap")[0]
// 	// video.click();
// 	list = document.getElementsByClassName("d-play-list num-tab")[0];
// 	current = list.getElementsByClassName("current")[0];
// 	list = current.parentElement;
// 	var index = 0;
// 	for(var child of list.children){
// 		console.log(child.className);
// 		if(child.className == "current"){
// 			index = index + 1;
// 			break;
// 		}
// 		index = index + 1;
// 	}
// 	// console.log(list.children[index].href);
// 	try{
// 		url = list.children[index].href
// 	}
// 	catch(err){
// 		url = "https://www.17drama.net/"
// 	}
// 	chrome.storage.sync.set({"next_url": url}, function() {
//           console.log('next_url is set to ' + url);
//         });
// 	// function next_video(e) {
// 	// 	alert("Hello!");
// 	// 	console.log(list);
// 	// 	window.location.replace(list.children[index].href);
// 	// }
// 	// video.addEventListener('ended',next_video,false);
// }

// do_next_video();