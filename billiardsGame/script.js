const cueBall = document.getElementById('cue-ball');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isDragging = false;

cueBall.addEventListener( 'mousedown', startDragging);
document.addEventListener( 'mousemove', dragCueBall);
document.addEventListener('mouseup', releaseCueBall);

let cueBallStartX, cueBallStartY;
let mouseX, mouseY;
let lineStartX, lineStartY;

function startDragging(e) {
    isDragging = true;
    cueBallStartX = e.clientX;
    cueBallStartY = e.clientY;
}

function dragCueBall(e) {
    if (isDragging){
        isDragging = false;

        //velocity components calculations
        const velX = (mouseX - cueBallStartX) * 0.1;
        const velY = (mouseY - cueBallStartY) * 0.1;

        removeLine();
    }
}

function drawLine(){
    // draw line fromm cue ball to mouse position
    lineStartX = cueBallStartX;
    lineStartY = cueBallStartY;

    //clear the canvas
    ctx.clearRect(0, 0, canvas.clientWidth, canvas.height);

    // draw line from cue ball to mouse position
    ctx.beginPath();
    ctx.moveTo(cueBallStartX, cueBallStartY);
    ctx.lineTo(mouseX, mouseY);
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'black';
    ctx.stroke();
}

function removeLine(){
    //remove drawn line
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}