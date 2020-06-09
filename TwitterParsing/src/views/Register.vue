<template>
    <v-app id="inspire" >
        <v-content >
            <v-container
                class="fill-height"
                fluid
            >
                <v-row
                    align="center"
                    justify="center"
                >
                    <v-col
                        cols="12"
                        sm="8"
                        md="4"
                    >
                        <v-card class="elevation-12">
                            <v-toolbar
                                color="blue"
                                dark
                                flat
                            >
                                <v-toolbar-title>Registration</v-toolbar-title>
                            </v-toolbar>

                            <v-card-text>
                                <v-form
                                    ref="form"
                                    v-model="valid"
                                    lazy-validation
                                >
                                    <v-text-field
                                        v-model="name"
                                        :counter="10"
                                        :rules="nameRules"
                                        label="Name"
                                        required
                                    ></v-text-field>

                                    <v-text-field
                                        v-model="email"
                                        :rules="emailRules"
                                        label="E-mail"
                                        required
                                    ></v-text-field>

                                    <v-text-field
                                        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                                        :rules="passwordRules"
                                        :type="show ? 'text' : 'password'"
                                        name="input-10-2"
                                        label="Password"
                                        hint="At least 8 characters"
                                        v-model="password"
                                        required
                                        class="input-group--focused"
                                        @click:append="show = !show"
                                    ></v-text-field>

                                    <div class="text-right w-100">
                                        <v-btn 
                                            :disabled="!valid"
                                            color="success"
                                            class="mr-4 align-self-end  "
                                            @click="validate"
                                        >sign in
                                        </v-btn>
                                    </div>
                                </v-form>
                            <v-spacer></v-spacer>
                            <div class="text-center mt-2 w-100">
                                <router-link to="/login" class="px-5" style="font-size:15px">Log in</router-link>
                            </div>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-content>
  </v-app>
</template>

<script>

  export default {
      props: {
          source: String,
      },
      data: () => ({
          show:false,
          valid: false,
          name: '',
          password: '',
          passwordRules: [
              v => !!v || 'Required.',
              v => (v.length >= 8) || 'Min 8 characters',
          ],
          nameRules: [
              v => !!v || 'Name is required',
              v => (v && v.length <= 10) || 'Name must be less than 10 characters',
          ],
          email: '',
          emailRules: [
              v => !!v || 'E-mail is required',
              v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
          ],
        }),

        methods: {
            validate () {
                if(this.password){
                    let data = {
                        name : this.name,
                        password: this.password,
                        email : this.email
                    }
                    this.$store.dispatch("SignUp",data)
                }
                this.$refs.form.validate()
            }, 
        },
    }
</script>