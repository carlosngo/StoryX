
function assignScores(){

    // arrDC is only a placeholder. replace with actual values
    arrDC = [20.50, 40.5, 80.69];

    // check the prog-row divs to see what's the element class assigned (e.g. dialogue-content)
    // dialogue-content
    assignElemScores('dialogue-content', arrDC[0], arrDC[1], arrDC[2])
    
    // dialogue speaker
    assignElemScores('dialogue-speakers', arrDC[0], arrDC[1], arrDC[2])
    
    //characters
    assignElemScores('characters', arrDC[0], arrDC[1], arrDC[2])
    
    // props
    assignElemScores('props', arrDC[0], arrDC[1], arrDC[2])
    
    // action-lines
    assignElemScores('action-lines', arrDC[0], arrDC[1], arrDC[2])
    
    // scene-transitions
    assignElemScores('scene-transitions', arrDC[0], arrDC[1], arrDC[2])
}

function assignElemScores(element, precision, recall, f1) {
    drawPercent(element, 'precision', precision);
    drawPercent(element, 'recall', recall);
    drawPercent(element, 'f1score', f1);
}

function drawPercent(row, scoretype, percent){
    cssPattern = "." + row + " ." + scoretype + " "
    $(cssPattern + "div.prog").html('<div class="percent"></div><div id="slice"'+(percent > 50?' class="gt50"':'')+'><div class="pie"></div>'+(percent > 50?'<div class="pie fill"></div>':'')+'</div>');
    var deg = 360/100*percent;
    $(cssPattern + '#slice .pie').css({
        '-moz-transform':'rotate('+deg+'deg)',
        '-webkit-transform':'rotate('+deg+'deg)',
        '-o-transform':'rotate('+deg+'deg)',
        'transform':'rotate('+deg+'deg)'
    });
    $(cssPattern + '.percent').html('<p>' + percent.toFixed(2) +'%</p>');
}

$(document).ready(function(){
    assignScores();
});