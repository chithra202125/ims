function updateStock(id) {
    fetch('/update_stock/' + id, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        });
}
