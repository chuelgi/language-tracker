

//template code
function applyTheme() {
  const theme = localStorage.getItem("theme");

  const isDark =
    theme === "dark" ||
    (!theme && window.matchMedia("(prefers-color-scheme: dark)").matches);

  document.documentElement.classList.toggle("dark", isDark);

  const btn = document.getElementById("themeBtn");
  if (btn) btn.innerText = isDark ? "☀️" : "🌙";
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle("dark");

  localStorage.setItem("theme", isDark ? "dark" : "light");

  const btn = document.getElementById("themeBtn");
  if (btn) btn.innerText = isDark ? "☀️" : "🌙";
}

applyTheme();
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

function StopAndSaveSession() {
    let duration = count;

    // stop timer
    clearInterval(intervalID);
    intervalID = null;
    count = 0;

    document.getElementById("time").innerText = "00:00:00";

    // redirect to Flask form with data
    window.location.href =
        `/add-log?duration=${duration}`;
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