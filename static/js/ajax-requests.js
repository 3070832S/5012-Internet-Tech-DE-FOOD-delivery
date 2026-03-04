// AJAX requests for favorites page
// Backend integration marked with TODO comments

document.addEventListener('DOMContentLoaded', function() {
    
    // Only run on favorites page
    if (!document.querySelector('.favorite-btn')) return;
    
    // ---------- Favorite / Unfavorite Restaurant ----------
    const favoriteBtns = document.querySelectorAll('.favorite-btn');
    
    favoriteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const restaurantId = this.dataset.restaurantId;
            const icon = this.querySelector('i');
            
            // Toggle heart icon immediately for better UX
            if (icon.classList.contains('bi-heart')) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill', 'text-danger');
                
                // TODO: Send request to add to favorites
                // Expected endpoint: POST /api/favorites/add/
                // Parameters: { restaurant_id: restaurantId }
                
            } else {
                icon.classList.remove('bi-heart-fill', 'text-danger');
                icon.classList.add('bi-heart');
                
                // TODO: Send request to remove from favorites
                // Expected endpoint: POST /api/favorites/remove/
                // Parameters: { restaurant_id: restaurantId }
            }
            
            console.log(`TODO: Toggle favorite for restaurant ${restaurantId}`);
            
            // Example of what the real code will look like:
            /*
            fetch(`/api/favorites/toggle/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ restaurant_id: restaurantId })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Favorite toggled:', data);
            })
            .catch(error => console.error('Error:', error));
            */
        });
    });
    
    // Helper function to get CSRF token (if needed)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});