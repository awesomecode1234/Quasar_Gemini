<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-file
        v-model="file"
        label="Select a file"
      />
      <q-btn @click="uploadFile">{{btnText}}</q-btn>

      <q-banner v-if="responseMessage" class="q-mt-md">
        {{ responseMessage }}
      </q-banner>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const btnText = ref('Upload')
const responseMessage = ref('')

const uploadFile = async () => {
  btnText.value = 'Uploading...'
  if (!file.value) {
    console.error('No file selected')
    responseMessage.value = 'No file selected'
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const response = await axios.post('http://localhost:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    responseMessage.value = response.data.message
    file.value = null
  } catch (error) {
    console.error(error)
    if (error.response && error.response.data) {
      responseMessage.value = error.response.data.responsetext || 'An error occurred'
    } else {
      responseMessage.value = 'An unknown error occurred'
    }
  }
  btnText.value = 'Upload New File'
}
</script>
