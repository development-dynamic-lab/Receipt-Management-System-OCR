document.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.querySelector('.login');
    const signupRedirectBtn = document.querySelector('.signup');
    const signupSubmitBtn = document.querySelector('.signup-after');
    const serviceSubmitBtn = document.querySelector('.service-submit-button')

    // Login functionality
    if (loginBtn) {
        loginBtn.addEventListener('click', async function () {
            const username = document.querySelector('#username').value;
            const password = document.querySelector('#password').value;

            if (username && password) {
                console.log('Logging in with:', username);
                const data = await sendloginCredentials(username, password);

                if (data && data.status) {
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


    // Submit button functionality
    if (serviceSubmitBtn) {
        serviceSubmitBtn.addEventListener('click', async function () {
            // Get values from the fields
            const sourceDropdown = document.querySelector('.service-dropdown');
            const apiKey = document.querySelector('.api-key');
            const interval_time = document.querySelector('.Interval');
            const month = document.querySelector('.Month');
            const targetDropdown = document.querySelector('.target-dropdown');
            const credentialsTextarea = document.querySelector('#credential');

            // Get the selected values and input
            const selectedSource = sourceDropdown.value;
            const selectedTarget = targetDropdown.value;
            const apiKeyValue = apiKey.value.trim();
            const selectedIntervalTime = interval_time.value.trim()
            const selectedMonth = month.value.trim()
            const credentialsValue = credentialsTextarea.value.trim();

            // Validate inputs
            if (!selectedSource) {
                alert('Please select a source.');
                return;
            }

            if (!apiKeyValue) {
                alert('Please enter an API Key.');
                return;
            }

            if (!selectedIntervalTime){
                alert('Please select an interval.');
                return;
            }

            if (!selectedMonth){
                alert('Please select a month.');
                return;
            }

            if (!selectedTarget) {
                alert('Please select a target.');
                return;
            }

            if (!credentialsValue) {
                alert('Please enter credentials.');
                return;
            }



            // If all validations are passed, prepare the data
            const serviceData = {
                source: selectedSource,
                apiKey: apiKeyValue,
                interval: selectedIntervalTime,
                month: selectedMonth,
                target: selectedTarget,
                credentials: credentialsValue
            };

            // Call the function to send credentials
            const data = await sendServiceCredentials(serviceData);

            if (data && data.status) {
                alert('Service credentials submitted successfully and data transfer will start shortly!');
                // Perform any further actions after successful submission
            } else {
                alert('Failed to submit service credentials: ' + (data.error || 'Unknown error'));
            }
        });
    }
});

// Login API Call
async function sendloginCredentials(username, password) {
    try {
        const response = await fetch('/api/sendlogincredentials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
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


// Send service credentials
async function sendServiceCredentials(serviceData) {
    try {
        const response = await fetch('/api/sendservicecredentials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(serviceData)
        });

        return await response.json();
    } catch (error) {
        console.error('Error during service credentials submission:', error);
        return { error: 'Failed to submit credentials' };
    }
}