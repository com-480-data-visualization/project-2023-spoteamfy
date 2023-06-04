<template>
  <v-container fill-height fluid>
  <div style="flex:auto;margin-top: 50px;margin-bottom: 50px">
      <v-row align="center" justify="center">
        <v-col cols="12">
          <p style="color: white;">
              Welcome to the mesmerizing world of musical genres !<br>
              In this section, we bring you a truly captivating experience, showcasing the distribution of genres across emotions. <br>
              Watch as the vibrant circles come alive, representing the diverse musical genres that evoke different emotions within us. <br><br>
              Feel free to use the <b style="color: red;">checkboxes</b> below to select the emotions you want to compare. By selecting specific emotions, you can explore how genres are distributed among them.<br>
              Press and drag the <b style="color: red;">nodes</b> to learn more about how genres are distributed among different emotions.<br>
              The percentages indicate the proportion of tracks belonging to each genre out of all the tracks categorized under that emotion.<br>
              Let's embark on this genre-comparing journey together, and unlock the wonders of music like never before!
              <br>
          </p>
        </v-col>
      </v-row>
    </div>
    <div style="flex:auto"  class="circularPackingChart">
      <v-row align="center" justify="center">
      <v-col cols="3">
          <v-checkbox-group>
              <v-checkbox v-model="ex4" color="#FF0000" class="checkbox_padding" value="Joy" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Joy😀</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#ff8000" class="checkbox_padding" value="Love" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Love😍</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#ffff00" class="checkbox_padding" value="Trust" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Trust🤗</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#80ff00" class="checkbox_padding" value="Fear" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Fear😱</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#00ff00" class="checkbox_padding" value="Awe" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Awe😲</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#00ffff" class="checkbox_padding" value="Sadness" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Sadness😢</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#0080ff" class="checkbox_padding" value="Remorse" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Remorse😔</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#0000ff" class="checkbox_padding" value="Disgust" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Disgust🤢</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#A639FF" class="checkbox_padding" value="Contempt" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Contempt😒</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#8000ff" class="checkbox_padding" value="Anger" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Anger😡</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#ff00ff" class="checkbox_padding" value="Anticipation" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Anticipation🤔</div>
                  </template>
              </v-checkbox>
              <v-checkbox v-model="ex4" color="#ff0080" class="checkbox_padding" value="Optimism" hide-details>
                  <template v-slot:label>
                      <div class="checkbox_button">Optimism🙂</div>
                  </template>
              </v-checkbox>

          </v-checkbox-group>
      </v-col>
        <v-col cols="9">
          <div class='container-chart-circularPacking' ref="circularPacking" style="position: relative;"></div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import * as d3 from 'd3';
//import the data
import topGenres from '../../assets/data/top_genres_perc.json';

