<!-- SECTION 2 - TOP 5 GENRES -->
<template>
    <div class="playlists">
        <h3 class="titleGenres">
            <span :style="{ color: color }">Top 5 Genres</span>
            <span :style="{ color: color2, 'font-size': '14px', 'font-weight' : 'lighter'}"> (by number of tracks)</span>
        </h3>
        <v-container fill-height fluid>
            <v-row align="center" justify="center">
                <div class='container-chart' ref="chart"></div>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import * as d3 from 'd3';
import genres from '../../assets/data/top_genres.json';


export default {

    data() {
        return {
        Names : ["Joy", "Love", "Trust", "Fear", "Awe",  "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
        Colors_derivation : [
            ["#FF0000", "#ff8d8d", "#fed4d4"],
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
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
        clicked_genre :false,
      };
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
        color_text() {
            if (this.name == "sadness" || this.name == "awe" || this.name == "fear" || this.name == "trust") {
                return "#191919";
            } else {
                return "white";
            }
        },
        name() {
            return this.Names[this.index].toLowerCase();
        },
        myGenres() {
            return genres[this.name];
        },
    },

    mounted (){
        this.updateGenres();
    },

    watch: {
        index() {
            this.$store.commit('setGenre', null);
            this.updateGenres();
        },
    },

    methods: {
        updateGenres() {
            
            //Set variables 
            const depth = 20; // set the depth of the rectangle
            const margin_left = 10;
            const margin_right = 10;
            const width = 550 - margin_left - margin_right; 
            const height = 400; 
            const data = this.myGenres;
            const color2 = this.color_derivation;
            const color = this.color;
            const text_color = this.color_text;

            //Create SVG
            let svg = d3.select(this.$refs.chart).select("svg#my-genres");
            if (svg.empty()) {
                svg = d3.select(this.$refs.chart).append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("id", "my-genres")
                .append("g")
            }

            //Remove previous chart
            svg.selectAll(".mybar").remove();
            svg.selectAll(".mybar-up").remove();
            svg.selectAll(".mybar-right").remove();
            svg.selectAll(".mybar-text").remove();
            svg.selectAll(".mybar-legend").remove();

            //Create scales
            let x = d3.scaleBand()
                .range([ 0, width ])
                .domain(data.map(function(d) { return d.genre; }))
                .padding(0.2);

            let y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return d.counts; })])
                .range([height , 0]);

            //Add rectangles
            svg.selectAll(".mybar")
                .data(data)
                .enter()
                .append("rect")
                    .attr("class", "mybar") // add class name to the rectangle
                    .attr("x", function(d) { return x(d.genre); })
                    .attr("y", function(d) { return y(d.counts) + 50; })
                    .attr("width", x.bandwidth())
                    .attr("height", function(d) { return height - y(d.counts) - 50; })
                    .attr("fill", color)
            
            //To store x, y, widths and heights of the rectangles
            let x_array = [];
            let y_array = [];
            let width_array = [];
            let height_array = [];

            //Get the x, y, widths and heights of the rectangles
            const rects = svg.selectAll(".mybar");
            rects.each(function(d) {
                const rect = d3.select(this);
                const x = +rect.attr("x");
                const y = +rect.attr("y");
                const width = +rect.attr("width");
                const height = +rect.attr("height");
                x_array.push(x);
                y_array.push(y);
                width_array.push(width);
                height_array.push(height);
            });

            //Add 3D effect to the rectangles

            //Add the top rectangles
            svg.selectAll(".mybar-up")
                .data(data)
                .enter()
                .append("polygon")                    
                    .attr("class", "mybar-up") 
                    .attr("fill", color2)
                    .attr("stroke", "black")
                    .attr("points", function(d, i) {
                        return (x_array[i]) + "," + (y_array[i]) + " " + 
                        (x_array[i] + depth ) + "," + (y_array[i] - depth ) + " " + 
                        (x_array[i] + depth + width_array[i]) + "," + (y_array[i] - depth) + " " +
                        (x_array[i] + width_array[i]) + "," + (y_array[i]);
                    }) 

            //Add the right rectangles
            svg.selectAll(".mybar-right")
                .data(data)
                .enter()
                .append("polygon")                    
                    .attr("class", "mybar-right") 
                    .attr("fill", color2)
                    .attr("stroke", "black")
                    .attr("points", function(d, i) {
                        return (x_array[i] + width_array[i]) + "," + (y_array[i]) + " " +
                        (x_array[i] + width_array[i] + depth) + "," + (y_array[i] - depth) + " " +
                        (x_array[i] + width_array[i] + depth) + "," + (y_array[i] - depth + height_array[i]) + " " +
                        (x_array[i] + width_array[i]) + "," + (y_array[i] + height_array[i]);
                    })
            
            // Add text on top of rectangles (Genre names)
            svg.selectAll(".mybar-text")
                .data(data)
                .enter()
                .append("text")
                    .attr("class", "mybar-text")
                    .attr("x", function(d,i) { return x_array[i] + width_array[i]/2 + depth - 7; })
                    .attr("y", function(d,i) { return y_array[i] - 25; })
                    .attr("dy", "-5px")
                    .attr("text-anchor", "middle")
                    .attr("font-size", "13px")
                    .attr("fill", "white")
                    .attr('font-weight', 'bold')
                    .text(function(d) { return d.genre.charAt(0).toUpperCase() + d.genre.slice(1) });
            
            //Add values inside the rectangles
            svg.selectAll(".mybar-legend")
                .data(data)
                .enter()
                .append("text")
                    .attr("class", "mybar-legend")
                    .attr("x", function(d,i) { return x_array[i] + width_array[i] - 5; })
                    .attr("y", function(d,i) { return y_array[i] + 23; })
                    .attr("dy", "-5px")
                    .attr("text-anchor", "end")
                    .attr("font-size", "14px")
                    .attr("fill", text_color)
                    .attr('font-weight', 'bold')
                    .text(function(d) { return d.counts});

            //Add mouse events
            svg.selectAll('.mybar')
                .style("cursor", "pointer")
                .on("click", function(event, d) {
                        clickFeature(event, d);
                    })
                .on("mouseover", function(event, d, i) {
                        hoverFeature(event, d, i);
                    })
                .on("mouseout", function(event, d, i) {
                        outFeature(event, d, i);
                    });
            
            //Functions for mouse events
            const clickFeature = (event, d, i) => {
                    const selectedGenre = d.genre;
                    this.$store.commit('setGenre', selectedGenre);
                }
        
            const hoverFeature = (event, d) => {
                //Retrieve rectangle and genre name
                const all_bars = svg.selectAll('.mybar');
                const all_text = svg.selectAll('.mybar-text');

                //Get current rectangle
                const myBar = d3.select(event.target);
                //Retrieve index 
                const my_index = all_bars.nodes().indexOf(myBar.node());

                //Change color of the rectangle 
                all_bars.each(function(d,i) {
                    const bar = d3.select(this);
                    if (i != my_index) {
                        bar.transition()
                            .duration(300)
                            .attr("fill", color2)
                    }
                })
                //Change color and size of the text
                all_text.each(function(d,i) {
                    const text = d3.select(this);
                    if (i == my_index) {
                        text.transition()
                            .duration(300)
                            .attr('fill', color)
                            .attr('font-size', '18px')
                    }
                })
            };

            const outFeature = (event, d, i) => {
                //Retrieve rectangle and genre name
                const all_bars = svg.selectAll('.mybar');
                const all_text = svg.selectAll('.mybar-text');
                
                //Retrieve index 
                const myBar = d3.select(event.target);
                const my_index = all_bars.nodes().indexOf(myBar.node());

                //Change color of the rectangle
                all_bars.each(function(d,i) {
                    const bar = d3.select(this);
                    if (i != my_index) {
                        bar.transition()
                            .duration(300)
                            .attr("fill", color)
                    }
                })

                //Change color and size of the text
                all_text.each(function(d,i) {
                    const text = d3.select(this);
                    if (i == my_index) {
                        text.transition()
                            .duration(300)
                            .attr('fill', text_color)
                            .attr('font-size', '13px')
                    }
                })
            }
        }
    }
}
</script>

<style scoped>
.titleGenres {
    text-align: center;
    padding-bottom: 30px;
}
</style>