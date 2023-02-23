fetch('/api/vis/discovery_methods_bar')
  .then((response) => response.json())
  .then((data) => {

    console.log(data.Y)

    new Chart("discoveryChart", {
      type: "bar",
      data: {
        labels: data.X,
        datasets: [{
          label: 'Count',
          data: data.Y,
        }]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: 'Number of Exoplanets Found by Method'
          },
          legend: {
            display: false,
          }
        },
        scales: {
          y: {
            type: 'logarithmic',
          },
        },
      }
    });
  })





