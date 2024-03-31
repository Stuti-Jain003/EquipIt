// Helper function to send AJAX requests
function sendRequest(method, url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(null, JSON.parse(xhr.responseText));
            } else {
                callback(xhr.status);
            }
        }
    };
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
}

// Function to handle adding a new comment
function addComment() {
    var commentText = document.getElementById('comment_text').value;

    // Validate commentText if needed

    // Send request to server to add a new comment
    sendRequest('POST', '/add_comment/' + postId, { comment_text: commentText }, function (err, data) {
        if (!err) {
            // Update the UI or perform any other necessary actions
            console.log('Comment added successfully:', data);
            // You may refresh the page or update the comments section dynamically
        } else {
            console.error('Error adding comment:', err);
            // Handle the error
        }
    });
}

// Function to handle adding a new reply
function addReply(type, parentId) {
    var replyText = document.getElementById('reply_text').value;
    var url = type === 'comment' ? '/add_reply/' + parentId : '/add_reply/' + parentId;

    // Validate replyText if needed

    // Send request to server to add a new reply
    sendRequest('POST', url, { reply_text: replyText }, function (err, data) {
        if (!err) {
            // Update the UI or perform any other necessary actions
            console.log('Reply added successfully:', data);
            // You may refresh the page or update the comments section dynamically
        } else {
            console.error('Error adding reply:', err);
            // Handle the error
        }
    });
}

// Function to handle liking or disliking a comment or reply
function handleLike(type, id) {
    var url = type === 'comment' ? '/like_comment/' + id : '/like_reply/' + id;

    // Send request to server to record the like
    sendRequest('POST', url, {}, function (err, data) {
        if (!err) {
            // Update the UI or perform any other necessary actions
            console.log('Like recorded successfully:', data);
            // You may update the like count or perform other UI updates
        } else {
            console.error('Error recording like:', err);
            // Handle the error
        }
    });
}

// Function to handle disliking a comment or reply
function handleDislike(type, id) {
    var url = type === 'comment' ? '/dislike_comment/' + id : '/dislike_reply/' + id;

    // Send request to server to record the dislike
    sendRequest('POST', url, {}, function (err, data) {
        if (!err) {
            // Update the UI or perform any other necessary actions
            console.log('Dislike recorded successfully:', data);
            // You may update the dislike count or perform other UI updates
        } else {
            console.error('Error recording dislike:', err);
            // Handle the error
        }
    });
}

// Add any other functions or event listeners as needed
