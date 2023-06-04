<template>
  <div class="active-dark">
      <!-- Start Header  -->
      <div
        class="call-to-action-wrapper call-to-action text-white-wrapper pt--120 pb--120"
        style="border-bottom: white;border-style: solid;border-width: thin;"
      >
        <vue-particles
          :color="Colors"
          :particleOpacity="1"
          :particlesNumber="150"
          shapeType="circle"
          :particleSize="6"
          linesColor="#FFFFFF"
          :linesWidth="1"
          :lineLinked="true"
          :lineOpacity="0.4"
          :linesDistance="150"
          :moveSpeed="6"
          :hoverEffect="true"
          hoverMode="grab"
          :clickEffect="true"
          clickMode="push"
          class="particles"
        >
        </vue-particles>
        <v-container>
          <v-row>
            <v-col lg="12">
              <div class="inner text-center">
                <span
                  >MUSIC HAS ALWAYS BEEN A POWERFUL MEDIUM FOR EXPRESSING EMOTIONS.</span
                >
                <h2>Melodic Moods: Exploring Emotions Through Music.</h2>
                
                <h4>
                  Are you ready ? Let's get started.
                </h4>

              </div>
            </v-col>
          </v-row>
        </v-container>
      </div>

      <!-- Start About Area -->
      <div class="rn-counterup-area pt--220 pb--110 bg_color--1">
        <About/>
      </div>

      <!-- Start Data Area -->
      <div class="rn-counterup-area pt--35 pb--110 bg_color--1">
        <v-container>
          <v-row class="row">
            <v-col cols="12">
              <div class="section-title text-center">
                <h3 class="fontWeight500">The data</h3>
              </div>
            </v-col>
          </v-row>
          <CounterOne />
        </v-container>
      </div>

      <!-- Start Groot -->
      <div class="rn-counterup-area pt--220 pb--110 bg_color--1">
        <Groot/>
      </div>


    <!-- SECTION 1 - CHORD DIAGRAM -->
    <div class="rn-counterup-area pt--25 pb--1 bg_color--1 music_mood">
      <v-container>
        <!--Title-->
        <v-row>
          <v-col lg="12">
            <div class="section-title text-center">
              <h2 class="heading-secondary">Music & Mood Connections</h2>
            </div>
          </v-col>
        </v-row>
        <!--Chord-->
        <v-row>
          <Chord />
        </v-row>
      </v-container>
    </div>

    <!-- SECTION 2 - PRESENTATION OF SELECTED EMOTION -->
    <div v-show="clicked_emotion" class="rn-counterup-area pt--25 pb--1 bg_color--1 music_mood">
      <v-container>
        <v-card class='infosEmotion' :style="{ borderColor: color }">

          <!-- Title -->
          <v-card-title>
            <v-icon class='spotify_icon' :color="color" size="xxx-large">mdi-spotify</v-icon>
            <h2 class="heading-secondary">{{name}}</h2>
          </v-card-title>

          <!--Introduction text-->
          <v-card-text>
            <v-row>
              <v-col cols="9">
                <p  class="white--text" style="font-size: 15px; margin-bottom: 30px;">
                  Welcome to the captivating world of <span :style="{color: color}">{{name}}</span>!
                  <br/> 
                  Get ready to explore a selection of tracks that encapsulate the essence of this powerful emotion. 
                  <br/>
                  With just a few clicks, you'll uncover a wealth of fascinating insights. 
                  <br/><br/>
                  Start by discovering the <span :style="{color: color}"> major tags </span> associated with these tracks, providing a glimpse into the themes that define this emotional landscape. 
                  <br/>
                  Then, dive into the <span :style="{color: color}"> top 10 artists </span> who have captured the spirit of {{name}} in their music. 
                  <br/>
                  Lastly, analyze the <span :style="{color: color}"> audio features </span> directly sourced from Spotify. 
                  <br/><br/>
                  Sit back, relax, and enjoy your exploration of {{name}} through the lens of music!
                </p>
              </v-col>

              <!--Groot GIF-->
              <v-col cols="3">
                <v-img :src="grootHello" style="width:400px"></v-img>
              </v-col>
            </v-row>

            <!-- Wordcloud, features, artists -->
            <v-row>
              <v-card class="v-tabs-emotion" style="background:#191919" width="100%">
                <v-tabs
                  v-model="tab"
                  :color="color"
                  justify-content="center"
                  background-color="#191919"
                  dark
                >
                  <v-tab style="fontWeight:18px, color:white" href="#one">Top Tags</v-tab>
                  <v-tab-item value="one">
                    <wordCloud/>
                  </v-tab-item>

                  <v-tab  :style="{fontWeight:'18px'}"  href="#two">Top 10 Artists</v-tab>
                  <v-tab-item value="two">
                    <Artists/>
                  </v-tab-item>

                  <v-tab  :style="{fontWeight:'18px'}" href="#three">Audio features</v-tab>
                  <v-tab-item value="three">
                    <Features/>
                  </v-tab-item>

                </v-tabs>
              </v-card>
            </v-row>
            
            <!-- Divider -->
            <v-divider :color="color" thickness="3px">
            </v-divider>

            <!-- Playlist -->
            <v-row>
              <v-col cols="12">
                <musicReader/>
              </v-col>
            </v-row>

            <v-row class="jumpLine">

              <!-- Groot presentation -->
              <v-col cols="5">
                <v-img :src="grootDance" style="height:200px"></v-img>
                <p  class="white--text" style="font-size: 15px; padding-top:15px">
                  Wow, check out this incredible selection of tracks tailored to match your current mood! 
                  <br/>
                  But hold on, there's more! You can click on one of the top 5 genres and the playlist gets updated to match your favorite selected genre.
                  <br/><br/>
                  Looking to return to the initial playlist and explore all genres once again? 
                  <br/>
                  Simply click on the button below!
                </p>

                <!-- Reset all genres -->
                <div class="buttonInit">
                  <v-btn @click="allGenres()" :color="color" variant="outlined">
                    All genres
                  </v-btn>
                </div>
              </v-col>

              <!-- Top 5 Genres -->
              <v-col cols="7">
                <Genres/>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-container>
    </div>

    <!-- SECTION 3 - Music Comparison across Moods -->
    <div class="rn-counterup-area pt--100 pb--100 bg_color--1">
      <v-container>
        <v-row>
          <v-col lg="12">
            <div class="section-title text-center">
              <h2 class="heading-secondary">Music Comparison across Moods</h2>
            </div>
          </v-col>
        </v-row>
        <v-row>
          <Barchart />
        </v-row>
      </v-container>
    </div>
    
    <!-- SECTION 4 - Music Comparison across Genres -->
    
            <div class="rn-counterup-area pt--100 pb--100 bg_color--1">
              <v-container>
                <v-row>
                  <v-col lg="12">
                    <div class="section-title text-center">
                      <h2 class="heading-secondary">Music Comparison across Genres</h2>
                      </div>
                    </v-col>
                  </v-row>
                <v-row>
                      <circularPacking/>
                </v-row>
              </v-container>
            </div>

    <!-- Footer -->
    <div class="rn-counterup-area pt--200 bg_color--1">
      <Footer/>
    </div>

  </div>
