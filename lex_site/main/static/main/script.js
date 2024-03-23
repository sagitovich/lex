console.log("JavaScript файл успешно подключен!");

function userInfo() {
    var username = document.getElementById('username').value;
    $.ajax({
        url: '/userMain',
        data: {
            'username': username
        },
        dataType: 'text',
        success: function (data) {
            document.getElementById('content').innerHTML = data;
        },
        error: function (xhr, status, error) {
            console.error('AJAX Error: ', status, error);
        }
    });
}

function userSubscriptions() {
    var username = document.getElementById('username').value;
    $.ajax({
        url: '/userSubscriptions',
        data: {
            'username': username
        },
        dataType: 'text',
        success: function (data) {
            document.getElementById('content').innerHTML = data;
        },
        error: function (xhr, status, error) {
            console.error('AJAX Error: ', status, error);
        }
    });
}

function userFriends() {
    var username = document.getElementById('username').value;
    document.getElementById('content').innerHTML = "ДРУЗЬЯ пользователя " + username;
}

function userPosts() {
    var username = document.getElementById('username').value;
    document.getElementById('content').innerHTML = "ЗАПИСИ пользователя " + username;
}

function groupInfo() {
    console.log("groupInfo()")
    var groupname = document.getElementById('groupname').value;
    $.ajax({
        url: '/groupMain',
        data: {
            'groupname': groupname
        },
        dataType: 'text',
        success: function (data) {
            document.getElementById('content').innerHTML = data;
        },
        error: function (xhr, status, error) {
            console.error('AJAX Error: ', status, error);
        }
    });
}

function communitySubscribers() {
    var community = document.getElementById('groupname').value;
    document.getElementById('content').innerHTML = "ПОДПИСЧИКИ сообщества " + community;
}

function userComments() {
    var username = document.getElementById('username').value;
    var community = document.getElementById('groupname').value;
    document.getElementById('content').innerHTML = "КОММЕНТАРИИ пользователя " + username + " в сообществе " + community;
}

function allComments() {
    var community = document.getElementById('groupname').value;
    document.getElementById('content').innerHTML = "ВСЕ КОММЕНТАРИИ из сообщества " + community;
}
