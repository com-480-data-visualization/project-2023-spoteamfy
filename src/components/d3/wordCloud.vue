<!-- SECTION 2 - WORDCLOUD -->
<template>
    <div>
        <v-container fill-height fluid>
            <v-row align="center" justify="center">
                <v-col cols="8">
                    <div class='container-chart-word' ref="chart"></div>
                </v-col>
                <v-col cols="4">
                    <div class="groot">
                        <v-img :src="logoGroot" width="100px"></v-img>
                    </div>
                    <p style="color:white; font-size:15px; font-weight:lighter">
                        Here is a wordcloud that represents the 30 most common tags 
                        across all tracks of {{name}}. 
                        <br/>
                        The size of each tag is proportional to its frequency of appearance across the tracks.
                    </p>
                </v-col>
            </v-row>

        </v-container>


    </div>
</template>

<script>
import * as d3 from 'd3';
import cloud from 'd3-cloud';
import tags from '../../assets/data/tags_per_emotion.json';
import logoGroot from '../../assets/data/groot-vignette.png';

export default {

    data() {
      return {
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
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
        logoGroot:logoGroot,
      };
    },

    computed: {
        index() {
            return this.$store.state.index;
        },
        color() {
            return this.Colors[this.index];
        },
        color_derivation() {
            return this.Colors_derivation[this.index];
        },
        name() {
            return this.Names[this.index].toLowerCase();
        },
        myWords () {
            const myTags = tags[this.name];
            let myWords = null;
            //Only select the 30 most used tags 
            myWords = myTags.sort((a, b) => b.size - a.size).slice(0, 30);
            return myWords
        }
    },

    mounted() {
        this.updateWordCloud();
    },

    watch : {
        index() {
            this.updateWordCloud();
        }
    },

    methods : {
        updateWordCloud() {
            //Set size of svg
            const width = 700;
            const height = 600; 
            //Retrieve data
            const myWords = this.myWords;
            const color = this.color_derivation;
            //Set scale of words
            const fontScale = d3.scaleLinear().range([18, 45]); 
            const minSize = d3.min(myWords, d => d.size);
            const maxSize = d3.max(myWords, d => d.size);
            fontScale.domain([minSize, maxSize]);
            
            //Select the existing svg element or create a new one if it does not exist yet
            let svg = d3.select(this.$refs.chart).select("svg#my-wordcloud");
            if (svg.empty()) {
                svg = d3.select(this.$refs.chart).append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("id", "my-wordcloud")
            }

            //Remove the previous word cloud
            svg.selectAll("text").remove();

            //Create the word cloud
            let layout = cloud()
                .size([width, height])
                .words(myWords.map(function(d) { return {text: d.word, size:d.size}; }))
                .padding(10) //Space between words
                .fontSize(d => fontScale(d.size))
                .spiral("rectangular") // "archimedean" or "rectangular"
                .rotate(function() { return ~~(Math.random() * 3) * 45; })
                .on("end", draw);
            layout.start();

            //Draw the word cloud
            function draw(words) {
                svg
                .append("g")
                .attr("transform", "translate(" + width  / 2 + "," + height / 2 + ")")
                .selectAll("text")
                    .data(words)
                    .enter()
                        .append("text")
                        .style("font-size", function(d) { return d.size; })
                        .style("fill", function(d, i) { return color[i%3];})
                        .attr("text-anchor", "middle")
                        .style("font-family", "POPPINS")
                        .attr("transform", function(d) {
                            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                        })
                        .text(function(d) { return d.text; })
                }
            },

        },
}
</script>

<style scoped>
.container-chart-word {
    height: 600px;
    width: 700px;
    position: relative;
}

.groot {
    display : flex;
    justify-content: center;
    align-items: center;
    width : 200px;
    padding-bottom : 20px;
    padding-left: 100px;
}
</style>