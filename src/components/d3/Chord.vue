<!-- SECTION 1 - CHORD DIAGRAM -->
<template>
    <v-row align="center">

      <v-col cols="4">
        <v-container :style="{position:relative}">

          <!-- If user has not clicked on one emotion  -->
          <transition mode="out-in">
            <v-card v-if="!clicked_emotion" class="infosLinks" color="#191919" :style="{borderColor: '#f9004d'}" key="card1">

              <!-- Text -->
              <v-card-title>
                  <h3 class="fontWeight500" text style="color: #f9004d;"> Emotional Jukebox </h3>
                  <svg-icon class="icon" type="mdi" :path="path"></svg-icon>
              </v-card-title>

              <v-card-text>
                <p text-align="center" style="color: white;">Discover Music Links by clicking on your Mood.</p>
                <v-img :src="grootDJ"> </v-img> 
              </v-card-text>

            </v-card>

            <!-- If user has clicked on one emotion  -->
            <v-card v-else class="infosLinks" color="#191919" :style="{ borderColor: color_source }" key="card2">
              <!-- Chart -->
              <lollipop/>
            </v-card>

          </transition>
        </v-container>
      </v-col>

      <!-- Chord diagram -->
      <v-col cols="8">
        <div class='container-chart' ref="chart"></div>
      </v-col>
    </v-row>
</template>
  
