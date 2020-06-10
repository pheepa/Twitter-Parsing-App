<template>
    <v-form
        ref="form"
        v-model="valid"
    >
        <v-text-field
            v-model="name"
            :counter="30"
            :rules="nameRules"
            label="Hashtag title"
            required
        ></v-text-field>

        <v-menu
              ref="menu"
              v-model="menu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="290px"
        >
              <template v-slot:activator="{ on }">
                  <v-text-field v-model="dateRangeText"  v-on="on" label="Date range"  required></v-text-field>
              </template>
              <v-date-picker v-model="dates" ref="picker" range></v-date-picker>
        </v-menu>

        <v-text-field
              v-model="value"
              :counter="3"
              :rules="valueRules"
              label="Value"
              required
        ></v-text-field>

        <v-btn
              :disabled="!valid"
              :loading="loading"
              color="success"
              class="mr-4"
              @click="validate"
        >Submit
        </v-btn>
    </v-form>
</template>

<script>
import moment from 'moment'

function isNumeric(n) {
   return !isNaN(parseFloat(n)) && isFinite(n);
}

export default {
    data: () => ({
        dates: ['2020-06-01', '2020-06-09'],
        loading: false,

        menu: false,
        valid: true,
        name: '',
        nameRules: [
          v => !!v || 'Title is required',
          v => (v && v.length <= 30) || 'Title must be less than 30 characters',
        ],
        value: null,
        valueRules: [
          v => !!v || 'Value is required',
          v => (v && v <= 100) || 'Value must be less than 100',
          v => ( v>0)|| 'Value must be positive',
        v =>( isNumeric(v)) || 'It is not number',
        ],
    }),

    computed: {
      dateRangeText () {
          return this.dates.join(' ~ ')
      },
    },

    methods: {
        save (date) {
        this.$refs.menu.save(date)
    },

    async  validate () {
        let data ={
            hashtag : this.name,
            number_tweets : this.value
        }
        if(this.dates.length==2){
            if(moment(this.dates[0])<moment(this.dates[1])){
                data.from_date = moment(this.dates[0])
                data.until_date = moment(this.dates[1])
            }
            else{
                data.from_date = moment(this.dates[1])
                data.until_date = moment(this.dates[0])
            }
        }
        else{
            data.from_date = moment(this.dates[0])
            data.until_date = moment(this.dates[0])
        }
        this.loading =true
        await this.$store.dispatch('AddInquiry',data)
        this.loading =false    
        this.$store.dispatch("Change",0)
        this.$refs.form.validate()
      },
    },
  }
</script>