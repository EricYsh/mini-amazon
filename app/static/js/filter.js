document.addEventListener('DOMContentLoaded', function() {
    // 功能：切换筛选选项的可见性
    function toggleFilterOptions(filterId) {
        var filterElement = document.getElementById(filterId);
        filterElement.style.display = filterElement.style.display === 'none' ? 'block' : 'none';
    }

    // 获取筛选选项的数据并更新选择菜单
    function fetchFilterOptions(filterType) {
        var url = `/get-filter-options?type=${filterType}`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            const selectElement = document.getElementById(filterType + 'Filter');
            selectElement.innerHTML = '';  // 清空现有选项
            // 添加一个空选项作为默认选项
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '-- Select an option --';
            selectElement.appendChild(defaultOption);

            data.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.id || option.date || option.name;  // 根据数据类型设置value
                optionElement.textContent = option.name || option.date;  // 根据数据类型设置显示文本
                selectElement.appendChild(optionElement);
            });
            toggleFilterOptions(filterType + 'Filter');  // 显示下拉菜单
        })
        .catch(error => console.error('Error fetching filter options:', error));
    }

    // 绑定按钮事件，触发筛选选项数据的获取
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

    // 监听下拉选项的变化并更新购买历史表格
    ['itemFilter', 'sellerFilter', 'dateFilter'].forEach(filter => {
        document.getElementById(filter).addEventListener('change', function() {
            const filterType = this.id.replace('Filter', '');
            const filterValue = this.value;
            updatePurchaseHistory(filterType, filterValue);
        });
    });

    // 更新购买历史表格
    function updatePurchaseHistory(filterType, filterValue) {
        const url = new URL(window.location.href);
        url.searchParams.set('filter_type', filterType);
        url.searchParams.set('filter_value', filterValue);
      
        window.location.href = url.toString();
    }
});


// 从服务器获取按类别划分的购买数据
fetch('/get-purchases-by-category')
  .then(response => response.json())
  .then(categoryData => {
    // 绘制购买数量饼图
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

    // 绘制购买总金额柱状图
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
              display: false}}
      }
    });
  })
  .catch(error => console.error('Error fetching category data:', error));