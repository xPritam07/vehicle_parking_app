function getDirections(event) {
    event.preventDefault();

    const form = event.target;
    const address = form.getAttribute("data-address");
    console.log(address);

    if (!address) {
        alert("No address found.");
        return;
    }
    const encodedAddress = encodeURIComponent(address);
    console.log(encodedAddress);
    const mapsURL = `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;

    window.open(mapsURL, '_blank');
}

