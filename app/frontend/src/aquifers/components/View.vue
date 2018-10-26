/*
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

<template>
  <b-card no-body class="p-3 mb-4">
    <b-container>
      <b-row class="border-bottom mb-3 pb-2">
        <b-col><h5 class="pt-2">Aquifer Summary</h5></b-col>
        <b-col cols="auto">
          <b-button
            variant="default"
            v-if="userRoles.aquifers.edit"
            v-on:click.prevent="edit()">
            <span title="Edit" class="fa fa-edit"/>
          </b-button>
          <a class="ml-2 print fa fa-print fa-lg d-print-none"
            href="#"
            title="Print"
            v-on:click.prevent="print()"
           />
        </b-col>
      </b-row>

      <dl class="row">
        <dt class="col-sm-2">Aquifer number</dt>
        <dd class="col-sm-4">{{record.aquifer_id}}</dd>
        <dt class="col-sm-2">Year of mapping</dt>
        <dd class="col-sm-4">{{record.mapping_year}}</dd>

        <dt class="col-sm-2">Aquifer name</dt>
        <dd class="col-sm-4">{{record.aquifer_name}}</dd>
        <dt class="col-sm-2">Litho stratigraphic unit</dt>
        <dd class="col-sm-4">{{record.litho_stratographic_unit}}</dd>

        <dt class="col-sm-2">Descriptive location</dt>
        <dd class="col-sm-4">{{record.location_description}}</dd>
        <dt class="col-sm-2">Vulnerability</dt>
        <dd class="col-sm-4">{{record.vulnerability_description}}</dd>

        <dt class="col-sm-2">Material type</dt>
        <dd class="col-sm-4">{{record.material_description}}</dd>
        <dt class="col-sm-2">Subtype</dt>
        <dd class="col-sm-4">{{record.subtype_description}}</dd>

        <dt class="col-sm-2">Quality concerns</dt>
        <dd class="col-sm-4">{{record.quality_concern_description}}</dd>
        <dt class="col-sm-2">Productivity</dt>
        <dd class="col-sm-4">{{record.productivity_description}}</dd>

        <dt class="col-sm-2">Size (km²)</dt>
        <dd class="col-sm-4">{{record.area}}</dd>
        <dt class="col-sm-2">Demand</dt>
        <dd class="col-sm-4">{{record.demand_description}}</dd>
      </dl>
    </b-container>
  </b-card>
</template>

<style>
.print, .print:hover {
  color: black;
  text-decoration: none;
}
</style>

<script>
import ApiService from '@/common/services/ApiService.js'
import { mapGetters } from 'vuex'

export default {
  props: ['id'],
  created () { this.fetch() },
  data () {
    return {
      record: {}
    }
  },
  computed: {
    ...mapGetters(['userRoles'])
  },
  watch: {
    id () { this.fetch() }
  },
  methods: {
    edit () {
      this.$router.push({ name: 'edit', params: { id: this.id } })
    },
    print () {
      window.print()
    },
    fetch (id = this.id) {
      ApiService.query(`aquifers/${id}`)
        .then((response) => {
          this.record = response.data
        })
    }
  }
}
</script>