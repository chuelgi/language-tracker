

//template code
function toggleTheme(){
  document.documentElement.classList.toggle('dark');

  const btn = document.getElementById('themeBtn');
  const isDark = document.documentElement.classList.contains('dark');

  btn.innerText = isDark ? '☀️' : '🌙';
}

//timer

let count = 0;
let intervalID = null;

function startTime(){
    let clock =document.getElementById("time");

    if (!intervalID)
        intervalID =setInterval( function () {

            count++;

            document.getElementById("time").innerText = formatTime(count)

        },1000);

}

function pauseTime(){

    clearInterval(intervalID)
    intervalID = null
}

function stopTime(){
    clearInterval(intervalID)
    intervalID = null
    count = 0
    document.getElementById("time").innerText = "00:00:00"
}

async function StopAndSaveSession() {
    let topicID = document.getElementById("subject").value;
    let duration = count;

        //send to flask
    fetch("/save-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            topic_id: topicID,
            duration: duration
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Saved:", data);
    });

    //stop and reset timer
    clearInterval(intervalID)
    intervalID = null
    count = 0

    document.getElementById("time").innerText = "00:00:00"
}

function formatTime(totalSeconds){
    let hours = Math.floor(totalSeconds/3600);
    let mins = Math.floor((totalSeconds%3600)/ 60);
    let seconds = totalSeconds %60;

    return(
        String(hours).padStart(2,"0") + ":" +
        String(mins).padStart(2,"0") + ":" +
        String(seconds).padStart(2,"0")

    );
}