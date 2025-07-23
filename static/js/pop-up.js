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
        "password2": password2  // ← обязательно!
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

registerSendBtn.addEventListener('click', registerSend);