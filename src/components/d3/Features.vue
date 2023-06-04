<!-- SECTION 2 - AUDIO FEATURES -->
<template>
        <v-container fill-height fluid>
            <v-row align="center" justify="center" >

                <!-- Chart -->
                <v-col cols="8">
                    <div class='container-chart-features' ref="chart"></div>
                </v-col>

                <!-- Description -->
                <v-col cols="4">
                    <v-card elevation="25" class="description-features" v-if="isFeatureSelected">
                        <v-card-title class="title-bio" style="color:white">
                           <span :style="{color:color}"> {{ featureName }} </span>
                        </v-card-title>
                        <v-card-text class="text-bio" >
                            <p style="color:white; font-size:15px; font-weight:lighter">
                                 {{ description }}                         
                            </p>
                        </v-card-text>
                    </v-card>

                    <v-card elevation="25" class="description-features" v-else>
                        <v-card-text >
                            <div class="groot">
                                <v-img :src="logoGroot" width="100"></v-img>
                            </div>                            
                            <p style="color:white; font-size:15px; font-weight:lighter">
                                Explore a direct comparison of audio features extracted directly from Spotify. 
                                The mean value (expressed in %) for each feature is displayed, allowing you to analyze and compare them. 
                                <br/><br/>
                                💡Simply hover your mouse over a feature to access a brief description.
                            </p>
                        </v-card-text>
                    </v-card>
                </v-col>

                
            </v-row>
        </v-container>
</template>

<script>
import * as d3 from 'd3';
import features from '../../assets/data/features.json';
import descriptions from '../../assets/data/description.json';
import logoGroot from '../../assets/data/groot-vignette.png';


export default {

    data() {
      return {
        Names : ["Joy", "Love", "Trust", "Fear", "Awe",  "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
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
        featureName: "",
        description: "",
        isFeatureSelected: false,
        logoGroot: logoGroot
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
        name() {
            return this.Names[this.index].toLowerCase();
        },
        myFeatures() {
            //Retrieve audio features for current emotion
            let feature = [];
            for (let key in features[this.name]) {
                //Set to correct data input for chart
                feature.push({key: key, Value: features[this.name][key]})
            }
            return feature
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
            //Set up variables
            const height = 500;
            const width = 500;
            const data = this.myFeatures;
            const color = this.color;
            const color2 = this.color_derivation;

            //Select the existing svg element or create a new one if it does not exist yet
            let svg = d3.select(this.$refs.chart).select("svg#my-features");
            if (svg.empty()) {
                svg = d3.select(this.$refs.chart).append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("id", "my-features")
            }

            //Remove existing elements
            svg.selectAll(".my-bar").remove();
            svg.selectAll(".my-bar-text").remove();
            svg.selectAll(".my-bar-legend").remove();

            // Create X axis
            let x = d3.scaleLinear()
                .domain([0, 100])
                .range([ 0, width]);

            // Create Y axis 
            let y = d3.scaleBand()
                .range([0, height])
                .domain(data.map(function(d) { return d.key; }))
                .padding(.6);
                      
            //Bars
            svg.selectAll(".my-bar")
                .data(data)
                .enter()
                    .append("rect")
                        .attr("class", "my-bar") 
                        .attr("x", x(0)) 
                        .attr("y", function(d) { return y(d.key); })
                        .attr("width", function(d) { return x(d.Value); })
                        .attr("height", y.bandwidth() )
                        .style("fill", color)
                        .style('cursor', 'pointer')
                    .on("mouseover", function(event, d) {
                        overFeature(event, d);
                    })
                    .on("mouseout", function(event, d) {
                        outFeature(event, d);
                    })

            //Text inside bars 
            svg.selectAll(".my-bar-text")
                .data(data)
                .enter()
                    .append("text")
                        .attr("class", "my-bar-text") 
                        .attr("x", function(d) { return x(d.Value) + 10;})
                        .attr("y", function(d) { return y(d.key) + y.bandwidth()/2; })
                        .attr("dy", ".35em") 
                        .text(function(d) { return `${d.Value}%`; })
                        .attr("fill", color2)
                        .attr("font-size", "14px")
                        .attr("font-weight", "bold")

            //Legend 
            svg.selectAll(".my-bar-legend")
                .data(data)
                .enter()
                    .append("text")
                        .attr("class", "my-bar-legend") 
                        .attr("x", function(d) { return x(0)})
                        .attr("y", function(d) { return y(d.key) - 6})
                        .text(function(d) { return d.key.charAt(0).toUpperCase() + d.key.slice(1); })
                        .style("fill", "white")
                        .attr("font-size", "14px")
            
            //Show description of feature when hovering over it
            const overFeature = (event, d) => {
                //Change stroke of bar
                d3.select(event.target).style("stroke", color2);
                d3.select(event.target).style("stroke-width", "2px");
                //Retrieve description of feature
                this.isFeatureSelected = true;
                this.featureName = d.key.charAt(0).toUpperCase() + d.key.slice(1);
                this.description = descriptions[d.key];
            }

            const outFeature = (event, d) => {
                //Change stroke of bar
                d3.select(event.target).style("stroke", "none");
                //Reset description of feature
                this.isFeatureSelected = false;
                this.featureName = "";
                this.description = "";
            }
        }
    }
}
</script>

<style scoped>
.container-chart-features {
    padding-top:45px;
    padding-bottom:45px;
    margin-left: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.description-features {
    background : #191919;
}

.groot {
    display: flex;
    justify-content: center;
    align-items: center;
    width : 200px;
    padding-bottom: 20px;
    padding-left:100px;
}
</style>