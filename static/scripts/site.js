$(".copyable").click(function(evt) {
    var text = this.innerText;
    var copyInput = $("<input id='copyInput' type='text' value='" + text + "'/>");
    $("body").append(copyInput);
    copyInput.select();
    document.execCommand("copy");
    copyInput.remove();
});
