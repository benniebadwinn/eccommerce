function sendData (productId) {
    fetch('http://127.0.0.1:8000/add-wishlist', {
        method: 'POST',
        body: JSON.stringify({
            'productId': productId
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        },
    })
};

