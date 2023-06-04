<!-- INTRODUCTION OF GROOT -->

<template>
    <v-container class = "pt--100" height="600">
      <v-row align="center" justify="center" class="row--35">
        
        <!-- GIF -->
        <v-col lg="5" md="5" cols="5">
            <v-img :src="grootHello" height="400"> </v-img> 
        </v-col>

        <v-col lg="7" md="7" cols="7">
          <div class="about-inner inner">
            <div class="section-title  mt-30">

              <!-- Text to present Groot -->
              <h3 class="fontWeight500">I am Groot!</h3>
              <p class="description white--text" style="font-size:18px; font-weight: lighter;" >
                Introducing Groot, our lovable mascot and guide on this journey into the vast universe of music and emotions! 
                <br/>
                With Groot by your side, you can expect an adventure filled with joy, discovery, and heartfelt connections. 
                <br/><br/>
                So, together with Groot as your trusted companion, let's embark on this extraordinary expedition, 
                delving into a world where music and emotions harmoniously unite.
                <br/><br/>
                Get ready for a truly unforgettable experience!
              </p>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import grootHello from "../../assets/data/waouh.gif";
  
  export default {
    data() {
      return {
        grootHello: grootHello,
      };
    },
  };
  </script>