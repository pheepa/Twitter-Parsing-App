<template>
    <v-hover style="height:645px">
        <template v-slot="{ hover }">
            <v-card
                :elevation="hover ? 24 : 8"
                class="mx-auto pa-0"
            >

            <v-toolbar-title class="blue accent-2 pa-2">
                <v-icon dark>mdi-alert-circle-check</v-icon>
                <span style="color:white" >Сhecking your own text for negative </span>
            </v-toolbar-title>
            
            <div class="p-3">
                <v-form
                    ref="form"
                    v-model="valid"
                >
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }"> 
                            <v-btn class="mx-2" @click="FileInput()"  style="position:absolute;right:2px;top:48px;z-index:1000"  fab  small >
                                <input type="file" id="fileInput" @change="ReadFiles($event)" class="btn d-none btn-info mb-1 btn-sm"/>
                                <v-icon v-on="on">mdi-auto-upload</v-icon>
                            </v-btn>              
                        </template>
                        <span>Upload text from file .txt</span>
                    </v-tooltip>

                    <v-textarea class="pb-1 mt-3 pr-1 "
                        outlined
                        v-model="text"
                        rows="14"
                        name="input-7-4"
                        label="Enter your text"
                        value=""
                        hint="Hint text"
                        :rules="textRules"
                        :counter="280"
                    ></v-textarea>

                    <v-text-field class="pb-5"
                        v-model="name"
                        :counter="30"
                        :rules="nameRules"
                        label="Text title"
                        required
                    ></v-text-field>

                    <v-btn
                        :loading="loading"
                        :disabled="!valid"
                        color="success"
                        class="mr-4"
                        @click="validate"
                    >Submit
                    </v-btn>
                </v-form>
            </div>
        </v-card>
    </template>
  </v-hover>          
</template>


<script>

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

 var txt;
import swal from 'sweetalert'

export default {
    data: () => ({
        loading: false,
        text:'',

        valid: true,
        name: '',
        nameRules: [
          v => !!v || 'Name is required',
          v => (v && v.length <= 30) || 'Name must be less than 30 characters',
        ],

        textRules: [
          v => !!v || 'Text is required',
          v => (v && v.length <= 280) || 'Text must be less than 5000 characters',
        ],
    }),

    methods: {
        async validate () {
            this.loading =true
            await this.$store.dispatch('AddWriting',{name: this.name, text: this.text})
            this.loading =false
            this.$store.dispatch("Change",2)
        },

        FileInput(){
            var fileInput = document.getElementById("fileInput");
            fileInput.click();
        },

        async ReadFiles(event){
            var file = event.target.files[0]
            if(file.type =="text/plain"){
                var fr = new FileReader();
                fr.readAsText(file)

                fr.onload = ( function (e) {
                txt = e.currentTarget.result  
                })
                
                await sleep(100)
                this.text = txt;
      
            } else{
                swal({
                title: "Error",
                text: "You can only download a file with a resolution of .txt",
                icon: "error",
                button: "Ok",
                });
            }
        }
    }
}

</script>
