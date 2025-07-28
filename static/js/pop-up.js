const openPopUp = document.getElementById('open_pop_up');
const closePopUp = document.getElementById('pop_up_close');
const popUp = document.getElementById('pop_up');

openPopUp.addEventListener('click', function(e){
    e.preventDefault();
    popUp.classList.add('active');
})

closePopUp.addEventListener('click', () => {
    popUp.classList.remove('active');
})

const registerSendBtn = document.querySelector("#register");

async function registerSend(event) {
    event.preventDefault();

    const myForm = event.target.parentElement;
    const username = myForm.username.value;
    const birthday = myForm.birthday.value;
    const email = myForm.email.value;
    const password = myForm.password.value;
    const password2 = myForm.password2.value;

    let userInfo = {
        "username": username,
        "birthday": birthday,
        "email": email,
        "password": password,
        "password2": password2
    };

    try {
        let response = await fetch('/users/registration/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify(userInfo),
        });

        let result = await response.json();

        if (result.success) {
            alert('Регистрация успешно завершена!');
            window.location.replace(result.url);
        } else {
            alert('Ошибки: ' + JSON.stringify(result.errors));
            console.log(result.errors);
        }

    } catch (error) {
        alert('Ошибка соединения с сервером');
        console.error(error);
    }
}

registerSendBtn.addEventListener('click', registerSend);

const openPopUp2 = document.getElementById('open_pop_up2');
const closePopUp2 = document.getElementById('pop_up_close2');
const popUp2 = document.getElementById('pop_up2');

openPopUp2.addEventListener('click', function(e){
    e.preventDefault();
    popUp2.classList.add('active');
})

closePopUp2.addEventListener('click', () => {
    popUp2.classList.remove('active');
})

const loginSendBtn = document.querySelector("#login");

async function loginSend(event) {
    event.preventDefault();

    const myForm = event.target.parentElement;
    const username = myForm.username.value;
    const password = myForm.password.value;

    let userInfo = {
        "username": username,
        "password": password,
    };

    try {
        let response = await fetch('/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify(userInfo),
        });

        let result = await response.json();

        if (result.success) {
            alert('С возвращением!');
            window.location.replace(result.url);  // переходим на главную
        } else {
            // Если есть ошибки — можно вывести (пока просто alert)
            alert('Ошибки: ' + JSON.stringify(result.errors));
            console.log(result.errors);
        }

    } catch (error) {
        alert('Ошибка соединения с сервером');
        console.error(error);
    }
}

loginSendBtn.addEventListener('click', loginSend);