<!-- SECTION 2 - TOP 10 ARTISTS -->
<template>
        <v-container fill-height fluid>
            <v-row align="center" justify="center">

                <!-- Chart -->
                <v-col cols="8">
                    <div class='container-chart-artists' ref="chart"></div>
                </v-col>

                <!-- Bio -->
                <v-col cols="4">
                    <v-card elevation="25" class="bio-artists" v-if="isArtistSelected">
                        <v-card-title class="title-bio" style="color:white">
                            About &nbsp;<span :style="{color:color}"> {{ artist_name }} </span>
                        </v-card-title>
                        <v-card-text class="text-bio" >
                            <p style="color:white; font-size:15px; font-weight:lighter">
                                <span :style="{color:color}">Number of tracks : </span>
                                 {{ nb_tracks }}                         
                            </p>
                            <br/>
                            <p style="color:white; font-size:15px; font-weight:lighter">
                                <span :style="{color:color}">Biography : </span>                            
                                {{bio}}
                            </p>
                        </v-card-text>
                    </v-card>

                    <v-card elevation="25" class="bio-artists" v-else>
                        <v-card-text class="text-bio" >
                            <div class="groot">
                                <v-img :src="logoGroot" width="100"></v-img>
                            </div>                            
                            <p style="color:white; font-size:15px; font-weight:lighter">
                                Discover the top 10 artists whose tracks are most prevalent in {{name}}. 
                                The size of each circle is proportional to the number of tracks included in the {{name}} playlist.
                                <br/><br/>
                                💡Hover your mouse over one picture to discover insights about each artist!
                            </p>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
</template>

<script>
import * as d3 from 'd3';
import artists from '../../assets/data/top_artists.json';
import logoGroot from '../../assets/data/groot-vignette.png';

