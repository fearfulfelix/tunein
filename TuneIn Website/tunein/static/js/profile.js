function createPopup(Gmessage){
    var notificaiton = document.createElement("DIV");
    var message = document.createElement("P");
    message.innerText = Gmessage;
    notificaiton.classList.add('message');
    $(notificaiton).append(message);
    $("#messages_go_here").append(notificaiton);

    setTimeout(function(){
        $(notificaiton).css('animation','fadeOut 2s ease')
        $(notificaiton).on('animationend webkitAnimationEnd oAnimationEnd', function(){$(notificaiton).remove();});
    }, 1000);
}

function follow(){
    $.ajax({
        url: appurl+'follow_user',
        data: {
            'target': document.getElementById("username").innerText
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup(data.message);
                what_are_they();
            }
        }
    });
}
function unfollow(){
    $.ajax({
        url: appurl+'unfollow_user',
        data: {
            'target': document.getElementById("username").innerText
        },
        dataType: 'json',
        success: function () {
                what_are_they();   
        }
    });
}


function friend(target){
    $.ajax({
        url: appurl+'friend_request_user',
        data: {
            'target': target
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup(data.message);
            }
            what_are_they();
        }
    });
}
function unfriend(target){
    $.ajax({
        url: appurl+ 'unfriend_user',
        data: {
            'target': target
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup(data.message);
            }
            what_are_they();
        }
    });
}
function accept_friend_request(target){
    $.ajax({
        url:  appurl+'accept_friend_request',
        data: {
            'target': target
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup(data.message);
            }
        }
    });
}
function cancel_friend_request(target){
    $.ajax({
        url: appurl+'cancel_friend_request',
        data: {
            'target': target
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup(data.message);
            }
        }
    });
}
function reject_friend_request(target){
    $.ajax({
        url: appurl+'reject_friend_request',
        data: {
            'target': target
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup(data.message);
            }
        }
    });
}

function delete_notification(type,from){
    $.ajax({
        url: appurl+'delete_notification',
        data:{
            'type':type,
            'from':from
        },
        dataType:'json',
        success: function(data){
            if(data.message){
                checkForNotifs();
            }
        }
    });
    
}
