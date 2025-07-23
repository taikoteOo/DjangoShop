async function removeItemFetch(event){
    let row = event.target.closest('tr');
    let productId = row.querySelector("#productId").value

    let itemInfo = {
        productIdValue: productId,
    };

    let response = await fetch('/cart/remove_fetch/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
      body: JSON.stringify(itemInfo),
    });
    }

async function removeItem(event){
    await removeItemFetch(event);
    afterRemoveItem(event.target.parentElement.parentElement.parentElement);
    getQuantityInCart();
    getTotalPriceCart();
}

async function getCartLength(){
    let response = await fetch('/cart/length/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },

    });

    let result = await response.json();
    alert(result.cart_length);
};

function getTotalPriceCart(){
    let itemPriceInputs = document.querySelectorAll("#itemPrice");
    let totalPrice = 0;
    itemPriceInputs.forEach((item, index)=>{
        totalPrice += +item.textContent;
        });
    let totalPriceCart = document.querySelector("#totalPriceCart");
    totalPriceCart.textContent = totalPrice;
    return totalPrice;
}

function getQuantityInCart(){
    let cartLengthHeader = document.querySelector("#cartLengthHeader")
    let quantityInputs = document.querySelectorAll(".prod_quantity");
    let allQuantity = 0;
    quantityInputs.forEach((item,index)=>{
        allQuantity += +item.value;
    });
    let cartLength = document.querySelector("#cartLength");
    cartLength.textContent = allQuantity;
    cartLengthHeader.textContent = allQuantity;
    return allQuantity;
}

function updatePrice(event){
    let quantity = event.target.value;
    let itemPrice = event.target.parentElement.parentElement.querySelector("#itemPrice")
    let productPrice = event.target.parentElement.parentElement.querySelector("#productPrice").textContent
    productPrice = Number(productPrice.replace(",","."))

    let newItemPrice = productPrice * quantity;
    itemPrice.textContent = newItemPrice;
    getQuantityInCart();
    getTotalPriceCart();

};

function afterRemoveItem(item){
    item.remove()
}

async function saveCartInSession(event){
    let productId = event.target.parentElement.parentElement.querySelector("#productId").value
    let quantity = event.target.value;

    let cartInfo = {
        productIdValue: productId,
        quantityValue: quantity,
        totalQuantity: getQuantityInCart(),
        totalPrice: getTotalPriceCart(),
    };

    let response = await fetch('/cart/update_cart_session/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
      body: JSON.stringify(cartInfo),
    });

let result = await response.json();
};

const quantityInput = document.querySelectorAll(".prod_quantity")
quantityInput.forEach((item)=>{item.addEventListener('change', updatePrice)})
quantityInput.forEach((item)=>{item.addEventListener('change', saveCartInSession)})

const itemsRemove = document.querySelectorAll(".removeFetch")
itemsRemove.forEach((item)=>{item.addEventListener('click', removeItem)})