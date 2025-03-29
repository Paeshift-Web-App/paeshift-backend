export default function Validation (values) {
    const errors = [];

    const email_pattern = /^[^\s@]+@[^\s@]+\.[^s@]{2, 6}$/
    const password_pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,}$/;

    if(values.firstname === "") {
        errors.firstname = "First name is Required";
    }
    if(values.lastname === "") {
        errors.lastname = "last name is Required";
    }

    if(values.email === "") {
        errors.email = "Email is Required";
    }
    else if(!email_pattern.test(values.email)) {
        errors.email = "Invalid email address";
    }

    if(values.password === "") {
        errors.password = "Password is Required";
    } 
    else if(!password_pattern.test(values.password)) {
        errors.password = "Invalid email address";
    }

    if(values.password !== values.confirmPassword ) {
        errors.confirmPassword = "Password did not match";
    } 

    return errors;
   
}

