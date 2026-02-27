document.addEventListener('DOMContentLoaded', function() {
    
    // Login form validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Username validation
            const username = document.getElementById('username');
            const usernameError = document.getElementById('username-error');
            if (username.value.trim() === '') {
                usernameError.textContent = 'Username is required';
                username.classList.add('is-invalid');
                isValid = false;
            } else {
                usernameError.textContent = '';
                username.classList.remove('is-invalid');
            }
            
            // Password validation
            const password = document.getElementById('password');
            const passwordError = document.getElementById('password-error');
            if (password.value.trim() === '') {
                passwordError.textContent = 'Password is required';
                password.classList.add('is-invalid');
                isValid = false;
            } else {
                passwordError.textContent = '';
                password.classList.remove('is-invalid');
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // Registration form validation
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Username validation
            const username = document.getElementById('username');
            const usernameError = document.getElementById('username-error');
            if (username.value.trim() === '') {
                usernameError.textContent = 'Username is required';
                username.classList.add('is-invalid');
                isValid = false;
            } else if (username.value.length < 3) {
                usernameError.textContent = 'Username must be at least 3 characters';
                username.classList.add('is-invalid');
                isValid = false;
            } else {
                usernameError.textContent = '';
                username.classList.remove('is-invalid');
            }
            
            // Email validation
            const email = document.getElementById('email');
            const emailError = document.getElementById('email-error');
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email.value.trim() === '') {
                emailError.textContent = 'Email is required';
                email.classList.add('is-invalid');
                isValid = false;
            } else if (!emailPattern.test(email.value)) {
                emailError.textContent = 'Please enter a valid email';
                email.classList.add('is-invalid');
                isValid = false;
            } else {
                emailError.textContent = '';
                email.classList.remove('is-invalid');
            }
            
            // Password validation
            const password = document.getElementById('password');
            const passwordError = document.getElementById('password-error');
            if (password.value.trim() === '') {
                passwordError.textContent = 'Password is required';
                password.classList.add('is-invalid');
                isValid = false;
            } else if (password.value.length < 6) {
                passwordError.textContent = 'Password must be at least 6 characters';
                password.classList.add('is-invalid');
                isValid = false;
            } else {
                passwordError.textContent = '';
                password.classList.remove('is-invalid');
            }
            
            // Confirm password validation
            const confirmPassword = document.getElementById('confirm-password');
            const confirmError = document.getElementById('confirm-error');
            if (confirmPassword.value.trim() === '') {
                confirmError.textContent = 'Please confirm your password';
                confirmPassword.classList.add('is-invalid');
                isValid = false;
            } else if (confirmPassword.value !== password.value) {
                confirmError.textContent = 'Passwords do not match';
                confirmPassword.classList.add('is-invalid');
                isValid = false;
            } else {
                confirmError.textContent = '';
                confirmPassword.classList.remove('is-invalid');
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // Real-time validation (as user types)
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                this.classList.remove('is-invalid');
            }
        });
    });
});