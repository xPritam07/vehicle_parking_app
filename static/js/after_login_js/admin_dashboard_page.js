document.getElementById('lot-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    const response = await fetch(form.action, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: formData
    });

    if (response.ok) {
        const newLot = await response.json();
        appendLotToTable(newLot);
        form.reset();
        alert('Parking Lot added successfully!');
    } else {
        alert('Error adding lot');
    }
});

function appendLotToTable(lot) {
    const tableBody = document.querySelector('table tbody');
    
    // Remove 'No Lot Found' row if exists
    const noLotRow = tableBody.querySelector('td[colspan="7"]');
    if (noLotRow) noLotRow.parentElement.remove();

    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${lot.id}</td>
        <td>${lot.address}</td>
        <td>${lot.pincode}</td>
        <td>${lot.parkLiteCount}</td>
        <td>${lot.parkSmartCount}</td>
        <td>${lot.parkProCount}</td>
        <td>${lot.ratings}</td>
    `;
    tableBody.appendChild(row);
}