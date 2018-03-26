var color = ['black', 'green', 'brown', 'red', 'blue', 'yellow', 'pink'];

function selector_color(color, css_id) {

    var randcolor = color[Math.floor(Math.random() * color.length)];
    console.log('entro');
    $(css_id).css("background", randcolor);

    $.post("/save_session", {div: css_id, color_div: randcolor},
        function(data, status){
            console.log("Data: " + data + "\nStatus: " + status);
        });
}

$(document).ready(function(){
        $("#div1").click(function(){
            selector_color(color, '#div1');
        });
        $("#div2").click(function(){
            selector_color(color, '#div2');
        });
        $("#div3").click(function(){
            selector_color(color, '#div3');
        });
        $("#div4").click(function(){
            selector_color(color, '#div4');
        });
    });