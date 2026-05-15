window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        toggle_theme: function(theme_value) {
            const theme = (theme_value && theme_value.length > 0) ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            return theme === 'dark' ? 'dark-mode-active' : '';
        }
    }
});

// Wait for the Dash app to load
window.addEventListener('load', function() {
    console.log("D3.js integration loaded");
    
    // Interval to check for map existence and apply enhancements
    setInterval(function() {
        const deviationMap = document.getElementById('deviation-map');
        if (deviationMap && d3) {
            enhanceDeviationMap(deviationMap);
        }
    }, 2000);
});

function enhanceDeviationMap(container) {
    // Select all path elements (regions) in the map
    const regions = d3.select(container).selectAll('path.choropleth');
    
    regions.each(function() {
        const path = d3.select(this);
        const data = path.datum();
        
        // Custom logic can be added here based on the data
        // For example, pulse animation for high deviations
        // This is a placeholder for advanced D3 effects
    });
}

// Custom Tooltip Positioning or Animated Legends can be implemented here
