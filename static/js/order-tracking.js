// Order tracking with real-time updates
// Backend integration marked with TODO comments

document.addEventListener('DOMContentLoaded', function() {
    
    // Only run on order status page
    if (!window.location.pathname.includes('/orders/status/')) return;
    
    // ---------- Get order ID from URL ----------
    function getOrderIdFromUrl() {
        const pathParts = window.location.pathname.split('/');
        // URL format: /orders/status/123/
        return pathParts[pathParts.length - 2] || 'unknown';
    }
    
    const orderId = getOrderIdFromUrl();
    console.log('Tracking order:', orderId);
    
    // ---------- Step elements ----------
    const steps = [
        { element: document.querySelector('.step-order-placed'), name: 'placed' },
        { element: document.querySelector('.step-confirmed'), name: 'confirmed' },
        { element: document.querySelector('.step-preparing'), name: 'preparing' },
        { element: document.querySelector('.step-on-the-way'), name: 'on_the_way' },
        { element: document.querySelector('.step-delivered'), name: 'delivered' }
    ];
    
    // ---------- Progress bar ----------
    const progressBar = document.querySelector('.progress-bar');
    
    // ---------- Estimated time element ----------
    const estimatedTimeEl = document.getElementById('estimated-time');
    
    // ---------- Update UI based on order status ----------
    function updateOrderStatus(status) {
        console.log('Updating UI for status:', status);
        
        // TODO: Replace with actual status mapping
        // Expected status values: 'placed', 'confirmed', 'preparing', 'on_the_way', 'delivered'
        
        const statusOrder = ['placed', 'confirmed', 'preparing', 'on_the_way', 'delivered'];
        const currentIndex = statusOrder.indexOf(status);
        
        if (currentIndex === -1) return;
        
        // Update step indicators
        steps.forEach((step, index) => {
            if (step.element) {
                const circle = step.element.querySelector('div:first-child');
                if (index <= currentIndex) {
                    // Completed step
                    circle?.classList.add('bg-warning');
                    circle?.classList.remove('bg-light', 'border');
                } else {
                    // Incomplete step
                    circle?.classList.remove('bg-warning');
                    circle?.classList.add('bg-light', 'border');
                }
            }
        });
        
        // Update progress bar width
        if (progressBar) {
            const percent = ((currentIndex + 1) / statusOrder.length) * 100;
            progressBar.style.width = percent + '%';
        }
        
        // TODO: Update estimated time from backend
        // if (estimatedTimeEl) {
        //     estimatedTimeEl.textContent = data.estimated_time;
        // }
    }
    
    // ---------- Poll order status ----------
    function pollOrderStatus() {
        console.log(`Polling order status for order: ${orderId}`);
        
        // TODO: Replace with actual API call
        // Expected endpoint: GET /api/orders/{orderId}/status/
        
        /*
        fetch(`/api/orders/${orderId}/status/`)
            .then(response => response.json())
            .then(data => {
                updateOrderStatus(data.status);
                if (estimatedTimeEl) {
                    estimatedTimeEl.textContent = data.estimated_time;
                }
            })
            .catch(error => console.error('Error fetching order status:', error));
        */
        
        // For demo purposes, cycle through statuses every 3 seconds
        // Remove this when backend is ready
        const demoStatuses = ['placed', 'confirmed', 'preparing', 'on_the_way', 'delivered'];
        let demoIndex = 0;
        
        setInterval(() => {
            updateOrderStatus(demoStatuses[demoIndex]);
            demoIndex = (demoIndex + 1) % demoStatuses.length;
        }, 3000);
    }
    
    // Start polling
    pollOrderStatus();
});