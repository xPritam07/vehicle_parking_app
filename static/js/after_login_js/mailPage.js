function sendReply(event) {
    event.preventDefault(); // Prevent form submission

    const replyText = document.getElementById("replyMessage").value.trim();
    if (!replyText) {
        alert("Please type your reply before sending.");
        return;
    }

    const recipient = "{{ doubt.email }}";
    const subject = "Reply to your query";
    const body = encodeURIComponent(replyText);

    const gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=${recipient}&su=${encodeURIComponent(subject)}&body=${body}`;

    // Open Gmail compose window in a new tab
    window.open(gmailLink, '_blank');

    // Redirect to doubt page after a short delay
    setTimeout(() => {
        window.location.href = "http://127.0.0.1:5000/admin/doubts";
    }, 2000);
}