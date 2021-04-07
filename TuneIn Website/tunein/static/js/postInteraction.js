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
                var likes = numToStr(data.likes);

                var $row = $('#'+id+' > div:eq(3) > div:eq(0)');
                $row.html("<button class='btn' onclick='unlikePost("+id+")' id='likeButton'><span class='btn-icon'>💘"+likes+"</span><span class='btn-text'>Liked</span></button>");
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
                var likes = numToStr(data.likes);

                var $row = $('#'+id+' > div:eq(3) > div:eq(0)');
                $row.html("<button class='btn' onclick='likePost("+id+")'id='likeButton'><span class='btn-icon'>❤"+likes+"</span><span class='btn-text'>Like</span></button>");
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
            var likes = numToStr(data.likes);
            if (data.liked) {
                $row.html("<button class='btn' onclick='unlikePost("+id+")' id='likeButton'><span class='btn-icon'>💘"+likes+"</span><span class='btn-text'>Liked</span></button>");
            } else{
                $row.html("<button class='btn' onclick='likePost("+id+")'id='likeButton'><span class='btn-icon'>❤"+likes+"</span><span class='btn-text'>Like</span></button>");
            }
        }
    });
}

function showCommentPopup(id){
    if($("#cc_"+id).length){
        //closes comment area
        $("#cc_"+id).remove();
    }
    else{
        var container = document.createElement('DIV');
        $(container).attr('id', 'cc_'+id);
        
        var title = document.createElement('h3');
        title.innerHTML='Comments:';
        $(container).append(title);
        var comments = document.createElement('DIV');
        $.ajax({
            url: appurl+'getComments',
            data: {
                'postID': id
            },
            dataType: 'json',
            success: function (data) {
                if(data.amount >0){
                    data.comments.forEach(element => {
                        var comment = document.createElement('DIV');
                        comment.classList.add('comments');
                        comment.classList.add('comments:hover');
                        var username = document.createElement('b');
                        username.innerText = element.user +': ';
                        var message = document.createElement('span');
                        message.innerText = element.message;  
                        $(comment).append(username);
                        $(comment).append(message);
                        $(comments).append(comment);
                        if(element.isUser){
                            var delButton = document.createElement('BUTTON');
                            delButton.classList.add('commentDelButton');
                            delButton.classList.add('commentDelButton:hover');
                            delButton.innerText = 'x';
                            delButton.onclick = function(){
                                deleteComment(id,element.id);
                            }
                            $(comment).append(delButton);
                        }
                    });
                }
            }
        });
       
        
        $(container).append(comments);
        
        //you can't serialize a form so we're just gonna make one the hard way
        var commentField = document.createElement('TEXTAREA');
        $(commentField).attr('id', 'cf_'+id);
        var formbutton = document.createElement('button');
        formbutton.innerText = 'Post';
        formbutton.onclick = function(){postComment(id);};
        $(container).append(commentField);
        $(container).append(formbutton);
        $("#"+id).append(container);
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

function deleteComment(p,id){
    $.ajax({
        url: appurl+'deleteComment',
        data: {
            'c_id': id
        },
        dataType: 'json',
        success: function (data) {
            if (data.message) {
                createPopup('comment removed');
                
                showCommentPopup(p);
                showCommentPopup(p);
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
function numToStr(x){
    var xStr = "";

    if(x < 1000){
        xStr = x;
    } else if(x > 1000 && x < 1000000){
        xStr = (x/1000).toPrecision(2) + "K";
    } else if(x> 1000000){
        xStr = (x/1000000).toPrecision(2) + "M";
    }

    return xStr;
}