<template>
    <v-form
    ref="form"
    v-model="valid"
  >
    <v-text-field
      v-model="name"
      :counter="30"
      :rules="nameRules"
      label="Name"
      required
    ></v-text-field>

    <v-text-field
      v-model="limit"
      :counter="3"
      :rules="limitRules"
      label="How many last tweets?"
      required
    ></v-text-field> 

    <v-btn
        :disabled="!valid"
        :loading="loading"
        color="success"
        class="mr-4 "
        style="position:absolute;bottom:8px"
        @click="validate"
      >
      Submit
    </v-btn>
  </v-form>
</template>
<script>

function isNumeric(n) {
   return !isNaN(n) && isFinite(n);
}

export default {
    data: () => ({
        loading: false,
        limit:null,
        valid: true,
        name: '',
        nameRules: [
          v => !!v || 'Name is required',
          v => (v && v.length <= 30) || 'Name must be less than 30 characters',
        ],
        limitRules: [
          v => !!v || 'Value is required',
          v => (v && v <= 100) || 'Value tweets must be less than 100',
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

      async validate () {
          let data ={
            name : this.name,
            limit:this.limit}
          this.loading =true
          await this.$store.dispatch('AddAccount',data)
          this.loading =false
          this.$store.dispatch("Change",1)
          this.$refs.form.validate()
      },
    
    },
  }
</script>

<style>
  .custom-loader {
    animation: loader 1s infinite;
    display: flex;
  }
  @-moz-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-webkit-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-o-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>