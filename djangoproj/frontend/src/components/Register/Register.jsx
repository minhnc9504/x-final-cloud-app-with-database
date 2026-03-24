async function register(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (result.success) {
            alert('Registration successful! You can now log in.');
            window.location.href = '/admin/';
        } else {
            alert('Registration failed: ' + (result.message || result.error));
        }
    } catch (error) {
        alert('Registration failed. Please try again.');
    }
}

function Register() {
    return (
        <div className="register_container">
            <form onSubmit={register}>
                <h2>Sign Up</h2>
                <input type="text" name="username" placeholder="Username" required />
                <input type="text" name="first_name" placeholder="First Name" required />
                <input type="text" name="last_name" placeholder="Last Name" required />
                <input type="email" name="email" placeholder="Email" required />
                <input type="password" name="password" placeholder="Password" required />
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default Register;
