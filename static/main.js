function added() {
    alert("Success! Product has been added to your cart.");
}

function sendToWhatsapp() {
    let name = document.getElementById('name').value;
    let phone = document.getElementById('phone').value;
    let product = "{{ product.name }}"; 
    let price = "{{ product.price }}"; 

    let myNumber = "212773517986"; 
    
    let message = `Hello, I would like to order:\n` +
                  `Product: ${product}\n` +
                  `Price: ${price} DH\n` +
                  `Name: ${name}\n` +
                  `Phone: ${phone}`;

    let url = `https://wa.me/${myNumber}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank').focus();
}