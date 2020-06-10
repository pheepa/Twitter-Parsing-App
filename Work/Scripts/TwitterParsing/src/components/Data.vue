<template>
    <v-hover style="height:645px">
        <template v-slot="{ hover }">
            <v-card
                :elevation="hover ? 24 : 8"
                class="mx-auto pa-0"
            >
                <v-toolbar-title class="blue accent-2 pa-2">
                    <v-icon dark>mdi-database</v-icon>
                    <span style="color:white"> Results</span>
                </v-toolbar-title>

                <div class="p-0">
                    <v-tabs class="pl-2"
                        :value="tab" @change="Change"
                    >
                        <v-tab  >  
                            Hashtags
                        </v-tab>
                        <v-tab  >
                            Accounts
                        </v-tab>
                        <v-tab >
                            Texts
                        </v-tab>
                    </v-tabs>
                                                        
                    <v-tabs-items  :value="tab">
                        <v-tab-item style="height:0px">
                            <div class="p-2">
                                <router-view></router-view>
                            </div>
                        </v-tab-item>
                        
                        <v-tab-item style="height:0px">
                            <div class="p-2">
                                <router-view></router-view>
                            </div>
                        </v-tab-item>

                        <v-tab-item style="height:0px">
                            <div class="p-2">
                                <router-view></router-view>
                            </div>
                        </v-tab-item>
                    </v-tabs-items>
                </div>
            </v-card>
        </template>
    </v-hover>        
</template>


<script>

export default {
    data: () => ({
      text:'',
      items: [
          { tab: 'Hashtag',content:"Title hashtag",  },
          { tab: 'Account',content:"Name",  }
      ],
      valid: true,
      name: '',
    }),

    computed: {
        tab: {
            get () {
                return this.$store.state.tab
            },
            set (value) {
                this.$store.commit('setTab', value)
            }
        }
    },

    methods: {
        Change(t){
            this.tab =t
            this.$store.dispatch("Change",t)
        },
    },
}
</script>