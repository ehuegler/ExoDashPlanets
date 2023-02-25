fetch('/api/vis/discovery_methods_bar')
  .then((response) => response.json())
  .then((dataRaw) => {

    let data = []
    dataRaw.X.forEach((x, i) => {
      data[i] = {}
      data[i].type = x
      data[i].count = dataRaw.Y[i]
    })
    console.log(data)

    let margin = { top: 10, right: 30, bottom: 90, left: 40 },
      width = 800 - margin.left - margin.right,
      height = 450 - margin.top - margin.bottom;

    let svg = d3.select("#first-graph")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    let x = d3.scaleBand()
      .range([0, width])
      .padding(0.1)
    x.domain(data.map(function (d) { return d.type; }));

    let y = d3.scaleLinear()
      .range([0, height])
    y.domain([d3.max(data, function (d) { return d.count; }), 0]);

    svg.selectAll("mybar")
      .data(data)
      .enter()
      .append('rect')
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.type); })
      .attr('width', x.bandwidth())
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return height - y(d.count); });

    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    svg.append("g")
      .call(d3.axisLeft(y));
  })





