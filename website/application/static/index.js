$(function() {
    $('#sendBtn').bind('click', function() {
        var text = document.getElementById("msg").value
        console.log(text)
        $.getJSON('/run', {txt: text},
            function(data) {
            });
        return false;
    });
});

function validate(name){
    if(name.length >= 2)
        return true;
    return false;
}