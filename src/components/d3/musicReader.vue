<!-- SECTION 2 - PLAYLIST -->
<template>
    <div class="playlists">
        <h3 class="moodPlaylist"> 
            <span :style="{ color: color }">Your mood playlist {{smiley}}</span>
        </h3>
        <v-data-table 
            :headers="[
            { text: 'Album', value: 'image_url' },
            { text: 'Track', value: 'track' },
            { text: 'Artist', value: 'artist' },
            { text: 'Genre', value: 'genre' },
            { text: 'Preview', value: 'preview_url' }]"
            :items="items"
            :items-per-page="5"
            class="elevation-1 playlistTable"
            :key="items.length"
            dark
        >

            <template v-slot:item.image_url="{ item }">
                <v-img
                :src="item.image_url"
                height="80px"
                width="80px"
                :cover="true"
                ></v-img>
            </template>

            <template v-slot:item.preview_url="{ item }">
                <v-icon @click="playAudio(item)">mdi-play-circle</v-icon>
            </template>

        </v-data-table>
        

    </div>
</template>

<script>
import tracks_preview from '../../assets/data/emotion2tracks#2.json'
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiPlayCircleOutline } from '@mdi/js';

export default{
    components: {
        SvgIcon,
    },
    data() {
        return {
            path :  mdiPlayCircleOutline,
            Names : ["Joy", "Love", "Trust", "Fear", "Awe", "Sadness", "Remorse", "Disgust", "Contempt", "Anger", "Anticipation", "Optimism"],
            Colors : ["#FF0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ffff", "#0080ff", "#0000ff","#A639FF",  "#8000ff", "#ff00ff", "#ff0080"],
            Smileys : ["😀", "😍", "🤗", "😱", "😲", "😢", "😔", "🤢", "😒", "😡", "🤔", "🙂"],
            current_track_audio : null,
            past_track_audio : null,
            current_track_audio_id : null,
        }
    },
    computed : {
        index() {
            return this.$store.state.index;
        },
        clicked_emotion() {
            return this.$store.state.clicked_emotion;
        },
        name() {
            return this.Names[this.index].toLowerCase();
        },
        color() {
            return this.Colors[this.index];
        },
        smiley() {
            return this.Smileys[this.index];
        },
        items () {
            //Retrieve genre from vuex store
            const genre = this.$store.state.genre;
            if(genre == null) { //No genre selected
                //Keep 100 most popular tracks
                if(tracks_preview[this.name].length > 100) {    
                    return tracks_preview[this.name].slice(0, 100);
                } else {
                    return tracks_preview[this.name];
                }
            } else {
                //Filter tracks by genre
                const filtered_tracks = tracks_preview[this.name].filter(track => track.genre == genre);
                if(filtered_tracks.length > 100) {
                    return filtered_tracks.slice(0, 100);
                } else {
                    return filtered_tracks;
                }
            }  
        }, 
    },

    methods : {
        playAudio(item) {
            if (this.current_track_audio_id == item.preview_url) { //Current track is played
                this.current_track_audio.pause();
                this.current_track_audio.currentTime = 0;
                this.current_track_audio = null;
                this.current_track_audio_id = null;
                return;
            }
            else if (this.current_track_audio != null) { //One music is already played
                this.current_track_audio.pause();   //Pause it
                this.current_track_audio.currentTime = 0;
            } 
            //Play new track
            this.current_track_audio = new Audio(item.preview_url); 
            this.current_track_audio_id = item.preview_url;
            this.current_track_audio.play();
        },
    }
}
</script>

<style scoped>

/* Add this CSS to change the full color of the v-data-table */
.playlistTable {
    --v-data-table-color: #191919;
    --v-data-table-header-text-color: pink;
    --v-data-table-header-background-color: #191919;
    --v-data-table-selected-color: #191919;
    --v-data-table-border-color: pink;
}
.moodPlaylist {
    text-align: center;
    padding-top : 30px;
    padding-bottom : 10px;
}

</style>