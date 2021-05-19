function drawPercent(){
    $(".prog-row .prog-obj div.prog").each(function(index) {
        let score = parseFloat($(this).text()) * 100.0
        $(this).html('<div class="percent"></div><div class="slice'+(score > 50?' gt50':'')+'"><div class="pie"></div>'+(score > 50?'<div class="pie fill"></div>':'')+'</div>');

        let deg = 360.0 / 100 * score;
        $(this).find('.slice .pie').css({
            '-moz-transform':'rotate('+deg+'deg)',
            '-webkit-transform':'rotate('+deg+'deg)',
            '-o-transform':'rotate('+deg+'deg)',
            'transform':'rotate('+deg+'deg)'
        });
        $(this).find('.percent').html('<p>' + score.toFixed(2) +'%</p>');
    });    
}

$(document).ready(function(){
    drawPercent()
});