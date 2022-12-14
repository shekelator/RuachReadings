function enableCopyButton(button) {
    button.click(function() {
        let parent = button.parents(".copyable");
        var text = parent.text().trim();
        var copyInput = $("<input id='copyInput' type='text' value='" + text + "'/>");
        $("body").append(copyInput);
        copyInput.select();
        document.execCommand("copy");
        copyInput.remove();
        button.removeClass("bi-clipboard").addClass("bi-clipboard-check");
        setTimeout(function() {
            button.removeClass("bi-clipboard-check").addClass("bi-clipboard");
        }, 1000);
    });
}

function enableReadButton(button) {
    button.click(function() {
        let button = $(this);
        let parent = button.parents(".copyable");
        var text = parent.text().trim();
        let url = button.hasClass('besorah')
            ? `https://www.biblegateway.com/passage/?search=${text}&version=TLV`
            : `https://www.sefaria.org/${text}?lang=bi&aliyot=0`;
        window.open(url, "OpenSefariaWindow");
    });
}


$(".readings td").hover(function(evt) {
    let el = $(this);
    el.find(".action-buttons").show();
    enableCopyButton(el.find(".copy-button"));
    enableReadButton(el.find(".read-button"));
}, function(evt) {
    let el = $(this);
    el.find(".copy-button").off("click");
    el.find(".read-button").off("click");
    el.find(".action-buttons").hide();
});
