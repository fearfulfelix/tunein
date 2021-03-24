function are_they_friends(){
    var target = document.getElementById('username').innerText
    $.ajax({
        url: appurl+'are_they_friends',
        data:{
            'target': target
        },
        success: function (data) {
            if (data.Friends == 'True') {
                document.getElementById('friendButton').onclick = function(){ unfriend(target)};
                document.getElementById('friendButton').innerText = "Unfriend-";
            } else if(data.Friends == 'False'){
                document.getElementById('friendButton').onclick = function(){ friend(target)};
                document.getElementById('friendButton').innerText = "Friend+";
            } else if(data.Friends == 'Requested'){
                document.getElementById('friendButton').onclick = function(){ cancel_friend_request(target)};
                document.getElementById('friendButton').innerText = "Pending-";
            } 
        }
    });
}

function are_they_being_followed(){
    var target = document.getElementById('username').innerText
    $.ajax({
        url: appurl+ 'are_they_being_followed',
        data:{
            'target': target
        },
        success: function (data) {
            if($('#followButton').length){
            if (data.followBool == true) {
                document.getElementById('followButton').onclick = function(){ unfollow(target)};
                document.getElementById('followButton').innerText = "Unfollow-";
            } else{
                document.getElementById('followButton').onclick = function(){ follow(target)};
                document.getElementById('followButton').innerText = "Follow+";
            }
        }
        }
    });
}

function what_are_they(){
    are_they_friends();
    are_they_being_followed();
}
what_are_they();
setInterval(what_are_they, 10000);