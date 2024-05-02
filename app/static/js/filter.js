document.addEventListener('DOMContentLoaded', function() {
    // Toggle visibility of filter options
    function toggleFilterOptions(filterId) {
        var filterElement = document.getElementById(filterId);
        filterElement.style.display = filterElement.style.display === 'none' ? 'block' : 'none';
    }

    // Fetch and populate filter options 
    function fetchFilterOptions(filterType) {
        var url = `/get-filter-options?type=${filterType}`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            const selectElement = document.getElementById(filterType + 'Filter');
            selectElement.innerHTML = '';  
            // Create a default option that prompts the user to select an option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '-- Select an option --';
            selectElement.appendChild(defaultOption);
            // Populate select element with options from the server
            data.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.id || option.date || option.name;  
                optionElement.textContent = option.name || option.date;  
                selectElement.appendChild(optionElement);
            });
            toggleFilterOptions(filterType + 'Filter');  
        })
        .catch(error => console.error('Error fetching filter options:', error));
    }

    // Event listeners for filter buttons
    document.getElementById('itemFilterBtn').addEventListener('click', function() {
        fetchFilterOptions('item');
    });
    document.getElementById('sellerFilterBtn').addEventListener('click', function() {
        fetchFilterOptions('seller');
    });
    document.getElementById('dateFilterBtn').addEventListener('click', function() {
        fetchFilterOptions('date');
    });
    document.getElementById('showAllBtn').addEventListener('click', function() {
        updatePurchaseHistory('', '');
    });

    // Event listener for changes in filter selection
    ['itemFilter', 'sellerFilter', 'dateFilter'].forEach(filter => {
        document.getElementById(filter).addEventListener('change', function() {
            const filterType = this.id.replace('Filter', '');
            const filterValue = this.value;
            updatePurchaseHistory(filterType, filterValue);
        });
    });

    // Update the page to show filtered purchases
    function updatePurchaseHistory(filterType, filterValue) {
        const url = new URL(window.location.href);
        url.searchParams.set('filter_type', filterType);
        url.searchParams.set('filter_value', filterValue);
      
        window.location.href = url.toString();
    }
});


// Fetch and display purchases by category using Chart.js
fetch('/get-purchases-by-category')
  .then(response => response.json())
  .then(categoryData => {
    // Setup pie chart for purchase quantities
    const quantityPieCtx = document.getElementById('quantityPieChart').getContext('2d');
    new Chart(quantityPieCtx, {
      type: 'pie',
      data: {
        labels: categoryData.map(item => item.category_name),
        datasets: [{
          data: categoryData.map(item => item.total_quantity),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#FF9F40', '#8A2BE2',
          '#00FA9A', '#00CED1', '#9370DB', '#FFD700', '#DA70D6']
        }]
      },
      options: {
        maintainAspectRatio: false,
        responsive: true
      }
    });

    // Setup bar chart for total purchase amounts
    const amountBarCtx = document.getElementById('amountBarChart').getContext('2d');
    new Chart(amountBarCtx, {
      type: 'bar',
      data: {
        labels: categoryData.map(item => item.category_name),
        datasets: [{
          data: categoryData.map(item => item.total_amount),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#FF9F40', '#8A2BE2',
          '#00FA9A', '#00CED1', '#9370DB', '#FFD700', '#DA70D6']
        }]
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
            legend: {
              display: false}}// Option to hide the legend
      }
    });
  })
  .catch(error => console.error('Error fetching category data:', error));