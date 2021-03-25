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
                createPopup('post liked');
                $row.html("<button onclick='unlikePost("+id+")' id='likeButton'>💘Liked</button>");
            } else{
                $row.html("<button onclick='likePost("+id+")'id='likeButton'>❤Like</button>");
            }
        }
    });
}