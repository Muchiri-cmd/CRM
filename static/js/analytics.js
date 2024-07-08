   // Retrieve and parse the JSON data
   const chartData = JSON.parse(document.getElementById('chartData').textContent);
   console.log(chartData);  // Log the parsed data to the console for inspection
   
   const ctx = document.getElementById('myChart').getContext('2d');
   
   const config = {
       type: 'line',
       data: chartData,
       options: {
           responsive: true,
           plugins: {
               legend: {
                   display: true
               }
           },
           scales: {
               y: {
                   beginAtZero: true, 
               }
           }
       }
   };
   
   const myChart = new Chart(ctx, config);
   
   function toggleDataset(index) {
       const meta = myChart.getDatasetMeta(index);
       meta.hidden = meta.hidden === null ? !myChart.data.datasets[index].hidden : null;
       myChart.update();
   }