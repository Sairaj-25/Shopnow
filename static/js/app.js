// Function to navigate back to the previous page
function goBack() {
    // Navigate to the previous page
    window.history.back();
    
    // Set a small delay before reloading the page
    setTimeout(function() {
        window.location.reload(); // Reload the page after navigating back
    }, 100); // Delay in milliseconds (adjust as needed)
}


// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function () {
    // Get the CSRF token for secure requests
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Function to check the cart and update the UI
    function checkCartAndUpdateUI() {
        axios.get("/get_cart/") // Endpoint to fetch cart data
            .then(response => {
                const cartItems = response.data.cart_items; // Assuming { product_id: quantity }

                cartItems.forEach(item => {
                    const productContainer = document.querySelector(`[data-id='${item.product_id}']`)?.closest(".product-container");

                    if (productContainer) {
                        // Hide "Add" button
                        const addToCartButton = productContainer.querySelector(".add-to-cart");
                        addToCartButton.style.display = "none";

                        // Show quantity controls
                        updateCartUI(item.product_id, item.quantity, productContainer);
                    }
                });
            })
            .catch(error => console.log(error));
    }

    // Add to cart handler
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.getAttribute("data-id");
    
            // Check if user is logged in before adding to cart
            axios.get("/login_check")
                .then(response => {
                    if (!response.data.isAuthenticated) {
                        // Redirect to login page if user is not authenticated
                        window.location.href = "/login?next=" + window.location.pathname;
                    } else {
                        // If user is authenticated, proceed with adding to cart
                        axios.post("/add_to_cart/", { product_id: productId }, {
                            headers: { "X-CSRFToken": csrftoken }
                        }).then(response => {
                            const cartQuantity = response.data.quantity;
                            const productContainer = this.closest(".product-container");
    
                            // Hide the "Add" button and show quantity controls if quantity > 0
                            if (cartQuantity > 0) {
                                this.style.display = "none"; // Hide the Add button
                                updateCartUI(productId, cartQuantity, productContainer); // Update the cart UI with controls
                            }
                        }).catch(error => console.log(error));
                    }
                })
                .catch(error => console.log("Error checking login status:", error));
        });
    });


    // Function to update the cart UI with quantity controls (+, -)
    function updateCartUI(productId, cartQuantity, productContainer) {
        const existingQuantityControls = productContainer.querySelector(`#cart-item-${productId}`);

        if (!existingQuantityControls) {
            const newCartItem = document.createElement("div");
            newCartItem.id = `cart-item-${productId}`;
            newCartItem.classList.add("input-group");
            newCartItem.innerHTML = `
                <button class="btn btn-secondary btn-sm fw-bold decrement" data-id="${productId}">-</button>
                <input type="text" class="form-control form-control-sm text-center text-primary w-25" value="${cartQuantity}" id="qty-${productId}" readonly>
                <button class="btn btn-secondary btn-sm fw-bold increment" data-id="${productId}">+</button>
            `;
            productContainer.querySelector(".cart-item-container").appendChild(newCartItem);

            // Attach event listeners for the increment and decrement buttons
            addQuantityEventListeners();
        }
    }

    // Function to add event listeners for increment and decrement buttons
    function addQuantityEventListeners() {
        // Attach click event listeners to the decrement and increment buttons
        document.querySelectorAll(".decrement").forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.getAttribute("data-id");
                updateQuantity(productId, "decrement");
            });
        });

        document.querySelectorAll(".increment").forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.getAttribute("data-id");
                updateQuantity(productId, "increment");
            });
        });
    }

    // Function to update the quantity and sync with backend
    function updateQuantity(productId, action) {
        // Get the current quantity from the input field
        const quantityField = document.getElementById(`qty-${productId}`);
        let currentQuantity = parseInt(quantityField.value);

        // Determine new quantity based on action
        let newQuantity = currentQuantity; // Default to current quantity
        if (action === "increment") {
            newQuantity = currentQuantity + 1;
        } else if (action === "decrement") {
            newQuantity = currentQuantity - 1;
        }

        // Prevent quantity from going below 0
        if (newQuantity < 0) return;

        // Send request to the backend to update the cart
        axios.post("/update_cart/", { product_id: productId, action: action }, {
            headers: { "X-CSRFToken": csrftoken }
        }).then(response => {
            const updatedQuantity = response.data.quantity;

            // Update the UI with the updated quantity
            quantityField.value = updatedQuantity;

            // If quantity is 0, show the "Add" button and remove quantity controls
            if (updatedQuantity === 0) {
                const cartItem = document.querySelector(`#cart-item-${productId}`);
                if (cartItem) {
                    cartItem.remove(); // Remove quantity controls
                }

                // Show the "Add" button again
                const productContainer = document.querySelector(`[data-id='${productId}']`).closest(".product-container");
                const addToCartButton = productContainer.querySelector(".add-to-cart");
                addToCartButton.style.display = "block";
            }
        }).catch(error => console.log(error));
    }

    // Fetch cart items and update UI on page load
    checkCartAndUpdateUI();
});



function removeFromCart(productId) {
    axios.delete(`/remove-from-cart/${productId}/`, {
        headers: {
            "X-CSRFToken": "{{ csrf_token }}"
        }
    })
    .then(response => {
        if (response.status === 200) {
            // Remove the cart item from the UI
            document.getElementById(`cart-item-${productId}`).remove();

            document.getElementById("cart-count").innerText = response.data.total_quantity;

            // Update totals dynamically
            document.getElementById("total-amount").innerText = response.data.Total;

            document.getElementById("grand-total").innerText = response.data.GrandTotal;

            // Update delivery charges logic
            if (response.data.Total > 199) {
                document.getElementById("delivery-charges").innerText = "free";
            } else {
                document.getElementById("delivery-charges").innerText = response.data.delivery_charges;
            }

            // Check if the cart is empty, show empty cart message
            if (response.data.cart_items.length === 0) {
                document.getElementById("order-details").remove(); // Remove order details section
                document.getElementById("cart-title").innerHTML =`<p class="text-center">Your cart is empty. <a href="/">Start Shopping</a></p>`
            }
        }
    })
    .catch(error => {
        console.error("Error removing item:", error);
    });
}

// Store the current scroll position
function storeScrollPosition() {
    const scrollPosition = window.scrollY || window.pageYOffset;
    sessionStorage.setItem('scrollPosition', scrollPosition);
}

// Restore the scroll position
function restoreScrollPosition() {
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        // window.scrollTo(0, parseInt(scrollPosition)); // Stop Scrolling

        window.scrollTo({
            top: parseInt(scrollPosition),
            behavior: 'auto' // Instant jump (no smooth scrolling)
            // in style.css html,body tag scroll-behavior: auto !important; Added
        });

        sessionStorage.removeItem('scrollPosition'); // Clear the stored position
    }
}

// Call this function when the page loads
document.addEventListener("DOMContentLoaded", restoreScrollPosition);