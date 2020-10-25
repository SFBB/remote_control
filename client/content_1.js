// sleep 6;
// alert("Hello!");
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function play_video(){
	console.log("asdasdasd");
	// await sleep(5000);
	console.log('ended is set to false');
	try{
		if(window.location.href.indexOf("https://www.398zy.com/") != -1){
			video = document.getElementsByTagName("video")[0]
		}
		else if(window.location.href.indexOf("https://youku.kuyun-leshi.com/") != -1 || window.location.href.indexOf("https://www.solezy.me/") != -1 || window.location.href.indexOf("https://youku.com-t-youku.com/") != -1){
			video = document.getElementsByTagName("video")[0]
		}
		else{
			video = document.getElementsByTagName("video")[0]
		}
		video.play()
		while(true){
			if(!video.paused)
				break;
			else
				video.click();
		}
	}
	catch(err){
		url = document.getElementsByTagName("iframe")[0].src
		window.location.replace(url)
	}
	// document.getElementsByClassName("dplayer-icon dplayer-full-icon")[0].click();
	function next_video(e) {
		// alert("Hello!");
		chrome.storage.sync.set({"ended": true}, function() {
	          console.log('ended is set to true');
	        });
		chrome.extension.sendMessage({"ended": true});
	}
	video.addEventListener('ended',next_video,false);
	console.log("go!");
}

function do_next_video(){
	chrome.storage.sync.set({"ended": false}, function() {
		play_video();
    });
}

do_next_video();
