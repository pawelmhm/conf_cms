(function () {
    var buttonDelete = document.getElementById('deleteButton');
    buttonDelete.addEventListener('click',deletePost);
    '{{ csrf_token }}'
    var buttonLeave = document.getElementById('leave');
    buttonLeave.addEventListener('click', redirect);

    function redirect (e) {
    
    }

    function deletePost(e) {
        e.preventDefault();
        var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var req = new XMLHttpRequest();

        req.onload = function (e) {
            if (req.readyState ==4) {
                console.log(req.responseText)
                window.location.assign(window.location.origin+'/admin/posts/') 
            }
        }
        req.open('delete',window.location.href);
        req.setRequestHeader('X-CSRFToken',csrf);
        req.send(csrf);
    }
})();