export default {

    data() {
      return {
        logoGroot : logoGroot,
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00",  "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
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
        nb_tracks : 0,
        bio : "Sorry, no biography available.",
        artist_name : "",
        isArtistSelected : false,
     };
    },

    computed: {
        index() {
            return this.$store.state.index;
        },
        color() {
            return this.Colors[this.index];
        },
        name() {
            return this.Names[this.index].toLowerCase();
        },
        myArtists () {
            return artists[this.name];
        }, 
    },

    mounted (){
        this.updateArtists();
    },

    watch: {
        index() {
            this.updateArtists();
        }
    },

    methods: {
        updateArtists() {
            //Set width and height
            const width = 750;
            const height = 750;

            //Retrieve data 
            let data = this.myArtists;
            //Retrieve color
            const color = this.color;

            //Select the existing svg element or create a new one if it does not exist yet
            let svg = d3.select(this.$refs.chart).select("svg#my-artists");
            if (svg.empty()) {
                svg = d3.select(this.$refs.chart).append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("id", "my-artists")
            }

            //Remove previous data
            svg.selectAll("g").remove();

            //Create a hierarchy from the data
            const root = d3.hierarchy({name:"root", size:"0", children: data })
                .sum(d => d.size);

            //Compute layout
            const pack = d3.pack()
                .size([750, 750])
                .padding(15);
            pack(root);

            //Retrieve the descendents 
            const descendants = root.descendants();

            //Create a group for each node (only the leaf nodes will have a group)
            const smallNodes = descendants.filter(d => !d.children);

            const node = svg.selectAll('.node')
                .data(descendants)
                    .enter()
                        .append('g')
                        .attr('class', 'node');

            //Retrieve only leaf nodes
            const leafNodes = node.filter(d => !d.children);

            //Create a circle for each node
            node.append('circle')
                .attr('r', d => d.r)
                .attr('cx', d => d.x)
                .attr('cy', d => d.y)
                .attr('fill', d => {
                    if (d.data.name == "root") {
                        return "#191919";
                    }
                    else {
                        return color;
                    }
                })
            
            //Create a clip path for each node
            svg.append('defs')
                .selectAll('.clip')
                .data(smallNodes)
                    .enter()
                        .append('clipPath')
                        .attr('id', d => `clip-${d.data.track_id}`)
                        .append('circle')
                            .attr('r', d => d.r)
                            .attr('cx', d => d.x)
                            .attr('cy', d => d.y);
            
            leafNodes.each( function(d) {
                //Retrieve the current node
                const currentNode = d3.select(this);

                //Add image to each node
                currentNode.append('image')
                    .attr('x', d => d.x - d.r)
                    .attr('y', d => d.y - d.r)
                    //Resize the image to fit the circle
                    .attr('preserveAspectRatio', 'xMidYMid slice')
                    .attr('height', d => d.r * 2)
                    .attr('width', d=> d.r * 2)
                    //Clip the image to fit the circle
                    .attr('clip-path', d => `url(#clip-${d.data.track_id})`)
                    .attr('xlink:href', d => d.data.image_url)
                    //Make it visible
                    .style('visibility', 'visible');

                //Add text to each node
                currentNode.append('foreignObject')
                    .attr('x', d => d.x - d.r)
                    .attr('y', d => d.y - d.r/2 - 10)
                    .attr('width', d => d.r*2)
                    .attr('height', d => d.r*2)
                    //Make it invisible
                    .style('visibility', 'hidden')
                    .append('xhtml:div')
                        .attr('class', 'text-container')
                        //Add html text to the node
                        .html(d => `<div>
                            <p style="
                            ${(color == '#ffff00' || color == '#80ff00' || color == '#00ff00'|| color == '#00ffff') ? 'color: black;' : 'color: white'}; 
                            font-size: ${Math.round(d.r/5)}">
                                <strong>#${d.data.rank}</strong><br/>
                                <span style="font-weight:lighter">${d.data.name}</span>
                            </p>
                            </div>`)
                        .style('display', 'flex')
                        .style('justify-content', 'center')
                        .style('align-items', 'center')
                        .style('text-align', 'center');

                //Add mouseover and mouseout events to each node
                currentNode
                    .on('mouseover', function(event, d) {
                        changeCircle(event, d)
                    })
                    .on('mouseout', function(event, d) {
                        changeCircleBack(event, d);
                    });
            });

            //Function to show the text when hovering over a node
            const changeCircle = (event, d) => {
                //Cursor
                d3.select(event.currentTarget).style("cursor", "pointer");

                //Retrieve nb of tracks, bio and name for current artist 
                this.nb_tracks = d.data.size;
                this.bio = d.data.bio;
                this.artist_name = d.data.name;

                //Set artist selected to true
                this.isArtistSelected = true;

                //Show text
                d3.select(event.currentTarget).select("foreignObject")
                    .transition()
                        . duration(2000)
                        .style("visibility", "visible");
                //Hide image
                d3.select(event.currentTarget).select("image")
                    .transition()
                    .duration(2000)
                    .style("visibility", "hidden");
            };

            //Function to hide the text when hovering over a node
            const changeCircleBack = (event, d) => {
                //Reset default setup
                this.isArtistSelected = false;
                this.bio = "";
                this.nb_tracks = 0;
                this.artist_name = "";

                //Cursor
                d3.select(event.currentTarget)
                    .style("cursor", "default");
                //Hide text
                d3.select(event.currentTarget).select("foreignObject")
                    .transition()
                    .duration(2000)
                    .style("visibility", "hidden");
                //Show image
                d3.select(event.currentTarget).select("image")
                    .transition()
                    .duration(2000)
                    .style("visibility", "visible");
            };
        },
    },

}
</script>

<style scoped>
.container-chart-artists {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    margin-top: -10px;
}
.bio-artists{
    background-color: #191919;
}

.groot {
    display : flex;
    justify-content: center;
    align-items: center;
    width: 200px;
    padding-bottom : 20px;
    padding-left:100px;

}


</style>