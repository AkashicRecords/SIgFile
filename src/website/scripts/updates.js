document.addEventListener('DOMContentLoaded', function() {
    const updateFeed = document.getElementById('updateFeed');
    
    // Fetch updates from JSON file
    fetch('/updates.json')
        .then(response => response.json())
        .then(data => {
            data.updates.forEach(update => {
                const updateElement = createUpdateElement(update);
                updateFeed.appendChild(updateElement);
            });
        })
        .catch(error => {
            console.error('Error loading updates:', error);
            updateFeed.innerHTML = '<p class="error">Unable to load updates. Please try again later.</p>';
        });
});

function createUpdateElement(update) {
    const div = document.createElement('div');
    div.className = `update-item ${update.type}`;
    
    div.innerHTML = `
        <div class="update-header">
            <span class="update-date">${update.date}</span>
            <span class="update-type">${update.type}</span>
        </div>
        <h3 class="update-title">${update.title}</h3>
        <p class="update-description">${update.description}</p>
        <a href="${update.link}" class="update-link">Learn more</a>
    `;
    
    return div;
} 