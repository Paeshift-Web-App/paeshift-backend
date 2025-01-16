export default function Validation (values) {
    const errors = [];

    const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,6}$/;
    // const password_pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}$/;
    const password_pattern = /^[\w@-]{8,}$/;

    if(values.firstname === "") {
        errors.push("First name is Required");
    }
    if(values.lastname === "") {
        errors.push("last name is Required");
    }

    if(values.email === "") {
        errors.push("Email is Required");
    }
    else if(!email_pattern.test(values.email)) {
        errors.push(email_pattern.test(values.email));
    errors.push("Invalid email address");
    }

    if(values.password === "") {
        errors.push("Password is Required");
    } 
    else if(!password_pattern.test(values.password)) {
        errors.push(password_pattern.test(values.password));
        errors.push("Invalid password");
    }

    if(values.password !== values.confirmPassword ) {
        errors.push("Password did not match");
    } 
    return errors;
}