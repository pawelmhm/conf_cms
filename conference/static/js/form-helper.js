window.onload = function () {
    var form = document.getElementById('abstract-form');
    form.addEventListener('submit',sendData);

    function sendData(e) {
        e.preventDefault();
        /*var req = new XMLHttpRequest();
        req.onload = function (e) {
            if (req.status == 201) {
                removeForm()
            } else { */
        
        form.removeEventListener('submit',sendData);
        var ev = new Event('submit');
        form.dispatchEvent(ev);
           /* }
        };
        req.onerror = function (e) {
            console.log(e)
        };
        req.onprogress = function (e) {
        //    console.log(e);
        }
        req.open("POST",window.location.origin + "/admin/abstracts/");
        req.send(new FormData(form));
    }

    function removeForm() {
        form.remove();
        var box = document.getElementById('form-box');
        var h3 = document.createElement('h3');
        h3.textContent = "Thanks Submission. We will notify you about the results until ...";
        box.appendChild(h3);
        window.location = window.location.origin;
    }

    function displayErrors(errorMessage){
        var errs = JSON.parse(errorMessage);
        console.log(errs);
        var inputs = form.elements;
        for (var i =0;i<inputs.length;i++) {
            console.log(inputs[i].name);
            if (errs[inputs[i].name] != undefined) {
                var elem = document.getElementById(inputs[i].id);
                
                if (document.getElementById('message-'+elem.id) == null) {
                    var span = document.createElement('span');
                    span.class = "message";
                    span.id = 'message-' + elem.id;
                    span.textContent = errs[inputs[i].name];
                    elem.parentNode.insertBefore(span,elem.nextSibling);
                }
            }
        } */
    } 
};
