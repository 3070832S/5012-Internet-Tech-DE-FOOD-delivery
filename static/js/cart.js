// Shopping cart UI interactions (frontend only)
// Backend integration marked with TODO comments

document.addEventListener('DOMContentLoaded', function() {
    
    // ---------- UI Interactions (can run without backend) ----------
    
    // Increase quantity
    const increaseBtns = document.querySelectorAll('.increase-qty');
    increaseBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.qty-input');
            let currentVal = parseInt(input.value);
            input.value = currentVal + 1;
            updateItemSubtotal(this);
            updateCartTotal();
            
            // TODO: Call backend API to update quantity in database
            // Expected endpoint: POST /carts/api/update/
            // Parameters: { item_id: XXX, quantity: newValue }
        });
    });
    
    // Decrease quantity
    const decreaseBtns = document.querySelectorAll('.decrease-qty');
    decreaseBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.qty-input');
            let currentVal = parseInt(input.value);
            if (currentVal > 1) {
                input.value = currentVal - 1;
                updateItemSubtotal(this);
                updateCartTotal();
                
                // TODO: Call backend API to update quantity
            }
        });
    });
    
    // Remove item
    const removeBtns = document.querySelectorAll('.remove-item');
    removeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const row = this.closest('.cart-item-row');
            const itemId = row.dataset.itemId; // You'll need to add data-item-id in HTML
            
            row.remove();
            updateCartTotal();
            
            // TODO: Call backend API to delete item from cart
            // Expected endpoint: POST /carts/api/remove/
            // Parameters: { item_id: itemId }
        });
    });
    
    // Manual quantity input
    const qtyInputs = document.querySelectorAll('.qty-input');
    qtyInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) this.value = 1;
            updateItemSubtotal(this);
            updateCartTotal();
            
            // TODO: Call backend API to update quantity
        });
    });
    
    // ---------- UI Calculation Functions (no backend needed) ----------
    
    // Update individual item subtotal
    function updateItemSubtotal(element) {
        const row = element.closest('.cart-item-row');
        const price = parseFloat(row.querySelector('.item-price').dataset.price);
        const qty = parseInt(row.querySelector('.qty-input').value);
        const subtotal = price * qty;
        row.querySelector('.item-subtotal').textContent = '$' + subtotal.toFixed(2);
    }
    
    // Update cart total
    function updateCartTotal() {
        const subtotals = document.querySelectorAll('.item-subtotal');
        let total = 0;
        subtotals.forEach(sub => {
            total += parseFloat(sub.textContent.replace('$', ''));
        });
        
        const cartSubtotal = document.getElementById('cart-subtotal');
        const deliveryFee = document.getElementById('delivery-fee');
        const cartTotal = document.getElementById('cart-total');
        
        if (cartSubtotal) {
            cartSubtotal.textContent = '$' + total.toFixed(2);
        }
        
        if (deliveryFee && cartTotal) {
            const fee = parseFloat(deliveryFee.dataset.fee || 5);
            cartTotal.textContent = '$' + (total + fee).toFixed(2);
        }
    }
});