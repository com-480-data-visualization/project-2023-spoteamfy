<!-- SECTION 1 - LOLIPPOP -->
<template>
    <div class="playlists">
        <h3 class="featuresTitle">
            <span :style="{ color: color }">{{ name_title }} {{ smiley }}</span>
        </h3>
        <v-container fill-height fluid>
            <v-row align="center" justify="center">
                <div class='container-chart-lollipop' ref="chart"></div>
            </v-row>            
        </v-container>
    </div>
</template>

<script>
import * as d3 from 'd3';
import links from '../../assets/data/links.json';

export default {

    data() {
      return {
        Names : ["Joy", "Love", "Trust", "Fear", "Awe",  "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
        Colors_derivation : [
            ["#FF0000", "#ff8d8d", "#FB4242"],
            ["#ff8000", "#ffe2c5", "#ffb061"],
            ["#ffff00", "#ffffb2", "#ffff81"],
            ["#80ff00", "#c6ff8d", "#e7ffce"],
            ["#00ff00", "#99ff99", "#d0ffd0"],
            ["#00ffff", "#b0ffff", "#deffff"],
            ["#0080ff", "#68b4ff", "#bbddff"],
            ["#0000ff", "#6f6fff", "#b2b2ff"],
            ["#A639FF", "#c47dff", "#e1beff"],
            ["#8000ff", "#ae5cff", "#cfa0ff"],
            ["#ff00ff", "#ff78ff", "#ffc0ff"],
            ["#ff0080", "#ff73b9", "#ffbedf"]
        ],
        Smileys : ["😀", "😍", "🤗", "😱", "😲", "😢", "😔", "🤢", "😒", "😡", "🤔", "🙂"],
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
        emotion2Smiley : {
            "Joy": "😀",
            "Love": "😍",
            "Trust": "🤗",
            "Fear": "😱",
            "Awe": "😲",
            "Sadness": "😢",
            "Remorse": "😔",
            "Disgust": "🤢",
            "Contempt": "😒",
            "Anger": "😡",
            "Anticipation": "🤔",
            "Optimism": "🙂"
        },
        emotion2Color : {
            "Joy": "#FF0000",
            "Love": "#ff8000",
            "Trust": "#ffff00",
            "Fear": "#80ff00",
            "Awe": "#00ff00",
            "Sadness": "#00ffff",
            "Remorse": "#0080ff",
            "Disgust": "#0000ff",
            "Contempt": "#A639FF",
            "Anger": "#8000ff",
            "Anticipation": "#ff00ff",
            "Optimism": "#ff0080"
        }
    }
    },
    computed: {
        index() {
            return this.$store.state.index;
        },
        color() {
            return this.Colors[this.index];
        },
        color_derivation () {
            return this.Colors_derivation[this.index][2];
        },
        name() {
            return this.Names[this.index].toLowerCase();
        },
        name_title() {
            return this.Names[this.index];
        },
        smiley() {
            return this.Smileys[this.index];
        },
        myLinks() {
            const links_data = links[this.index];
            //Retrieve links for current emotion
            let link = [];
            for (let key in links_data) {
                //Filter if when rounded to int, the value is 0
                if (Math.round(links_data[key]) == 0) {
                    continue;
                }
                //Set to correct data input for chart
                link.push({key: key, Value: links_data[key]})
            }
            return link;
        },        
    },

    mounted() {
        this.createChart();
    },

    watch: {
        index() {
            this.createChart();
        }
    },

    methods : {
        createChart() {
            //Set up chart and data
            const height = 500;
            const margin_left = 120;
            const width = 400 - margin_left; 

            const data = this.myLinks;
            data.sort(function(b, a) {
                return a.Value - b.Value;
            });
            const smileys = this.emotion2Smiley;
            const colors = this.emotion2Color;    

            const color = this.color;
            const color2 = this.color_derivation;

            //Select the existing svg element or create a new one if it does not exist yet
            let svg = d3.select(this.$refs.chart).select("svg#my-lollipop");
            if (svg.empty()) {
                svg = d3.select(this.$refs.chart).append("svg")
                .attr("width", width + margin_left)
                .attr("height", height)
                .attr("id", "my-lollipop")
            }

            //Remove previous chart
            svg.selectAll(".mycircle").remove();
            svg.selectAll(".myline").remove();
            svg.selectAll(".mylegend").remove();
            svg.selectAll(".myvalue").remove();

            // Create X axis
            let x = d3.scaleLinear()
                .domain([0, 70])
                .range([ 0, width]);

            // Create Y axis 
            let y = d3.scaleBand()
                .range([0, height])
                .domain(data.map(function(d) { return d.key; }))
                .padding(.9);

            // Lines
            svg.selectAll(".myline")
                .data(data)
                .enter()
                .append("line")
                    .attr("class", "myline")
                    .attr("x1", x(0))
                    .attr("x2", x(0))
                    .attr("y1", function(d) { return y(d.key); })
                    .attr("y2", function(d) { return y(d.key); })
                    .attr("stroke", color) 
                    .attr("stroke-width", "1.5px")
                    .attr("transform", "translate(" + margin_left + ")")
                    .on("mouseover", function(event, d) {
                            const param = "line"
                            return mouseOver(event, d, param);
                        })
                        .on("mouseout", function(event, d) {
                            return mouseOut(event, d);
                        })    
                    .transition()
                        .duration(1000)
                        .attr("x2", function(d) { return x(d.Value); })
        
            // Circles, Smileys
            svg.selectAll(".mycircle")
                .data(data)
                .enter()
                .append("text")
                    .attr("class", "mycircle")
                    .attr("x", function(d) { return x(0); })
                    .attr("y", function(d) { return y(d.key); })
                    .attr("dy", "0.35em")
                    .attr("text-anchor", "middle")
                    .text(function(d,i) { return smileys[d.key]; })
                    .attr("transform", "translate(" + margin_left + ")")
                    .on("mouseover", function(event, d) {
                            const param = "circle"
                            return mouseOver(event, d, param);
                        })
                        .on("mouseout", function(event, d) {
                            return mouseOut(event, d);
                        })
                    .transition()
                        .duration(1000)
                        .attr("x", function(d) { return x(d.Value); })
            
            //Y-ticks text
            svg.selectAll(".mylegend")
                .data(data)
                .enter()
                    .append("text")
                        .attr("class", "mylegend") 
                        .attr("x", function(d) { return x(0) - 8;})
                        .attr("y", function(d) { return y(d.key)})
                        .attr("dy", ".35em") 
                        .attr("text-anchor", "end")
                        .text(function(d) { return d.key })
                        .attr("fill", function(d) { return colors[d.key]; })
                        .attr("font-size", "15px")
                        .attr("font-weight", "bold")
                        .attr("transform", "translate(" + margin_left + ")")
                        .on("mouseover", function(event, d) {
                            const param = "legend"
                            return mouseOver(event, d, param);
                        })
                        .on("mouseout", function(event, d) {
                            return mouseOut(event, d);
                        });

            //Values on the right
            svg.selectAll(".myvalue")
                .data(data)
                .enter()
                    .append("text")
                        .attr("class", "myvalue") 
                        .attr("x", function(d) { return x(d.Value) + 15 ;})
                        .attr("y", function(d) { return y(d.key)})
                        .attr("dy", ".35em") 
                        .attr("text-anchor", "start")
                        //Round to integer for readability
                        .text(function(d) { return Math.round(d.Value) + "%"})
                        .attr("fill", color)
                        .attr("font-size", "14px")
                        .attr("font-weight", "lighter")
                        .attr("transform", "translate(" + margin_left + ")")
            
            //Add y-axis (vertical line)
            svg.append("line")
                .attr("x1", x(0))
                .attr("x2", x(0))
                .attr("y1", 0)
                .attr("y2", height)
                .attr("stroke", color2) 
                .attr("stroke-width", "1px")
                .attr("transform", "translate(" + margin_left + ")");
            
            //Called when mouseover
            const mouseOver = (event, d, param) => {
                //Cursor
                d3.select(event.target).style("cursor", "pointer");
                //Current element
                const myItem = d3.select(event.target);
                //Retrieve all items (depending where user mouseover)
                let all_items = null; 
                if (param == "legend") {
                    all_items = svg.selectAll(".mylegend");
                } else if (param == "circle") {
                    all_items = svg.selectAll(".mycircle");
                } else if (param == "line") {
                    all_items = svg.selectAll(".myline");
                }
                //Retrieve index of current item
                const my_index = all_items.nodes().indexOf(myItem.node());

                //Retrieve all values
                const all_values = svg.selectAll(".myvalue");

                //Change color of value for the current index
                all_values.each(function(d, i) {
                    if (i == my_index) {
                        d3.select(this).transition()
                            .duration(200)
                            .style("fill", function(d) { return colors[d.key]; })
                            .attr("font-weight", "bold");
                    }
                })

                //Change color of line for the current index
                const all_lines = svg.selectAll(".myline");
                all_lines.each(function(d, i) {
                    if (i == my_index) {
                        d3.select(this).transition()
                            .duration(200)
                            .attr("stroke", function(d) { return colors[d.key]; })
                            .attr("stroke-width", "4px");
                    }
                })
                
            }

            //Called when mouseout
            const mouseOut = (event, d) => {
                //Reset values
                const all_values = svg.selectAll(".myvalue");
                all_values.transition()
                    .duration(200)
                    .style("fill", color)
                    .attr("font-weight", "lighter");
                
                //Reset color of line
                const all_lines = svg.selectAll(".myline");
                all_lines.transition()
                    .duration(200)
                    .attr("stroke", color)
                    .attr("stroke-width", "1.5px");
            }
        }
    }
}
</script>

<style scoped>
.featuresTitle {
    text-align: center;
}   
</style>