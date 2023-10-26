//var username = document.getElementsByName('uname')
//var password = document.getElementsByName('psw')

var username = document.getElementById('uname_box')
var password = document.getElementById('psw_box')
var msg_box  = document.getElementById('msg_box')
var remember_me = document.getElementById('remember_me')

const login_button = document.getElementById("login_btn")

let admin_username = "admin"
let admin_password = "admin"

//if ( localStorage.check )

function IsRememberMe() {
    if ( remember_me.checked && username.value !== "" ){
        localStorage.username = username.value
        localStorage.password = password.value
        localStorage.checkbox = remember_me.value
    }
    else {
        localStorage.username = ""
        localStorage.password = ""
        localStorage.checkbox = ""
    }
}

if ( localStorage.checkbox && localStorage.checkbox !== "" ){
    remember_me.setAttribute("checked", "checked")
    username.value = localStorage.username
    password.value = localStorage.password
}
else {
    remember_me.removeAttribute("checked")
    username.value = ""
    password.value = ""
}

remember_me.addEventListener( 'click', () => {
    IsRememberMe()
} )

login_button.addEventListener('click', () => {
    //console.log( username.value )
    //console.log( password.value )

    if ( username.value == admin_username ){
        console.log(remember_me.value)
        // check password
        if ( password.value == admin_password){
            console.log("Password mached")
            msg_box.innerHTML = "Password matched"   
            window.location.href = "approve_page.html"
        } 
        else{
            console.log("Password did not match")
            msg_box.innerHTML = "Password did not matched"    
        }
    }
    else{
        console.log("Username incorrect")
        msg_box.innerHTML = "Username incorrect"
    }
})
