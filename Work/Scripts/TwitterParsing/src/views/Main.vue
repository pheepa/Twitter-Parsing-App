<template>
    <v-app id="inspire">
        <v-navigation-drawer
            v-model="drawer"
            app
            clipped
        >
            <v-list dense>

                <v-list-item two-line >
                    <v-list-item-avatar>
                        <img src="https://randomuser.me/api/portraits/men/81.jpg">
                    </v-list-item-avatar>
                    <v-list-item-content>
                        <v-list-item-title>{{this.$store.state.user.name}}</v-list-item-title>
                        <v-list-item-subtitle>{{this.$store.state.user.email}}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>

                <v-list-item @click="change()" link> 
                    <v-list-item-action>   
                        <v-icon >mdi-database</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>    
                        <v-list-item-title>Results</v-list-item-title> 
                    </v-list-item-content>     
                </v-list-item>
          
                <router-link to="/" style="text-decoration: none; color: inherit;">
                    <v-list-item link>
                        <v-list-item-action>
                            <v-icon>mdi-alert-circle-check</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>Checking your own text</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </router-link>

                <router-link to="/login" @click="LogOut" style="text-decoration: none; color: inherit;">
                    <v-list-item @click="LogOut" link>
                        <v-list-item-action>
                            <v-icon>mdi-exit-to-app</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>Log out</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </router-link>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar
            app
            clipped-left
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
            <v-toolbar-title>Twitter Parsing </v-toolbar-title>
            <img style="width:35px" class="ml-2" src="https://avatars.mds.yandex.net/get-pdb/1658707/58498ad4-958c-4b7a-ab90-2030bb8a4aa9/s1200?webp=false" />
            <v-icon style="position:absolute;right:90px">mdi-white-balance-sunny</v-icon>
            <v-icon style="position:absolute;right:20px">mdi-weather-night</v-icon>
            <v-switch 
                style="position:absolute;right:40px"
                v-model="statusDay"
                @change="Day"
                color="black"
                value="true"
                hide-details
            ></v-switch>
        </v-app-bar>

        <v-content>
            <div class="h-100 main">
                <div class="row pr-5">
                    <div class="col-7 pt-0">
                        <div class="row m-0">
                            <div class="col-6  ">
                                <v-hover  style="height:300px;">
                                    <template v-slot="{ hover }">
                                        <v-card
                                            :elevation="hover ? 24 : 8"
                                            class="mx-auto pa-0"
                                        >
                                            <v-toolbar-title color="white"   class="blue accent-2 pa-2">
                                                <v-icon dark>{{ mdiPoundBox }}</v-icon>
                                                <span style="color:white">Hashtag negative definition </span>
                                            </v-toolbar-title>
                                  
                                            <AddInquiry class="pl-3 pr-3"/>

                                        </v-card>
                                    </template>
                                </v-hover>
                            </div>

                            <div class="col-6">
                                <v-hover style="height:300px">
                                    <template v-slot="{ hover }">
                                        <v-card
                                            :elevation="hover ? 24 : 8"
                                            class="mx-auto pa-0"
                                        >
                                            <v-toolbar-title class="blue accent-2 pa-2">
                                                <v-icon dark>{{ svgPath }}</v-icon>
                                                <span style="color:white">Account negative definition </span>
                                            </v-toolbar-title>
                                        
                                            <AddAccount class="pl-3 pr-3"/>
                                        </v-card>
                                    </template>
                                </v-hover>
                            </div>

                            <div class="col-12">
                                <v-hover style="height:320px">
                                    <template v-slot="{ hover }">
                                        <v-card
                                            :elevation="hover ? 24 : 8"
                                            class="mx-auto pa-0"
                                        >

                                            <v-toolbar-title class="blue accent-2 pa-2">
                                                <v-icon dark>{{ mdiChartAreaspline }}</v-icon>
                                                <span style="color:white">Сharting</span>
                                            </v-toolbar-title>

                                            <AddGrafic class="pl-3 pr-3"/>
                                        </v-card>
                                    </template>
                                </v-hover>
                            </div>
                        </div>
                    </div>

                    <div class="col-5 pr-1 pl-0 ">
                        <router-view/>
                    </div>
                </div>
            </div>
        </v-content>

        <v-footer app>
            <span class="mr-4">&copy; 2020  Python project:    </span>
            <span> N. Alexandr, A. Philipp  </span>
        </v-footer>
    </v-app>
</template>

<script>

import AddInquiry from "../components/AddInquiry"
import AddAccount from "../components/AddAccount"
import AddGrafic from "../components/AddGrafic"

  export default {
      components:{
          AddInquiry,
          AddAccount,
          AddGrafic
      },
      props: {
          source: String,
      },

      mounted(){
          if(this.$store.state.user.token == null)
              this.$router.push('/login')
      },

      created () {
          this.$vuetify.theme.dark = false
      },

      data(){
          return{
              drawer: null,
              statusDay:true
          }
      },

      methods:{
          async LogOut(){
              await this.$store.dispatch('LogOut')
          },

          Day(){
              this.$vuetify.theme.dark = !this.$vuetify.theme.dark
          },

          change(){
              this.$store.dispatch("Change",this.$store.state.tab)
          }
      }  
  }
</script>