<script>
  import * as d3 from 'd3';
  import SvgIcon from '@jamescoyle/vue-icon';
  import { mdiMusicCircle } from '@mdi/js';
  import grootDJ from "../../assets/data/grootHey.gif";


  //Import components
  import lollipop from './lollipop.vue';
  import musicReader from './musicReader.vue';
  import Features from './Features.vue';
  import Genres from './Genres.vue';
  import Artists from './Artists.vue';
  import WordCloud from './wordCloud.vue';


  export default {
    components: {
      SvgIcon,
      musicReader,
      Features,
      Genres,
      Artists,
      WordCloud,
      lollipop
    },

    data() {
      return {
        //Images
        path : mdiMusicCircle,
        grootDJ : grootDJ,

        //If user has clicked on one emotion
        clicked_emotion : false,

        //When user hover an emotion, set these values
        targets : [],
        index_source: null,
        name_source : null,
        color_source : null,

        Names : ["Joy", "Love", "Trust", "Fear", "Awe", "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
        Smileys : ["😀", "😍", "🤗", "😱", "😲", "😢", "😔", "🤢", "😒", "😡", "🤔", "🙂"],

        emotion2Smiley : {
          "Joy": "😀",
          "Love": "😍",
          "Trust": "🤗",
          "Fear": "😱",
          "Awe": "😲",
          "Surprise": "😮",
          "Sadness": "😢",
          "Remorse": "😔",
          "Disgust": "🤢",
          "Contempt": "😒",
          "Anger": "😡",
          "Anticipation": "🤔",
          "Optimism": "🙂"
        },

        //Symetric matrix of emotions
        matrix :        [[8270, 2391, 952, 2636, 26,  16871, 1302, 159, 2692, 166, 17, 16814], //joy
                        [2391, 2332, 439, 2399, 22,  12716, 1065, 71, 952, 95, 13, 6808], //love
                        [952, 439, 400, 496, 2, 3148, 237, 32, 401, 31, 5, 2248], //trust
                        [2636, 2399, 496, 10772, 45,  20127, 2597, 72, 1023, 86, 15, 6696], //fear
                        [26, 22, 2, 45, 0,  151, 15, 1, 8, 3, 0, 74], //awe
                        [16871, 12716, 3148, 20127, 151, 111220, 7814, 533, 8982, 730, 50, 44483], //sadness
                        [1302, 1065, 237, 2597, 15,  7814, 1558, 50, 390, 45, 17, 3380], //remorse
                        [159, 71, 32, 72, 1,  533, 50, 20, 80, 9, 0, 478], //disgust
                        [2692, 952, 401, 1023, 8,  8982, 390, 80, 3558, 267, 7, 7215], //contempt
                        [166, 95, 31, 86, 3,  730, 45, 9, 267, 48, 2, 450], //anger
                        [17, 13, 5, 15, 0,  50, 17, 0, 7, 2, 6, 39], //anticipation
                        [16814, 6808, 2248, 6696, 74,  44483, 3380, 478, 7215, 450, 39, 53302] //optimism
                        ]
      };
    },

    mounted() {
      this.createChord();
    }, 

    methods : {
      createChord() {
        //Set up the svg
        const radius = 260; //300
        const innerRadius = 280; //320
        const outerRadius = 300; //340
        const label_margin = 10;

        //Retrieve data 
        const matrix = this.matrix;
        const Names = this.Names;
        const Colors = this.Colors;
        const Smileys = this.Smileys;

        //Create the svg 
        const svg = d3.select(this.$refs.chart)
          .append('svg')
            .attr('width', 800)
            .attr('height', 800)
            .attr('class', 'svg-style')
          .append("g")
            .attr("transform", "translate(400,400)");
        
        //Set color scale
        const colors = d3.scaleLinear()
          .domain(d3.range(Names.length))
          .range(Colors);

        //Create chord layout  
        const chord = d3.chord()
          .padAngle(0.05)     // padding between entities 
          .sortSubgroups(d3.descending)
          (matrix)

        // Add the links between groups
        let ribbon = svg
          .datum(chord)
          .append("g")
          .selectAll("path")
          .data(function(d) { return d; })
          .enter()
          .append("path")
            .attr("d", d3.ribbon()
              .radius(radius)    //Size of inner circle
            )
            .attr("class", "ribbon")
            .style("opacity", 0.8)
            .style("stroke", function(d,i) { //fill with linear gradient
              const url = "url(#linear-gradient-" + d.source.index +"-"+d.target.index + ")";
              return url;
            })
            .style("fill", function(d,i) { 
              const url = "url(#linear-gradient-" + d.source.index +"-"+d.target.index + ")";
              return url;
            })
          
        //Retrieve groups
        let group = svg
          .datum(chord)
          .append("g")
          .selectAll("g")
          .data(function(d) { 
            return d.groups; 
          })
          .enter()

        //Add the group arc (pie chart)
        group.append("g")
          .append("path")
          .style("fill", function(d,i) {return colors(i);})
          .style("stroke", function(d,i) {return colors(i);})
          .attr("d", d3.arc()
            .innerRadius(innerRadius)    // This is the size of the donut (inner)
            .outerRadius(outerRadius)    // This is the size of the donut (outer)
          )
          .style('cursor', 'pointer')
          .on("click", function(event, d) {
            clickEmotion(event, d);
          });
          
        //Set the color for each ribbon
        ribbon.each(function(d){
          //Create a unique id
          const gradient_id = "linear-gradient-" + d.source.index +"-"+d.target.index;

          //Create the gradient
          const gradient = svg.append("defs")
            .append("linearGradient")
            .attr("id", gradient_id)
            .attr("gradientUnits", "userSpaceOnUse")
            .attr("x1", function() { 
              return Math.cos((d.source.startAngle + d.source.endAngle) / 2 - Math.PI / 2) * radius; })
            .attr("y1", function() {
              return Math.sin((d.source.startAngle + d.source.endAngle) / 2 - Math.PI / 2) * radius; })
            .attr("x2", function() {
              return Math.cos((d.target.startAngle + d.target.endAngle) / 2 - Math.PI / 2) * radius; })
            .attr("y2", function() {
              return Math.sin((d.target.startAngle + d.target.endAngle) / 2 - Math.PI / 2) * radius; })
          //Set the gradient
          gradient.append("stop")
            .attr("offset", "0%")
            .attr("stop-color", colors(d.source.index))
          gradient.append("stop")
            .attr("offset", "100%")
            .attr("stop-color", colors(d.target.index))
          //Fill the ribbon with the gradient
          d3.select(this).style("fill", "url(#" + gradient_id + ")");
        });

        //Add the group labels
        group.append("text")
          .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })  //retrieve the angle of the middle of the arc
          .attr("dy", ".35em")  //y alignment
          .attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : "start"; }) //x alignment
          .attr("transform", function(d) {
            //*180/pi to convert radian to degree
            //Starts at 12 o'clock and goes counterclockwise
            //First go to 0, then rotate the angle, then translate to the outer radius
            return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
                + "translate(" + (outerRadius + label_margin) + ")"
                + (d.angle > Math.PI ? "rotate(180)" : "");
          })
          .text(function(d, i) { return Names[i]; })
          .style("fill", "white")
          .style("font-size", '15px')
          .style('cursor', 'pointer')
          .on("click", function(event, d) {
            clickEmotion(event, d);
          })

        //When user click on a group      
        const clickEmotion = (event, d) => {
            //Retrieve the index of the emotion
            const index_source = d3.select(event.currentTarget).datum().index;

            if (this.clicked_emotion == false || this.index_source != index_source) {
              inEmotion(event, d);  //Show data about emotion
            } else {
              outEmotion(event, d); //Reset original data
            }
          }

          //When user selects one emotion
          const inEmotion = (event, d) => {
            //Retrieve the index of the emotion
            const index_source = d3.select(event.currentTarget).datum().index;

            //Set the hover variable to true 
            this.clicked_emotion = true;
            this.$store.commit('setClickedEmotion', true);

            //Update the vuex store
            this.$store.commit('setIndex', index_source);

            //Set the source informations
            this.name_source = Names[index_source];
            this.color_source = Colors[index_source];
            this.index_source = index_source;
            const total_source = matrix[index_source].reduce((a, b) => a + b, 0);

            //Set the target informations
            let targets = [];
            const values = matrix[index_source];

            for (let i = 0; i < values.length; i++) {
              if (values[i] != 0) {
                const target = {
                  name: Names[i],
                  percent: Math.round((values[i] / total_source) * 100),
                  color: Colors[i],
                  smiley : Smileys[i]
                }
                if (target.percent > 0) {
                  targets.push(target);
                }
              }
            }

            //Order by percent from largest to mallest 
            targets.sort((a, b) => (a.percent < b.percent) ? 1 : -1);
            this.targets = targets;

            //Now, retrieve all paths and two options : 
            // - set color to black only if the index is not the current emotion (for pie chart)
            // - set color to black only if the index is the source emotion of the ribbon
            const paths = svg.selectAll("path");
            paths.style("fill", function(d) {
              if (d.index != index_source ) {
                return "black";
              }
              else {
                return Colors[index_source];
              }
            });

            //Retrieve all texts and set color to Colors[index_source] only if the index is the current emotion
            const texts = svg.selectAll("text");
            texts.style("fill", function(d) {
              if (d.index == index_source ) {
                return Colors[index_source];
              }
              else {
                return "white";
              }
            });

            // retrieve the ribbons of the chord diagram
            const ribbons = svg.selectAll(".ribbon");
            //Set the color of the ribbons
            ribbons.style("fill", function(d) {
              if (d.source.index != index_source && d.target.index != index_source) {
                return "black";
              }
              else {
                return "url(#linear-gradient-" + d.source.index +"-"+d.target.index + ")";
              }
            });
            //Set the color of strokes
            ribbons.style("stroke", function(d) {
              if (d.source.index != index_source && d.target.index != index_source) {
                return "black";
              }
              else {
                return "url(#linear-gradient-" + d.source.index +"-"+d.target.index + ")";
              }
            });
            //Change opacity
            ribbons.style("opacity", function(d) {
              if (d.source.index != index_source && d.target.index != index_source) {
                return 0.1;
              }
              else {
                return 0.9;
              }
            });
          };

          //Reset initial layout 
          const outEmotion = (event, d) => {
            //Set the hover variable to false 
            this.clicked_emotion = false;
            this.$store.commit('setClickedEmotion', false);

            //Retrieve all paths 
            const paths = svg.selectAll("path");
            paths.style("fill", function(d) {
              return Colors[d.index];
            });

            //Retrieve all texts 
            const texts = svg.selectAll("text");
            texts.style("fill", function(d) {
                return "white";
            });

            //Retrieve the ribbons of the chord diagram
            const ribbons = svg.selectAll(".ribbon");
            //Set the color of the ribbons
            ribbons.style("fill", function(d) {
              return "url(#linear-gradient-" + d.source.index +"-"+d.target.index + ")";
            });
            //Set the color of strokes
            ribbons.style("stroke", function(d) {
              return "url(#linear-gradient-" + d.source.index +"-"+d.target.index + ")";
            });
            //Change opacity
            ribbons.style("opacity", function(d) {
            return 0.8;
            });
          };
        }
    }
  }
</script>

<style>

.container-chart {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    
  }
  
  svg {
    display: flex;
    justify-content: center;
    align-items: center;
  }

.infosLinks {
  display: flex;

  justify-content: center;
  align-content: center;
  align-items: center;
  flex-direction: column;

  margin-top: 175px;
  margin-bottom: 175px;

  width: 450px;
  height: 650px;

  border-width: 2px;  
  border-style: solid;
  border-color:#f9004d;
}

.icon {
  margin-top: -11px;
  margin-left: 10px;
  fill: #f9004d;
}

path[data-v-8dea8908] {
  fill: #f9004d;
}

.icon2 {
  margin-top: -11px;
  margin-left: 10px;
}

.infosEmotion {
  max-width: 1500px;
  background-color: #191919;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>

  