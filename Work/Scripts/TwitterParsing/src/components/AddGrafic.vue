<template>
    <div class="row">
        <div class="col-6 p-0">

              <v-tabs class="pl-4"
                v-model="tab"
              >
                <v-tab
                  v-for="item in items"
                  :key="item.tab"
                >
                  
                  {{ item.tab }}
                </v-tab>
              </v-tabs>
              <v-tabs-items  v-model="tab">
                  <v-tab-item
                      style="height:0px"
                      v-for="item in items"
                      :key="item.tab" 
                  >
                  
                  <div class="p-3">
                      <v-form v-if="item.tab =='Account'"
                          ref="formgrafic"
                          v-model="validAccount"
                      >
                            <v-text-field 
                                v-model="name"
                                :counter="30"
                                :rules="nameRules"
                                label="Name"
                                required
                            ></v-text-field>

                            <v-text-field
                                v-model="value"
                                :counter="3"
                                :rules="valueRulesAccount"
                                label="How many last tweets?"
                                required
                            ></v-text-field>

                            <v-btn
                                :loading="loading1"
                                :disabled="!validAccount"
                                color="success"
                                class="mr-4 "
                                style="position:absolute;bottom:-218px"
                                @click="validate(item.tab)"
                            >
                            Submit
                            </v-btn>
                        </v-form>
                        
                        <v-form  v-if="item.tab =='Hashtag'"
                            ref="formgrafic"
                            v-model="validHashtag"
                        >
                            <v-text-field
                                v-model="hashtag"
                                :counter="30"
                                :rules="nameRules"
                                label="Hashtag title"
                                required
                            ></v-text-field>

                            <v-text-field
                                v-model="value"
                                :counter="3"
                                :rules="valueRulesHashtag"
                                label="How many last days?"
                                required
                            ></v-text-field>

                            <v-btn
                                :loading="loading2"
                                :disabled="!validHashtag"
                                color="success"
                                class="mr-4 "
                                style="position:absolute;bottom:-218px"
                                @click="validate(item.tab)"
                            >
                            Submit
                            </v-btn>
                        </v-form>
                    </div>                       
                </v-tab-item>
              </v-tabs-items>
          </div>

          <div class="col-6  ">
              <img src="" id="ItemPreview" style="height:220px" />
          </div>
        
          <div v-if="img" style="position:absolute;right:0px;bottom:7px">
            <v-btn class="mx-2"
                fab dark
                color="#448AFF"
                @click="downloadImg()"
            >
              <v-icon dark>mdi-download</v-icon>
            </v-btn>
          </div>
    </div>
</template>

<script>

function isNumeric(n) {
   return !isNaN(n) && isFinite(n);
}

export default {
    data: () => ({
      loading1: false,
      loading2: false, 

      tab: null,
      img:false,

      loading5: false,
      validAccount:true,
      validHashtag:true,
      name: '',
      hashtag:'',

      nameRules: [
        v => !!v || 'It is required',
        v => (v && v.length <= 30) || 'This must be less than 30 characters',
      ],

      items: [
          { tab: 'Hashtag',content:"Title hashtag",  },
          { tab: 'Account',content:"Name",  },
      ],
     
     value: null,
     valueRulesAccount: [
         v =>( isNumeric(v)) || 'It is not number',
         v => !!v || 'Value is required',
         v => (v && +v <= 100) || 'Value days must be less than 100',
         v => ( v>0)|| 'Value must be positive',
      ],

      valueRulesHashtag: [
         v =>( isNumeric(v)) || 'It is not number',
        v => !!v || 'Value is required',
        v => (v && +v <= 30) || 'Value days must be less than 30',
         v => ( v>0)|| 'Value must be positive',
      ],
    }),

    computed: {
      dateRangeText () {
        return this.dates.join(' ~ ')
      },
    },
    
    methods: {
      downloadImg(){
          var a = document.createElement("a"); //Create <a>
          a.href = "data:image/png;base64," + this.$store.state.byteImage.bits; //Image Base64 Goes here
          a.download = "Image.png"; 
          a.click();
      },

      save (date) {
          this.$refs.menu.save(date)
      },

      async validate (tab) {
          if(tab=="Account"){
              this.loading1 =true
              await  this.$store.dispatch('ChartingAccount', {name:this.name, months: this.value})
              this.loading1 =false
          }  
          else{
              this.loading2 =true
              await  this.$store.dispatch('ChartingHashtag', {name:this.hashtag, months: this.value})
              this.loading2 =false
          }
          this.img = true
          document.getElementById("ItemPreview").setAttribute( 'src', 'data:image/png;base64,' + this.$store.state.byteImage.bits);
      },
    },
  }
</script>


<style>
  .custom-loader {
    animation: loader 1s infinite;
    display: flex;
  }
</style>