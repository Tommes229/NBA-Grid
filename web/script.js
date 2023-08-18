document.querySelector("button").onclick = function() {   
    eel.one_python()(function(number) {
        document.querySelector(".one_number").innerHTML = number;
    })
}