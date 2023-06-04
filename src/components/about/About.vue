<!-- SECTION INTRODUCTION - ABOUT -->

<template>
  <v-container class = "pt--100" height="600">
    <v-row align="center" justify="center" class="row--35">
      
      <v-col lg="5" md="5" cols="5">
          <v-img :src="wheel" height="500"> </v-img> 
      </v-col>
      
      <v-col lg="7" md="7" cols="7">
        <div class="about-inner inner">
          <div class="section-title  mt-30">
            <h3 class="fontWeight500">About</h3>
            <p class="description white--text" style="font-size:18px; font-weight: lighter;" >
              Our project aims to explore the intriguing relationship between music and emotions through visualisation. 
              <br> <br>
              With the guidance of Robert Plutchik's theory, we aim to cluster tracks into eight basic emotions and eight mixed emotions, 
              including joy, sadness, trust, love, awe, aggressiveness, and more.
              <br>
              We will explore the connections between songs through their appearance in the same Spotify playlists, allowing us to uncover the hidden relationships between music and emotions. 
              <br> <br>
              Feel free to play around and examine the characteristics of each cluster to gain a deeper understanding of how emotions are expressed through music.
            </p>
          </div>
          
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import wheel from "../../assets/data/wheel_emotion.png";

export default {
  name: "About",
  data() {
    return {
      wheel: wheel,
    };
  },
};
</script>