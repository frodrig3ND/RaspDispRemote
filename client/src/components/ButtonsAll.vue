<template>
<div>
    <div>
      <br>
      <b-form-checkbox
      id="checkbox-1"
      v-model="delStatus"
      name="checkbox-delete"
      switch
      >
      Allow Delete
      </b-form-checkbox>
      <hr>
      <b-container class="bv-example-row">
        <b-row cols="1" cols-sm="2" cols-md="4" cols-lg="6">
          <b-col class="p-1" v-for="button in buttonsAll" :key="button.id">
            <div class="h-100" style="min-height: 10vh">
              <b-button size="md" class="w-100 h-100" variant="primary" @click="sendCommand(button)"
            @contextmenu="onBtnContext(button, $event)">
            {{button.description}}</b-button>
            </div>
          </b-col>
          <b-col class="p-1">
            <b-button class="w-100 h-100"
            variant="outline-success" @click="onReset" v-b-modal.create-btn-modal>+</b-button>
          </b-col>
        </b-row>
      </b-container>
    </div>
<!-- create button modal -->
    <b-modal ref="createBtnModal"
      id="create-btn-modal"
      title="Create new Button"
      hide-footer>
      <b-form class="w-100" @submit="onCreate">
        <b-form-group id="form-size-group"
                        label="Description:"
                        label-for="form-description-input">
          <b-form-input id="form-description-input"
                        type="text"
                        v-model="createBtnForm.description"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Target:"
                        label-for="form-target-input">
          <b-form-input id="form-command-target"
                        type="text"
                        v-model="createBtnForm.target"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Workdir:"
                        label-for="form-wd-input">
          <b-form-input id="form-wd-input"
                        type="text"
                        v-model="createBtnForm.workdir"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Type:"
                        label-for="form-type-input">
        <b-form-select v-model="createBtnForm.action_type_id"
        :options="btypes"
        value-field="id"
        text-field="command"></b-form-select>
        </b-form-group>
        <br>
        <b-button-group>
          <b-button type="submit" variant="primary">Create</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
<!-- edit button modal -->
    <b-modal ref="editBtnModal"
      id="edit-btn-modal"
      title="Edit Button record"
      hide-footer>
      <b-form class="w-100" @submit="onEdit">
        <b-form-group id="form-size-group"
                        label="Description:"
                        label-for="form-description-input">
          <b-form-input id="form-description-input"
                        type="text"
                        v-model="editBtnForm.description"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Target:"
                        label-for="form-target-input">
          <b-form-input id="form-command-target"
                        type="text"
                        v-model="editBtnForm.target"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Workdir:"
                        label-for="form-wd-input">
          <b-form-input id="form-wd-input"
                        type="text"
                        v-model="editBtnForm.workdir"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Type:"
                        label-for="form-type-input">
        <b-form-select v-model="editBtnForm.action_type_id"
        :options="btypes"
        value-field="id"
        text-field="command"></b-form-select>
        </b-form-group>
        <br>
        <b-button-group>
          <b-button type="submit" variant="primary">Edit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
<!-- delete modal -->
    <b-modal ref="confirmDelete"
          id="del-conf"
          :title= "editBtnForm.name"
          hide-footer>
    <b-button-group>
      <b-button type="submit" variant="danger" @click="onDel">Delete</b-button>
    </b-button-group>
  </b-modal>
</div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'ButtonsAll',
  data() {
    return {
      delStatus: false,
      btnDelid: '',
      createBtnForm: {
        description: '',
        target: '',
        workdir: '',
        action_type_id: '',
      },
      editBtnForm: {
        description: '',
        target: '',
        workdir: '',
        action_type_id: '',
      },
    };
  },
  computed: {
    buttonsAll() {
      return this.$store.state.buttons;
    },
    cbutton() {
      return this.$store.state.button;
    },
    btypes() {
      return this.$store.state.buttonTypes;
    },
  },
  methods: {
    onButtonSel(btn) {
      console.log(btn);
    },
    onBtnContext(btn, evt) {
      evt.preventDefault();
      this.updateSelButton(btn.id);
      if (this.delStatus === false) {
        this.btnSelid = btn.id;
        this.$bvModal.show('edit-btn-modal');
      } else {
        this.btnSelid = btn.id;
        this.$bvModal.show('del-conf');
      }
    },
    async updateSelButton(id) {
      await this.$store.dispatch('fetchButton', id);
      this.editBtnForm.description = this.cbutton.description;
      this.editBtnForm.target = this.cbutton.target;
      this.editBtnForm.workdir = this.cbutton.workdir;
      this.editBtnForm.action_type_id = this.cbutton.action_type_id;
    },
    onReset() {
      this.editBtnForm = {
        description: '',
        target: '',
        workdir: '',
        action_type_id: '',
      };
    },
    onCreate(evt) {
      evt.preventDefault();
      this.$bvModal.hide('create-btn-modal');
      const payload = {
        description: this.createBtnForm.description,
        target: this.createBtnForm.target,
        workdir: this.createBtnForm.workdir,
        action_type_id: this.createBtnForm.action_type_id,
      };
      this.$store.dispatch('addButton', payload).then(this.$store.dispatch('fetchButtons'));
    },
    onEdit(evt) {
      evt.preventDefault();
      this.$bvModal.hide('edit-btn-modal');
      const payload = {
        description: this.editBtnForm.description,
        target: this.editBtnForm.target,
        workdir: this.editBtnForm.workdir,
        action_type_id: this.editBtnForm.action_type_id,
      };
      this.$store.dispatch('editButton', { id: this.btnSelid, data: payload }).then(this.$store.dispatch('fetchButtons'));
      this.btnSelid = '';
      this.onReset();
    },
    onDel(evt) {
      evt.preventDefault();
      this.$bvModal.hide('del-conf');
      this.$store.dispatch('deleteButton', this.btnSelid);
      this.btnSelid = '';
    },
    sendCommand(command) {
      const path = `http://localhost:8000/commands/${command.id}`;
      axios.post(path).then(() => {
        console.log(`Command ${command.id} sent`);
      })
        .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        });
    },
  },
  mounted() {
    this.$store.dispatch('fetchButtons');
    this.$store.dispatch('fetchButtonTypes');
    this.connection.onmessage = function (event) {
      console.log(event);
    };
  },
};
</script>
