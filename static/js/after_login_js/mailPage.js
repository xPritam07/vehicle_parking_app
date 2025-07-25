function sendReply(event) {
    event.preventDefault(); // Prevent form submission

    const replyText = document.getElementById("replyMessage").value.trim();
    if (!replyText) {
        alert("Please type your reply before sending.");
        return;
    }

    const recipient = document.getElementById('recipient').innerText.split(' ')[2];
    const subject = "Reply to your query";
    const body = encodeURIComponent(replyText);

    const gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=${recipient}&su=${encodeURIComponent(subject)}&body=${body}`;

    window.open(gmailLink, '_blank');

    setTimeout(() => {
        window.location.href = "http://127.0.0.1:5000/admin/doubts";
    }, 2000);
}