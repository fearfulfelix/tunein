function likePost(id){
    $.ajax({
        url: appurl+'likePost',
        data: {
            'postID': id
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup('post liked');
                var $row = $('#'+id+' > div:eq(3) > div:eq(0)');
                $row.html("<button onclick='unlikePost("+id+")' id='likeButton'>💘Liked</button>");
            }
        }
    });
}

function unlikePost(id){
    $.ajax({
        url: appurl+'unlikePost',
        data: {
            'postID': id
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup('post liked');
                var $row = $('#'+id+' > div:eq(3) > div:eq(0)');
                $row.html("<button onclick='likePost("+id+")'id='likeButton'>❤Like</button>");
            }
        }
    });
}

function isLiked(id){
    $.ajax({
        url: appurl+'isLiked',
        data: {
            'postID': id
        },
        dataType: 'json',
        success: function (data) {
            var $row = $('#'+id+' > div:eq(3) > div:eq(0)');
            if (data.liked) {
                $row.html("<button onclick='unlikePost("+id+")' id='likeButton'>💘Liked</button>");
            } else{
                $row.html("<button onclick='likePost("+id+")'id='likeButton'>❤Like</button>");
            }
        }
    });
}

function showCommentPopup(id){
    if($("#cc_"+id).length){
        //dont open, comment box is already open
    }
    else{
        var container = document.createElement('DIV');
        container.classList.add('comment-Container');
        $(container).attr('id', 'cc_'+id);
        
        var title = document.createElement('h3');
        title.innerHTML='Comments:';
        var close = document.createElement('button');
        close.innerHTML='X';
        var comments = document.createElement('DIV');
        $.ajax({
            url: appurl+'getComments',
            data: {
                'postID': id
            },
            dataType: 'json',
            success: function (data) {
                if(data.amount >0){
                    console.log(data.amount);
                    for(var i = 0; i< data.amount;i++){
                        var comment = document.createElement('DIV');
                        var username = document.createElement('b');
                        username.innerText = data.comments[i].user +': ';
                        var message = document.createElement('span');
                        message.innerText = data.comments[i].message;
                        console.log(data.comments[i].message);
                        $(comment).append(username);
                        $(comment).append(message);
                        $(comments).append(comment);
                        if(data.comments[i].isUser){
                            var delButton = document.createElement('BUTTON');
                            delButton.innerText = 'X';
                            delButton.onclick = function(){
                                deleteComment(id,message.innerText);
                            }
                            $(comment).append(delButton);
                        }
                    }
                }
                else{
                    $(container).append('no comments!');
                    
                }
            }
        });
        close.onclick = function(){$(container).remove();}
        $(container).append(close);
        $(container).append(title);
        
        $(container).append(comments);
        
        //you can't serialize a form so we're just gonna make one the hard way
        var commentField = document.createElement('TEXTAREA');
        $(commentField).attr('id', 'cf_'+id);
        var formbutton = document.createElement('button');
        formbutton.innerText = 'Post';
        formbutton.onclick = function(){postComment(id);};
        $(container).append(commentField);
        $(container).append(formbutton);
        $("#"+id).prepend(container);
        window.location.hash = "#cc_"+id;
    }
}
function postComment(id){
    console.log($("#cf_"+id).val());
    if($("#cf_"+id).val()!= ""){
        $.ajax({
            url: appurl+'postComment',
            data: {
                'postID': id,
                'message': $("#cf_"+id).val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.message) {
                    createPopup('comment posted');
                    $("#cc_"+id).remove();
                    showCommentPopup(id);
                }
            }
        });
    }
    
}

function deleteComment(id, message){
    $.ajax({
        url: appurl+'deleteComment',
        data: {
            'postID': id,
            'message': message,
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup('comment removed');
                $("#cc_"+id).remove();
                showCommentPopup(id);
            }
        }
    });

}
function prepForSharing(id){
    if($("#sc_"+id).length){
        //dont open, comment box is already open
    }
    else{
        var container  = document.createElement('DIV');
        container.classList.add('comment-Container');//its not for comments but it still works
        $(container).attr('id', 'sc_'+id);
        var close = document.createElement('button');
        close.innerHTML='X';
        close.onclick = function(){$(container).remove();}
        var title = document.createElement('h3');
        title.innerHTML='Share to friends:';
        $(container).append(close);
        $(container).append(title);

        var commentField = document.createElement('TEXTAREA');
        $(commentField).attr('id', 'sf_'+id);
        var formbutton = document.createElement('button');
        formbutton.innerText = 'Post';
        formbutton.onclick = function(){shareToFriends(id);};
        
        $(container).append(commentField);
        $(container).append(formbutton);
        $("#"+id).prepend(container);
        window.location.hash = "#sc_"+id;
    }
}
function shareToFriends(id){
    $.ajax({
        url: appurl+'shareToFriends',
        data:{
            'postID':id,
            'message':$("#sf_"+id).val()
        },
        dataType: 'json',
        success:function (data){
            $("#sc_"+id).remove();
            
        }
    });

}