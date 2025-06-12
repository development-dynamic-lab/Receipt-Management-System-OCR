document.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.querySelector('.login');
    const signupRedirectBtn = document.querySelector('.signup');
    const signupSubmitBtn = document.querySelector('.signup-after');

    // Login functionality
    if (loginBtn) {
        loginBtn.addEventListener('click', async function () {
            const username = document.querySelector('#username').value;
            const password = document.querySelector('#password').value;
            const personName = document.querySelector('#name').value;

            if (personName && username && password) {
                console.log('Logging in with:', username);
                const data = await sendloginCredentials(personName, username, password);

                if (data && data.status) {
                    localStorage.setItem('loginName', data.loginName); 
                    alert(data.status);
                    window.location.href = '/dashboard'

                } else {
                    alert('Login failed: ' + (data.error || 'Unknown error'));
                }
            } else {
                alert('Please enter both username and password.');
            }
        });
    }

    // Redirect to signup page
    if (signupRedirectBtn) {
        signupRedirectBtn.addEventListener('click', function () {
            window.location.href = '/signup';
        });
    }

    // Sign-up functionality
    if (signupSubmitBtn) {
        signupSubmitBtn.addEventListener('click', async function () {
            const email = document.querySelector('#email').value;
            const password = document.querySelector('#signuppassword').value;

            if (email && password) {
                console.log('Signing up with:', email, 'and password:', password);
                const data = await sendCredentialsToFirebase(email, password);

                if (data && data.status) {
                    alert(data.status);
                    window.location.href = '/';
                } else {
                    alert('Signup failed: ' + (data.error || 'Unknown error'));
                }
            } else {
                alert('Please enter both email and password.');
            }
        });
    }


});

// Login API Call
async function sendloginCredentials(personName, username, password) {
    try {
        const response = await fetch('/api/sendlogincredentials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ personName, username, password })
        });

        return await response.json();
    } catch (error) {
        console.error('Error during login:', error);
    }
}

// Signup API Call
async function sendCredentialsToFirebase(email, password) {
    try {
        const response = await fetch('/api/sendcredentialstofirebase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        return await response.json();
    } catch (error) {
        console.error('Error during signup:', error);
    }
}


