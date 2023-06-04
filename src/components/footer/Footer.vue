<template>
  <footer class="footer-area footer-default">
    <div class="footer-wrapper">
      <v-row align="end" class="row--0">
        <v-col md="6" sm="12" cols="12">
          <div class="footer-left" style="border: solid;border-color: white;border-width: thin;">
            <div class="inner">
              <span>We hope you enjoyed</span>
              <h2>
                your Musical <br />
                Journey !
              </h2>
              
            </div>
          </div>
        </v-col>
        <!-- End .col -->
        <v-col md="6" sm="12" cols="12">
          <div class="footer-right" data-black-overlay="6">
            <v-row>

              <!-- Start Single Widget -->
              <v-col lg="6" sm="6" cols="12" class="mt_mobile--30">
                <div class="footer-widget">
                  <h4>Say Hello 👋</h4>
                  <ul class="ft-link">
                    <li v-for="(mail, i) in mailList" :key="i">
                      <a :href="mail.to">{{ mail.mailItem }}</a>
                    </li>
                  </ul>
                </div>
              </v-col>
              <!-- End Single Widget  -->

              <v-col lg="12">
                <div class="copyright-text">
                  <p>
                    Copyright © {{ new Date().getFullYear() }} SpoTeamFy.
                    All Rights Reserved.
                  </p>
                </div>
              </v-col>
            </v-row>
          </div>
        </v-col>
        <!-- End .col -->
      </v-row>
    </div>
  </footer>
</template>

<script>
  export default {
    data() {
      return {
        mailList: [
          {
            mailItem: "joanne.affolter@epfl.ch",
            to: "mailto:joanne.affolter@epfl.ch",
          },
          {
            mailItem: "damien.gomezdonoso@epfl.ch",
            to: "mailto:damien.gomezdonoso@epfl.ch",
          },
          {
            mailItem: "esraa.eltayar@epfl.ch",
            to: "mailto:esraa.eltayar@epfl.ch",
          },
        ],
      };
    },
  };
</script>
