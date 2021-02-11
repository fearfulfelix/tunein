function toggleVisiblilty(){
    if(document.getElementById("registrationFields").style.display =='none'){
        document.getElementById("loginFields").style.display ='none';
        document.getElementById("registrationFields").style.display ='inline-block';
        document.getElementById("loginToggle").value = "Have an account?";
    } else{
        document.getElementById("loginFields").style.display ='inline-block';
        document.getElementById("registrationFields").style.display ='none';
        document.getElementById("loginToggle").value = "Don't have an account?";
    }
}
toggleVisiblilty();