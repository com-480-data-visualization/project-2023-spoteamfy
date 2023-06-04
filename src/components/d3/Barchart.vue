<template>

    <v-container fill-height fluid>
        <div style="flex:auto;margin-top: 50px;margin-bottom: 100px"> 
                <v-row align="center" justify="center">
                    <v-col cols="9">
                        <p style="color: white;">
                            Hold on !<br>
                            At this point, you might have one emotion that stands out more than the others ! Isn't it ? <br>
                            Good for you ! We have a nice tool to understand why you are attracted by such an emotion... <br>
                            This nice tool compares the different music features accoss all the emotions. <br><br>
                            Feel free to press on the <b style="color: red;">buttons</b> to see the features of your favorite emotion compared to the others.<br>
                            <br>
                            <b>Note for the more experienced adventurer : </b> <br> 
                            This tool is created by doing a min-max normalization of the features that we transform into percent.
                            The height of a bar represents a mean value and the interval on it gives an idea of its confidence interval.
                        </p>
                    </v-col>
                    <v-col cols="3">
                        <v-img :src="groot_pressing" style="border-radius: 30px;"></v-img> 
                    </v-col>
                </v-row>
        </div>
    
        <div style="flex:auto"  class="barchart">
                <v-row align="center" justify="center">
                    <v-col cols="3">
                        <v-radio-group>
                            <v-radio @click ="updateBarChart(arousal, 'arousal')" class="radio_padding" value="1">
                                <template v-slot:label>
                                    <div class="radio_button">Arousal</div>
                                </template>
                            </v-radio>
                            <v-radio @click ="updateBarChart(dominance, 'dominance')" class="radio_padding" value="2">
                                <template v-slot:label>
                                    <div class="radio_button">Dominance</div>
                                </template>
                            </v-radio>
                            <v-radio @click ="updateBarChart(acousticness, 'acousticness')" class="radio_padding" value="3">
                                <template v-slot:label>
                                    <div class="radio_button">Acousticness</div>
                                </template>
                            </v-radio>
                            <v-radio @click ="updateBarChart(danceability, 'danceability')" class="radio_padding" value="4">
                                <template v-slot:label>
                                    <div class="radio_button">Danceability</div>
                                </template>
                            </v-radio>
                            <v-radio @click ="updateBarChart(valence, 'valence')" class="radio_padding" value="5">
                                <template v-slot:label>
                                    <div class="radio_button">Valence</div>
                                </template>
                            </v-radio>
                            <v-radio @click ="updateBarChart(loudness, 'loudness')" class="radio_padding" value="6">
                                <template v-slot:label>
                                    <div class="radio_button">Loudness</div>
                                </template>
                            </v-radio>
                            <v-radio @click ="updateBarChart(energy, 'energy')" class="radio_padding" value="7">
                                <template v-slot:label>
                                    <div class="radio_button">Energy</div>
                                </template>
                            </v-radio>
                            <v-radio @click ="dancingGroot" class="radio_padding" value="8">
                                <template v-slot:label>
                                    <div class="radio_button">Grootness</div>
                                </template>
                            </v-radio>
                        </v-radio-group>
                    </v-col>
                    <v-col cols="9">
                        <div class='container-barchart' ref="bar_chart" style="position: relative;">
                            <v-img :src="dancing_groot" style="height: 300px;width: 300px; position: absolute;top: 150px; left: 300px; border-radius: 10px;" v-if='showImage'></v-img> 
                        </div>
                    </v-col> 
                </v-row>
        </div>
        </v-container>
    </template>
    
    <script>
    import * as d3 from 'd3';
    //import the datas
    import means from '../../assets/data/features_stat_by_emotions.json';
    import dancing_groot from "../../assets/data/dancing_groot_dam.gif";
    import groot_pressing from "../../assets/data/groot_pressing.gif";

    export default {
        data() {
          return {
            //store the values that we need to access them in the algorithm
            Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
            Names : ["Joy", "Love", "Trust", "Fear", "Awe",  "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
            Smileys : ["😀", "😍", "🤗", "😱", "😲", "😢", "😔", "🤢", "😒", "😡", "🤔", "🙂"],
            tempo : [],
            arousal : [],
            dominance : [], 
            acousticness : [],
            danceability : [],
            energy : [],
            speechiness : [],
            loudness : [],
            liveness : [],
            valence : [],
            showImage : false,
            dancing_groot : dancing_groot,
            groot_pressing : groot_pressing,
            
            svg : null, 
            margin : null,
            width : null,
            height : null,
            x : null,
            y : null,
            xAxis : null,
            yAxis : null,
            state : null,
            descriptions:
            {   "danceability" : "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. ",
                "energy" : "Energy represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.",
                "instrumentalness" : "Instrumentalness predicts whether a track contains no vocals. Values above 50% are intended to represent instrumental tracks, but confidence is higher as the value approaches 100%.",
                "acousticness" : "Acousticness measures how a song sounds acoustic or natural, as opposed to electronic or synthesized. Higher values suggest a more organic sound, while lower values indicate a more digitally produced one.",
                "valence" : "Valence describes the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
                "arousal" : "Arousal refers to the level of physiological and psychological stimulation that a listener experiences while listening to music. It is often associated with the emotional intensity that a piece of music generates.",
                "dominance" : "Dominance refers to the sense of power conveyed by the music. In general, music that is perceived as more dominant tends to be more stimulating and exciting, while music that is less dominant may be more relaxing or soothing.",
                "loudness" : "The overall loudness of a track. Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength.",
                "grootness" : "🔥Ablility to be adorable and to be the cuuuuuuuuuuuuuuuuutest thing of the galaxy🔥",
            }
          };
        },
        mounted() {
            this.create_JSON();
            this.CreateBarChart();
            const rect = this.svg
            //show the bar height in percent and remove the CI when mouseovering on a specific bar
            rect.selectAll("rect").on("mouseover", function(d, i) {
                
                //reduce opacity of the bar
                d3.select(this)
                    .transition()
                    .duration('100')
                    .attr('opacity', '.5');
                //plot the corresponding emoji
                rect.selectAll(".emoji_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '1.0');
                //plot the value in percent
                rect.selectAll(".means_text_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '1.0');
                //hide the CI composed by one line, one point and two small lines.
                rect.selectAll(".error_points_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '0.0');
                
                rect.selectAll(".error_lines_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '0.0');
                
                rect.selectAll(".error_up_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '0.0');
                
                rect.selectAll(".error_down_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '0.0');
                })
            //show the bar and its CI when mouseouting on a specific bar
            rect.selectAll("rect").on("mouseout", function(d, i) {
                //show the bar
                d3.select(this)
                    .transition()
                    .duration('100')
                    .attr('opacity', '1.0');
                //hide the emoji
                rect.selectAll(".emoji_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '0.0');
                //hide the value
                rect.selectAll(".means_text_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '0.0');
                //show the CI composed by one line, one point and two small lines
                rect.selectAll(".error_points_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '1.0');
                
                rect.selectAll(".error_lines_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '1.0');
                
                rect.selectAll(".error_up_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '1.0');
                
                rect.selectAll(".error_down_" + i.group)
                    .transition()
                    .duration('100')
                    .attr('opacity', '1.0');
            })
        },
        methods : {
            //to create the data used in the barchart
            create_JSON(){
                //for each feature
                for (const feature in means) {
                    //for each emotion
                    for (const emotion in means[feature]) {
                        //not enough datas for surprise and submission
                        if (emotion != 'surprise' && emotion != 'submission') {
                            
                            //creation of a datapoint
                            let dict = {group   : emotion.charAt(0).toUpperCase() + emotion.slice(1), 
                                        value   : means[feature][emotion]['mean'],
                                        IC_low  : means[feature][emotion]['IC_low'], 
                                        IC_high : means[feature][emotion]['IC_high']}
                            //push the created datapoint into the corresponding array
                            if (feature == 'tempo') {
                                this.tempo.push(dict)
                            }
                            if (feature == 'valence') {
                                this.valence.push(dict)
                            }
                            if (feature == 'arousal') {
                                this.arousal.push(dict)
                            }
                            if (feature == 'dominance') {
                                this.dominance.push(dict)
                            }
                            if (feature == 'acousticness') {
                                this.acousticness.push(dict)
                            }
                            if (feature == 'danceability') {
                                this.danceability.push(dict)
                            }
                            if (feature == 'liveness') {
                                this.liveness.push(dict)
                            }
                            if (feature == 'loudness') {
                                this.loudness.push(dict)
                            }
                            if (feature == 'speechiness') {
                                this.speechiness.push(dict)
                            }
                            if (feature == 'energy') {
                                this.energy.push(dict)
                            }
                        }
                    }
                }
            },
            //this function creates the skeleton of the svg graph
            CreateBarChart() {
                //setup the margin, the width and the height
                this.margin = {top:150, right: 30, bottom: 150, left: 60},
                this.width  = 900 - this.margin.left - this.margin.right,
                this.height = 650 - this.margin.top - this.margin.bottom,
                //append the svg object to the body of the page
                this.svg = d3.select(this.$refs.bar_chart)
                                .append("svg")
                                .attr("width", this.width + this.margin.left + this.margin.right)
                                .attr("height", this.height + this.margin.top + this.margin.bottom)
                                    .append("g")
                                    .attr("transform","translate(" + this.margin.left + "," + this.margin.top + ")");
                //create X axis
                this.x = d3.scaleBand()
                            .range([ 0, this.width ])
                            .padding(0.2);
                this.xAxis = this.svg
                            .append("g")
                            .attr("transform", "translate(0," + this.height + ")")
                
                //create Y axis
                this.y = d3.scaleLinear()
                            .range([this.height, 0]);
                this.yAxis = this.svg
                            .append("g")
                            .attr("class", "barchart_axis")
                
                //plot the unit on the y axis
                this.svg.append("text")
                        .attr("class", "y_unit")
                        .text("[%]")
                        .style("font-size", "15px")
                        .style("text-anchor", "middle")
                        .attr("font-family", "Poppins")
                        .attr("x", -50)
                        .attr("y", 180)
                        .attr("opacity", 0)
                        .style('fill', 'white')
                //object used to plot the name of the displayed feature
                this.svg.append("text")
                        .attr("class", "feature_name")
                        .attr("x", 0)
                        .attr("y", -50)
                        .style("font-size", "45px")
                        .style('fill', 'white')
                
                //object used to plot the description of the feature
                this.svg.append("foreignObject")
                        .attr("width", 550)
                        .attr("height", 100)
                        .attr("x", 0)
                        .attr("y", -93)
                            .append("xhtml:div")
                                .append("p")
                                .attr("class", "feature_description")
                                .style("line-height", "1.5em")
                                .style("font-size", "12px")
                                .style("border-radius", "3px")
                                .style("color", "white")
                                .style("padding", "8px 8px 8px 8px")
                                .style("border-width", "1px")
                                .style("border-style", "solid")
                                .style("border-color", "#FFFFFF")
                
                //update the barchart using arousal as default feature
                this.updateBarChart(this.arousal, 'arousal')
            },
            
            //function used to set the feature as title name of the chart followed by its description
            //we also update the y unit 
            addTitle(name) {
                //do fancy transition for the unit value
                this.svg.select(".y_unit")
                        .transition()
                        .duration(300)
                        .attr("opacity", 0)
                        .transition()
                        .duration(300)
                        .attr("opacity", 1)
                //update the feature description and do a fancy transition
                this.svg.select(".feature_description")
                        .transition()
                        .duration(300)
                        .style("opacity", 0)
                        .transition()
                        .duration(300)
                        .text(this.descriptions[name])
                        .style("opacity", 1)
                //update the feature name and do a fancy transition
                this.svg.select(".feature_name")
                        .transition()
                        .duration(300)
                        .attr("y", -115)
                        .style("opacity", 0)
                        .transition()
                        .duration(300)
                        .text(name.charAt(0).toUpperCase() + name.slice(1) + ".")
                        .style("opacity", 1)
            },
            //fancy function when pressing on the grootness feature
            dancingGroot() {
                //update the feature title 
                this.addTitle("grootness");
                //show the .gif
                this.showImage = true;
                //change the color bar into pink
                this.svg.selectAll("rect")
                        .transition()
                        .duration(300)
                        .attr("fill", "#FFC0CB")
            },
            //this function is used to update the value (with transitions) displayed on the barchart
            updateBarChart(data, name) {
                //let define the values used in this function
                let max = d3.max(data, d => d.IC_high);
                let min = d3.min(data, d => d.IC_low);
                let delta = (max - min) * 0.1
                let x = this.x
                let y = this.y
                let Colors = this.Colors
                let Names  = this.Names
                let Smileys = this.Smileys
                let height = this.height
                let width  = this.width
                //remove the .gif when updating the barchart
                this.showImage = false;
                //update the feature title, the y unit and the feature description
                this.addTitle(name)
                //UPDATE THE X AXIS
                this.x
                    .domain(data.map(function(d) { return d.group; }))
                this.xAxis
                    .transition()
                    .duration(1000)
                    .style('color', 'white')
                    .call(d3.axisBottom(this.x))
                        .selectAll("text")
                        .style("text-anchor", "end")
                        .attr("font-family", "Poppins")
                        .style("font-size", "18px")
                        .attr("dx", "-.90em")
                        .attr("dy", ".12em")
                        .attr("transform", "rotate(-65)");
                //UPDATE THE Y AXIS
                this.y.domain([min - delta , max + delta])
                this.yAxis
                    .transition()
                    .duration(1000)
                    .style('color', 'white')
                    .call(d3.axisLeft(this.y))
                        .selectAll("text")
                        .attr("font-family", "Poppins")
                        .style("font-size", "18px")
                //UPDATE THE BARS
                let bars = this.svg.selectAll("rect").data(data)
                bars.enter()
                    .append('rect')
                    .merge(bars)
                    .transition().duration(1000)
                    .attr("x", function(d) { return x(d.group); })
                    .attr("y", function(d) { return y(d.value); })
                    .attr("width", x.bandwidth())
                    .attr("height", function(d) { return height - y(d.value); })
                    .attr("fill", function(d) {return Colors[Names.indexOf(d.group)];})
                
                bars.exit().remove()
                
                //UPDATE THE EMOJIS
                let emojis = this.svg.selectAll(".emoji").data(data)
                
                emojis.enter()
                    .append('text')
                    .merge(emojis)
                    .transition()
                    .duration(1000)
                    .text(function(d) { return Smileys[Names.indexOf(d.group)]; })
                    .attr("class", function(d) {return "emoji" + " " + "emoji_" + d.group})
                    .attr("x", width)
                    .attr("dx", -120)
                    .attr("y", 20)
                    .attr("dy", 0)
                    .attr("font-size" , "80px")
                    .attr('opacity', '0.0')
                emojis.exit().remove()
                
                //UPDATE THE MEANS VALUE TEXT (when mouseovering it on the bars)
                let means_text = this.svg.selectAll(".means_text").data(data)
                
                means_text.enter()
                    .append('text')
                    .merge(means_text)
                    .transition()
                    .duration(1000)
                    .text(function(d) { return d.value.toFixed(1).toString() + "%"; })
                    .attr("class", function(d) {return "means_text" + " " + "means_text_" + d.group})
                    .style("text-anchor", "middle")
                    .attr("x", function(d) {return x(d.group);})
                    .attr("dx", x.bandwidth() / 2.0)
                    .attr("y", function(d){return y(d.value);})
                    .attr("dy", - 10)
                    .attr("font-size" , "15px")
                    .attr("fill", "white")
                    .attr("font-family", "Poppins")
                    .attr('opacity', '0.0')
                means_text.exit().remove()
                //UPDATING OF THE CONFIDENCE INTERVAL
                //update the position of the points (points)
                //update the position of the error vertical lines for the CI (error_lines)
                //update the position of the two small horizontal lines for the CI (small_error_lines)
                let small_error_lines_up   = this.svg.selectAll(".error_up").data(data)
                let small_error_lines_down = this.svg.selectAll(".error_down").data(data)
                let error_lines            = this.svg.selectAll(".error_lines").data(data)
                let points                 = this.svg.selectAll(".error_points").data(data)
                points.enter()
                    .append('circle')
                    .merge(points)
                    .transition()
                    .duration(1000)
                    .attr("class", function(d) {return "error_points" + " " + "error_points_" + d.group})
                    .attr("cx", function(d) {return x(d.group) + x.bandwidth()/2.0;})
                    .attr("cy", function(d){return y(d.value);})
                    .attr('r', 2)
                    .attr("fill", "white")
                    .attr('opacity', '1.0')
                error_lines
                    .enter()
                    .append('line')
                    .merge(error_lines)
                    .transition()
                    .duration(1000)
                    .attr("class", function(d) {return "error_lines" + " " + "error_lines_" + d.group})
                    .attr("x1", function(d) {return x(d.group) + x.bandwidth()/2.0;})
                    .attr("y1", function(d){return y(d.IC_high) ;})
                    .attr("x2", function(d) {return x(d.group) + x.bandwidth()/2.0;})
                    .attr("y2", function(d){return y(d.IC_low) ;})
                    .style("stroke", "white")
                    .style("stroke-width", 25)
                    .attr('opacity', '1.0')
                small_error_lines_up
                    .enter()
                    .append('line')
                    .merge(small_error_lines_up)
                    .transition()
                    .duration(1000)
                    .attr("class", function(d) {return "error_up" + " " + "error_up_" + d.group})
                    .attr("x1", function(d) {return x(d.group) + x.bandwidth()/2.0 - 5;})
                    .attr("y1", function(d){return y(d.IC_high) ;})
                    .attr("x2", function(d) {return x(d.group) + x.bandwidth()/2.0 + 5;})
                    .attr("y2", function(d){return y(d.IC_high) ;})
                    .style("stroke", "white")
                    .style("stroke-width", 25)
                    .attr('opacity', '1.0')
                small_error_lines_down
                    .enter()
                    .append('line')
                    .merge(small_error_lines_down)
                    .transition()
                    .duration(1000)
                    .attr("class", function(d) {return "error_down" + " " + "error_down_" + d.group})
                    .attr("x1", function(d) {return x(d.group) + x.bandwidth()/2.0 - 5;})
                    .attr("y1", function(d){return y(d.IC_low) ;})
                    .attr("x2", function(d) {return x(d.group) + x.bandwidth()/2.0 + 5;})
                    .attr("y2", function(d){return y(d.IC_low) ;})
                    .style("stroke", "white")
                    .style("stroke-width", 25)
                    .attr('opacity', '1.0')
                
                points.exit().remove()
                error_lines.exit().remove()
                small_error_lines_down.exit().remove()
                small_error_lines_up.exit().remove()
            },
        },
    }
    </script>
    
    <style scoped>
    .radio_button{
        color: white;
        font-family: "Poppins";
        font-size: "18px";
    }
    .radio_padding{
        padding-top: 10px;
        padding-bottom: 10px;
    }
    </style>