</template>

<script>
  //Import components
  import About from "../components/about/About";
  import CounterOne from "../components/counter/CounterOne";
  import Footer from "../components/footer/Footer";
  import Groot from "../components/groot/Groot";
  import Chord from "../components/d3/Chord.vue";
  import musicReader from "../components/d3/musicReader.vue";
  import wordCloud from "../components/d3/wordCloud.vue";
  import Genres from "../components/d3/Genres.vue";
  import Features from "../components/d3/Features.vue";
  import Artists from "../components/d3/Artists.vue";
  import Barchart from "../components/d3/Barchart.vue";
  import circularPacking from "../components/d3/circularPacking.vue";
  import parallelCoordinates from "../components/d3/parallelCoordinates.vue";

  //Import icons
  import { mdiSpotify } from '@mdi/js';

  //Import GIFs
  import grootHello from "../assets/data/grootdance.gif";
  import grootDance from "../assets/data/grootdance2.gif";

  export default {
    components: {
      About,
      CounterOne,
      Footer,
      Groot,
      Barchart,
      Chord,
      musicReader,
      wordCloud,
      Genres,
      Features,
      Artists,
      parallelCoordinates,
      circularPacking,

    },
    data() {
      return {
        path : mdiSpotify,
        grootHello : grootHello,
        grootDance : grootDance,
        Names : ["Joy", "Love", "Trust", "Fear", "Awe",  "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
        Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00",  "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
        Smileys : ["😀", "😍", "🤗", "😱", "😲",  "😢", "😔", "🤢", "😒", "😡", "🤔", "🙂"],
      };
    },

    computed: {
      index() {
        return this.$store.state.index;
      },
      clicked_emotion() {
        return this.$store.state.clicked_emotion;
      },
      name() {
        return this.Names[this.index];
      },
      color() {
        return this.Colors[this.index];
      },
      text_color() {
            if (this.name == "sadness" || this.name == "awe" || this.name == "fear" || this.name == "trust") {
                return "#191919";
            } else {
                return "white";
            }
      },
      smiley() {
        return this.Smileys[this.index];
      },
    },
    methods : {
      allGenres() {
        this.$store.commit('setGenre', null);
      },
    }
  };
</script>


<style lang="scss" scoped>
.theme--dark.about-expension-panels .v-expansion-panel-header::after {
  height: 1px;
  width: 100%;
}
.particles {
  position: absolute;
  width: 100%;
  height: 120%;
  margin-top:-120px;
}
.theme--dark.about-expension-panels .v-expansion-panel-header {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 0 0 10px 0;
  font-size: 18px;
}
.main-page-preview-gallery {
  .v-tabs {
    margin: 35px auto 30px;
  }
}
.jumpLine {
  padding-top:40px;
}
.infosEmotion {
  background-color: #191919;
  padding: 32px;
  border-width: 2px;  
  border-style: solid;
  border-color:#f9004d;

}
.spotify_icon {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  margin-top: -11px;
}
.buttonInit {
  display: flex;
  justify-content: center;
}
.data-v-1e61a1be{
  background: #191919;
}

</style>
