<template>
  <v-container fill-height fluid>

  <div style="flex:auto;margin-top: 50px;margin-bottom: 50px">
      <v-row align="center" justify="center">
        <v-col cols="10">
          <p style="color: white;">
              Now let's explore the distribution of genres through different emotions by <b style="color: red;">count</b><br>
              <br>
          </p>
        </v-col>
      </v-row>
    </div>

    <div style="flex:auto"  class="parallelChart">
      <v-row align="center" justify="center">
        <v-col cols="9">
          <div class='container-chart-parallel' ref="parallel_chart" style="position: relative;"></div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import * as d3 from 'd3';
//import the data
import topGenres from '../../assets/data/adjusted_top_genres.json';

export default {
    data() {
      return {
        //store the values that we need to access them in the algorithm
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
        Names : ["Joy", "Love", "Trust", "Fear", "Awe",  "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
        genreColors : ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"],
        Genres : ['Indie', 'Rock', 'Pop', 'Folk', 'Electronic', 'Alternative', 'Hip_hop', 'Ambient', 'Martial_industrial', 'New_age'],
        genresNames : ['indie', 'rock', 'pop', 'folk', 'electronic', 'alternative', 'hip-hop', 'ambient', 'martial industrial', 'new age'],
        Smileys : ["😀", "😍", "🤗", "😱", "😲", "😢", "😔", "🤢", "😒", "😡", "🤔", "🙂"],
        indie : [],
        rock : [],
        pop : [],
        folk : [],
        electronic : [],
        alternative : [],
        hip_hop : [],
        ambient : [],
        martial_industrial : [],
        new_age : [],

        svg : null,
        margin : null,
        width : null,
        height : null,
        x : null,
        y : null,

        xAxis : null,
        yAxis : null,
        myPath : null,
      };
    },
    mounted() {
        this.create_JSON();
        this.CreateParallelChart();

        const line = this.svg
        const axis = this.svg
        const path = this.svg

        axis.selectAll(".axis").on("mouseover", function(event, d) {
            //reduce opacity of the bar
            d3.select(this)
                .transition()
                .duration('100')
                .attr('opacity', '1.0');
        //plot the corresponding emoji
        axis.selectAll(".emoji_" + d)
                .transition()
                .duration('100')
                .attr('opacity', '1.0');
                })

        axis.selectAll(".axis").on("mouseout", function(event, d) {
            //show the bar
            d3.select(this)
                .transition()
                .duration('100')
                .attr('opacity', '0.4');
            //hide the emoji
        axis.selectAll(".emoji_" + d)
                .transition()
                .duration('100')
                .attr('opacity', '0.4');
                })
  },

    methods : {
        //to create the data used in the parallel chart
        create_JSON(){
        const genres = this.genresNames;
            for (const emotion in topGenres) {
                //not enough datas for surprise and submission
                if (emotion != 'surprise' && emotion != 'submission') {
                //for each genre
                for (const i in topGenres[emotion]) {
                    if (genres.indexOf(topGenres[emotion][i].genre) > -1) {
                        let genre = topGenres[emotion][i].genre
                        //creation of a datapoint
                        let dict = {emotion   : emotion.charAt(0).toUpperCase() + emotion.slice(1),
                                    group   : genre.charAt(0).toUpperCase() + genre.slice(1),
                                    value   : topGenres[emotion][i].counts}
                        //push the created datapoint into the corresponding array
                        if (genre == 'indie') {
                            this.indie.push(dict)
                        }
                        if (genre == 'rock') {
                            this.rock.push(dict)
                        }
                        if (genre == 'pop') {
                            this.pop.push(dict)
                        }
                        if (genre == 'folk') {
                            this.folk.push(dict)
                        }
                        if (genre == 'electronic') {
                            this.electronic.push(dict)
                        }
                        if (genre == 'alternative') {
                            this.alternative.push(dict)
                        }
                        if (genre == 'hip-hop') {
                            this.hip_hop.push(dict)
                        }
                        if (genre == 'ambient') {
                            this.ambient.push(dict)
                        }
                        if (genre == 'martial industrial') {
                            this.martial_industrial.push(dict)
                        }
                        if (genre == 'new age') {
                            this.new_age.push(dict)
                        }
                    }
                }
            }
          }
        },
        //this function creates the skeleton of the svg graph
        CreateParallelChart() {
            //setup the margin, the width and the height
            this.margin = {top:100, right: 30, bottom: 100, left: 60},
            this.width  = 1000 - this.margin.left - this.margin.right,
            this.height = 800 - this.margin.top - this.margin.bottom,
            //append the svg object to the body of the page
            this.svg = d3.select(this.$refs.parallel_chart)
                            .append("svg")
                            .attr("width", this.width + this.margin.left + this.margin.right)
                            .attr("height", this.height + this.margin.top + this.margin.bottom)
                                .append("g")
                                .attr("transform","translate(" + this.margin.left + "," + this.margin.top + ")");
            //create X axis
            this.x = d3.scalePoint()
                        .range([ 0, this.width ]).domain(this.Names)
                        .padding(0.2);

            //create Y axis
            this.y = {};
            this.Names.forEach(name => {
              this.y[name] = d3.scaleLinear()
                .range([this.height, 0]).domain([0,500])
            });

            let x = this.x
            let y = this.y

            this.yAxis = this.svg.selectAll(".axis").data(this.Names).enter()
                    .append("g")
                    .attr("class", function(d) { return "axis " + d })
                    .style('color', 'white')
                    .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
                    .each(function(d) { d3.select(this).call(d3.axisLeft().ticks(5).scale(y[d])); })
                    .attr('opacity', '0.4')
                    .append("text")
                    .style("text-anchor", "middle")
                    .attr("font-family", "Poppins")
                    .attr("y", -30)
                    .attr("x", 30)
                    .text(function(d) {return d })
                    .style("font-size", "18px")
                    .style("fill", "white")
                    .attr("transform", "rotate(-50)")
                    .attr('opacity', '0.4')


          const Names = this.Names
          //UPDATE THE EMOJIS
          let Smileys = this.Smileys
          let emojis = this.svg.selectAll(".emoji").data(this.Names)

          emojis.enter()
                .append('text')
                .merge(emojis)
                .transition()
                .duration(1000)
                .text(function(d) { return Smileys[Names.indexOf(d)]; })
                .attr("class", function(d) {return "emoji" + " " + "emoji_" + d})
                .attr("x", function(d) { return x(d)+90; })
                .attr("dx", -120)
                .attr("y", 650)
                .attr("dy", 0)
                .attr("font-size" , "50px")
                .attr('opacity', '0.4')


          const genresLists = [
              this.indie, this.rock, this.pop, this.folk, this.electronic,
              this.alternative, this.hip_hop, this.ambient, this.martial_industrial,
              this.new_age
              ];

          const genreColors = this.genreColors;
          const Genres = this.Genres

          genresLists.forEach((data, index) => {
              const name = this.Genres[index];
              this.ParallelChart(data, name, x, y, genreColors, Names, Genres);
              });
        },

        ParallelChart(data, name, x, y, genreColors, Names, Genres) {

        let paths = this.svg.selectAll(".path").data([data])
        paths.enter()
              .append("path")
              .merge(paths)
              .on("mouseover", function(d, i) {
                  //show the bar
                  d3.select(this)
                      .transition()
                      .duration('100')
                      .style("stroke", "lightgrey")
                      .attr('opacity', '1.0')
                  d3.select("." + name)
                      .transition().duration(100)
                      .style("stroke", genreColors[Genres.indexOf(name)])
                      .style("opacity", "1")
              })
              .on("mouseout", function(d, i) {
                  //show the bar
                  d3.select(this)
                      .transition()
                      .duration('100')
                      .style("stroke", genreColors[Genres.indexOf(name)])
                      .attr('opacity', '1.0');
              })
              .transition().duration(1000)
              .attr("class", "path_" + name) // 2 class for each line: 'line' and the group name
              .attr("d", function (d) {
                    return d3.line()(Names.map(function(name) {
                    return [x(name), y[name](d.find(item => item.emotion === name).value)]; }));
                })
              .style("fill", "none" )
              .style("stroke", genreColors[Genres.indexOf(name)])
              .style("stroke-width", 10.0)
              .attr('opacity', '1.0')

        },
    },
}

</script>

<style scoped>
  .container-chart-parallel {
      height: 900px;
      width: 1000px;
      position: relative;
  }
</style>
