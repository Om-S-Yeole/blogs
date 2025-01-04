let body_theme = localStorage.getItem('theme');

document.addEventListener('DOMContentLoaded', function () {
    body_theme = localStorage.getItem('theme');
    let bodyClass = null;
    if(body_theme === "dark-mode"){
        bodyClass = "form-dark";
    }
    else{
        bodyClass = "form-light;"
    }
    // const bodyClass = document.body.classList.contains('dark-mode') ? 'form-dark' : 'form-light';
    let form = document.getElementById('registration-form');
    form.classList.add(bodyClass);
});

modeToggle.addEventListener('click', () =>{
    if (window.location.pathname === '/logout/'){
        window.location.assign('');
    }
    else{
        window.location.reload();
    }
});