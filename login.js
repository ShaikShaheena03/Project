

var submitError = document.getElementById("subit-error");

var studentCheck = /^[0-9]+[0-9]+[0-9]+[0-9]+[0-9]+[0-9]$/
/*var sectionCheck = /^(?=.*?[A-Z])(?=.*?[a-z])$/*/

function validateid() {
    var studentid = document.getElementById("studentid").value;
    var idError = document.getElementById("id-error");
    var studentCheck = /^[A-Za-z0-9 .]+$/

    if (studentid.length == 0) {
        idError.innerHTML = "Please enter your id";
        return false;
    }
    if (!studentid.match(studentCheck)) {
        idError.innerHTML = "Please enter valid id";
        return false;
    }
    idError.innerHTML = "Valid"
    return true;
}

function validateSec() {
    var section = document.getElementById("section");
    var sectionError = document.getElementById("section-error");
    var sectionCheck = /^[A-Za-z.]+$/

    if (section.length == 0) {
        sectionError.innerHTML("Please enter your section");
        return false
    }
    if (!section.match(sectionCheck)) {
        sectionError.innerHTML = "PLease enter valid course id "
        return false;
    }
    sectionError.innerHTML = "valid"
    return true
}


function validateForm() {
    var submitError = document.getElementById("subit-error");
    if (!validateid()) {
        submitError.innerHTML = "Please fix error to submit";
        return false;
    }
    alert("Your Results")
    return true;
}


var idError = document.getElementById("id-error");
var sectionError = document.getElementById("section-error");
var submitError = document.getElementById("subit-error");



function validateid() {
    var studentid = document.getElementById("studentid").value;

    if (studentid.length == 0) {
        idError.innerHTML = "Please enter your id";
        return false;
    }
    if (!studentid.match(studentCheck)) {
        idError.innerHTML = "Please enter valid id";
        return false;
    }
    idError.innerHTML = "Valid"
    return true;
}

function validateSec() {
    var section = document.getElementById("section");

    if (section.length == 0) {
        sectionError.innerHTML("Please enter your section");
        return false
    }
}
function validateForm() {
    if (!validateid()) {
        submitError.innerHTML = "Please fix error to submit";
        return false;
    }
    alert("Your Results")
    return true;
}
