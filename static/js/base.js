// ===== Global JavaScript for Food Delivery =====

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Navbar active state based on current URL
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        // Remove active class from all links
        link.classList.remove('active');
        
        // Add active class if href matches current path
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
        
        // Special handling for nested paths
        if (currentPath.includes('/restaurants/') && link.getAttribute('href') === '/restaurants/') {
            link.classList.add('active');
        }
        if (currentPath.includes('/cart/') && link.getAttribute('href') === '/cart/') {
            link.classList.add('active');
        }
        if (currentPath.includes('/orders/') && link.getAttribute('href') === '/orders/') {
            link.classList.add('active');
        }
    });
    
    // 2. Back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopBtn.id = 'back-to-top';
    backToTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #ffc107;
        color: #212529;
        border: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        cursor: pointer;
        display: none;
        z-index: 999;
        transition: all 0.3s;
        font-size: 20px;
    `;
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // 3. Add security attributes to external links
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
        if (!link.getAttribute('href').includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
    
    // 4. Lazy loading for images (if browser supports)
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // 5. Console welcome message (just for fun)
    console.log('🍔 Food Delivery - Frontend loaded successfully!');
    console.log('📱 Responsive design enabled');
    console.log('🚀 Ready to order!');
    
    // 6. Auto-dismiss alerts after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 3000);
    });
});