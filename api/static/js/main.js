fetch('/api/vis/discovery_methods_bar')
  .then((response) => response.json())
  .then((data) => {

    new Chart("myChart", {
      type: "bar",
      data: {
        labels: data.X,
        datasets: [{
          label: 'none',
          data: data.Y
        }]
      },
      options: {
        plugins: {
          legend: {
            display: false,
          }
        }
      }
    });
  })