export default {
    data() {
      return {
        //store the values that we need to access them in the algorithm
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
        Names : ["Joy", "Love", "Trust", "Fear", "Awe",  "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
        Smileys : ["😀", "😍", "🤗", "😱", "😲", "😢", "😔", "🤢", "😒", "😡", "🤔", "🙂"],
        dataFull : [],
        dataFiltered : [],
        ex4: ['Joy', 'Love', 'Trust', 'Fear', 'Awe', 'Sadness', 'Remorse', 'Disgust', 'Contempt', 'Anger', 'Anticipation', 'Optimism'],

        svg : null,
        Tooltip : null,
        margin : null,
        width : null,
        height : null,
        size : null,
        x : null,
        node : null,
      };
    },
    mounted() {
        //function to create data to be used
        this.create_JSON();
        //function to create the circular packing chart
        this.CreateCircularChart(this.dataFull, this.ex4);
  },

//watcher to detect if emotionsList selected from checkboxes change and update data accordingly
  watch: {
        ex4: {
          handler() {
            this.updateNodes();
          },
          deep: true,
        },
        },

    methods : {
        //to create the data used in the circular packing chart
        create_JSON(){
            //for each emotion
            for (const emotion in topGenres) {
                //not enough data for surprise and submission
                if (emotion != 'surprise' && emotion != 'submission') {
                //for each genre
                for (const i in topGenres[emotion]) {
                    let genre = topGenres[emotion][i].genre;
                    genre = genre.replace(/ /g, '-');
                        //creation of a datapoint
                        let dict = {emotion : emotion.charAt(0).toUpperCase() + emotion.slice(1),
                                    group   : genre.charAt(0).toUpperCase() + genre.slice(1),
                                    percentage   : topGenres[emotion][i].percentage}
                        //push the created datapoint one array
                        this.dataFull.push(dict)
                    }
                }
          }
        },

        updateNodes() {
        let svg = this.svg

        //update data based on emotions selected from checkbox
          this.dataFiltered = this.dataFull.filter(item => this.ex4.includes(item.emotion));
          this.CreateCircularChart(this.dataFiltered, this.ex4)
        },

        //this function creates the circular packing graph
        CreateCircularChart(data, emotions) {
        //remove old svg element if exists
        if (this.svg !== null) {
          this.svg.remove();
        }
        //setup the margin, the width and the height
        this.margin = {top:0, right: 0, bottom: 0, left: 0},
        this.width  = 1000 - this.margin.left - this.margin.right,
        this.height = 800 - this.margin.top - this.margin.bottom,
        //append the svg object to the body of the page
        this.svg = d3.select(this.$refs.circularPacking)
                        .append("svg")
                        .attr("width", this.width + this.margin.left + this.margin.right)
                        .attr("height", this.height + this.margin.top + this.margin.bottom)

        //tooltip when node is selected
        this.Tooltip = d3.select(this.$refs.circularPacking)
                          .append("div")
                          .style("position", "absolute")
                          .style("opacity", 0)
                          .attr("class", "tooltip")
                          .style("background-color", "white")
                          .style("border", "solid")
                          .style("border-width", "2px")
                          .style("border-radius", "5px")
                          .style("padding", "5px")

            //create size scale for the nodes
            this.size = d3.scaleLinear()
                        .domain([0.0,1000.0])
                        .range([10, 1200]);

            //dynamic range and domain for x based on length of emotions selected
            const numbersArray = Array.from({ length: emotions.length }, (_, index) => index + 1);
            const rangeStep = 60 * ((12 - emotions.length)/10 + 1); // Define the step size for each value in the range
            const range = Array.from({ length: emotions.length }, (_, index) => index * rangeStep + 100);

            this.x = d3.scaleOrdinal().domain(numbersArray)
                                      .range(range)

            let size = this.size
            let names = this.Names
            let width = this.width
            let height = this.height
            const color = this.Colors
            let tooltip = this.Tooltip
            let node = this.node
            let svg = this.svg
            let x = this.x

            var mouseover = function(event, d) {
              tooltip
                .style("opacity", 1)
              svg.selectAll(".node_"  + d.emotion + "_" + d.group)
                .attr("opacity", 0.4)
              svg.selectAll(".emoji_" + d.emotion)
                .attr("opacity", 1.0)
              svg.selectAll(".emoji_text_" + d.emotion)
                .attr("opacity", 1.0)
              }


            var mousemove = function(event, d) {
            console.log(window.scrollY)
            console.log(d3.select(this).attr("cy"))
              tooltip
                .html('<u>' + d.group + '</u>' + "<br>" + d.percentage.toFixed(1).toString() + "%")
                .style("left", (d3.select(this).attr("cx")+10) + "px")
                .style("top", (d3.select(this).attr("cy")) + "px")
              }

            var mouseleave = function(event, d) {
              tooltip
                .style("opacity", 0)
              svg.selectAll(".node_"  + d.emotion + "_" + d.group)
                .attr("opacity", 1.0)
              svg.selectAll(".emoji_" + d.emotion)
                .attr("opacity", 0.0)
              svg.selectAll(".emoji_text_" + d.emotion)
                .attr("opacity", 0.0)
              }

            //create nodeGroup inside the svg element
            const nodeGroup = this.svg.append("g")


            node = nodeGroup.selectAll(".node")
                            .data(data).enter()
                            .append("circle")
                              .attr("class", function(d) {
                              return ("node_"  + d.emotion + "_" + d.group)})
                              .attr("r", function(d){
                              return size(d.percentage)})
                              .attr("cx", width / 2)
                              .attr("cy", height / 2)
                              .attr("opacity", "1.0")
                              .style("display", "block")
                              .style("fill", function(d){
                              return color[names.indexOf(d.emotion)]})
                              .style("fill-opacity", 0.8)
                              .attr("stroke", "black")
                              .style("stroke-width", 1)
                              .on("mouseover", mouseover) // What to do when hovered
                              .on("mousemove", mousemove)
                              .on("mouseleave", mouseleave)
                              .call(d3.drag() // call specific function when circle is dragged
                                         .on("start", dragstarted)
                                         .on("drag", dragged)
                                         .on("end", dragended));

            //create a force simulation
            var simulation = d3.forceSimulation()
                                .force("x", d3.forceX().strength(0.1).x( function(d){ return x(d.emotion) } ))
                                .force("y", d3.forceY().strength(0.1).y( height/2 ))
                                .force("center", d3.forceCenter().x(width / 2).y(height / 2)) // Attraction to the center of the svg area
                                .force("charge", d3.forceManyBody().strength(.1)) // Nodes are attracted one each other of value is > 0
                                .force("collide", d3.forceCollide().strength(.1).radius(function(d){ return (size(d.percentage)+5) }).iterations(1)) // Force that avoids circle overlapping
                                .force("attract", forceAttract());

            function forceAttract() {
                        const strength = 0.05; // Strength of attraction
                        const distances = {}; // Object to store distances between circles of the same color

                        // Calculate and store distances between circles of the same color
                        data.forEach(d => {
                          const key = d.emotion;
                          if (!distances[key]) distances[key] = [];
                          distances[key].push(d);
                        });

                        // Custom force function
                        function attract() {
                          data.forEach(d => {
                            const key = d.emotion;
                            const sameColorNodes = distances[key];

                            sameColorNodes.forEach(node => {
                              if (node !== d) {
                                const xDiff = node.x - d.x;
                                const yDiff = node.y - d.y;
                                const distance = Math.sqrt(xDiff * xDiff + yDiff * yDiff);

                                // Apply attraction force towards circles of the same color
                                if (distance > 0) {
                                  const forceX = (xDiff / distance) * strength;
                                  const forceY = (yDiff / distance) * strength;
                                  d.vx += forceX;
                                  d.vy += forceY;
                                }
                              }
                            });
                          });
                        }

                        return attract;
                      }


            // Apply these forces to the nodes and update their positions.
            // Once the force algorithm is happy with positions ('alpha' value is low enough), simulations will stop.
            simulation.nodes(data)
                      .on("tick", function(event, d){
                            node
                              .attr("cx", function(event){ return event.x; })
                              .attr("cy", function(event){ return event.y; });

            //add genre names text to nodes
            textGroup.selectAll(".genre-text")
                              .attr("x", function(d) { return d.x; })
                              .attr("y", function(d) { return d.y; });

                            }).alpha(1)
                            .restart();

            // What happens when a circle is dragged?
            function dragstarted(event, d) {
                    if (!event.active) simulation.alphaTarget(.03).restart();
                              d.fx = d.x;
                              d.fy = d.y;
                              }

            function dragged(event, d) {
                            // Get the current position of the dragged node
                            const newX = event.x;
                            const newY = event.y;

                            // Get the radius of the node
                            const nodeRadius = size(d.percentage);

                            // Calculate the minimum and maximum allowed positions
                            const minX = nodeRadius;
                            const minY = nodeRadius;
                            const maxX = width - nodeRadius;
                            const maxY = height - nodeRadius;

                            // Restrict the position within the boundaries
                            d.fx = Math.max(minX, Math.min(maxX, newX));
                            d.fy = Math.max(minY, Math.min(maxY, newY));
                              }

            function dragended(event, d) {
                              if (!event.active) simulation.alphaTarget(.03);
                              d.fx = null;
                              d.fy = null;
                              }

            // Create a group for text elements
            var textGroup = this.svg.append("g")
                                .attr("class", "text-group")


            // Add genre name text
            textGroup.selectAll(".genre-text")
                .data(data)
                .enter()
                .append("text")
                  .attr("class", "genre-text")
                  .text(function(d) { return d.group; })
                  .style("text-anchor", "middle")
                  .style("font-size", function(d) { return Math.min(0.22 * size(d.percentage), 24) + "px"; })
                  .attr("fill", "white")
                  .attr("font-family", "Poppins")
                  .style("pointer-events", "none")
                  .style("display", "block")

        },

    },
}

</script>

<style>
    .this.node:hover{
      stroke-width: 7px !important;
      opacity: 1 !important;
      }
      .tooltip {
        position: absolute;
      }
</style>

<style scoped>
   .checkbox_button{
       color: white;
       font-family: "Poppins";
       font-size: "18px";
   }
   .checkbox_padding{
       padding-top: 10px;
       padding-bottom: 10px;
   }
   </style>
