let count = 0;
let isRunning = true;

function startTime(){
    let clock =document.getElementById("timer-display");
    if (isRunning)
        setInterval( function () {

            count++;

            document.getElementById("timer-display").innerText = count
        },1000);

}
