const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
const margin = ({top: 20, right: 30, bottom: 30, left: 40})
const width = window.innerWidth;
const height = window.innerHeight;
(async (d3) => {
	const fetchData = async () => {
		let request = fetch('tgstat-views-pul-pervogo-sept-2021.json');
		const data = await request.then(async(response) => {
			let arr = await response.json();
			let dates = Object.values(arr.labels)
			let values = Object.values(arr.values)
			let r = []
			for(const key of dates){
				let keyYear = getYear(dates.indexOf(key));
				const hyphenated_key = new Date((`${key} ${keyYear}`).replace(' ', '-'));
				let entry = {};
				entry[hyphenated_key] = values[dates.indexOf(key)]
				r.push(entry);
			}
			return r;
		})
		return data;
	}
	const getYear = (index) => {
		if(index < 40) return "2020"
		else return "2021"
	}
	const dataset = await fetchData();
	let sorted_dataset = dataset.sort((a,b) => Object.keys(b)[0] - Object.keys(a)[0])
	const svg = d3.select('#root').append('svg:svg').attr("viewBox", [0, 0, width, height]);

	var xScale = d3.scaleTime().domain([new Date(Object.keys(sorted_dataset[0])[0]), new Date(Object.keys(sorted_dataset.at(-1))[0])])
		.range([margin.left, width - margin.right])
	var months = 
		[... new Set(sorted_dataset.map(
			(entry) => 
				(new Date(Object.keys(entry)[0]).getMonth()+1).toString()+'/'
				+new Date(Object.keys(entry)[0]).getFullYear().toString()
		))]
	console.log(months)
	var xAxis = d3.axisBottom(xScale)
			.tickFormat(d3.timeFormat("%b\n %Y"))
			.tickValues(xScale.ticks(10))
	let minValue = d3.min(sorted_dataset.map((entry) => Object.values(entry)[0]))
	let maxValue = d3.max(sorted_dataset.map((entry) => Object.values(entry)[0]))
	var yAxis = d3.scaleLinear()
		.range([height - margin.bottom, margin.top])
		.domain([minValue, maxValue])

	var gX = svg.append("g").attr("transform",`translate(0,${height - margin.bottom})`).call(xAxis);
	svg.append("g").attr("transform",`translate(${margin.left},0)`).call(d3.axisRight(yAxis))
	svg
	.selectAll("myline")
	.data(sorted_dataset)
	.enter()
	.append("line")
		.attr('x1', (d) => xScale((new Date(Object.keys(d)[0]))))
		.attr('x2', (d) => xScale((new Date(Object.keys(d)[0]))))
		.attr('y1', (d) => yAxis(0))
		.attr('y2', (d) => yAxis(Object.values(d)[0]))
		.attr('data-date', (d) => new Date(Object.keys(d)[0]).toString())
	.attr('stroke', 'grey')
	.attr('transform',`translate(0,0)`)
})(d3)