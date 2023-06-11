<template>
  <div  class="lg:h-[91vh] h-[88vh] cursor-default" 
  @keyup.ctrl.enter="getStreamCompletion()"
  @keyup.alt.c="stopCompletion()"
  @keyup.alt.l="clearAll()"
  >
    <div class="flex h-full">

     
      <div class="flex-grow w-full h-full pb-10 bg-gray-50 p-4">
        <h2 class="text-xl font-bold mb-4">Playground</h2>

        <!-- Prompt Area -->
        <textarea ref="promptBoxArea" v-model="promptBoxContent" class="w-full h-full resize-none p-4 border-2 rounded-md border-neutral-300 outline-none" placeholder="Put your prompt...">Esto es</textarea>
      </div>

      <!-- Settings panel -->
      <div class="w-1/4 p-4 bg-gray-100 overflow-auto ">
        <h2 class="text-xl font-bold mb-4">Settings</h2>

        <!-- Preset select -->
        <h1 class="font-light pt-2">Prompt styles</h1>
        <select class="w-4/5   block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none w- focus:ring-indigo-500" @change="handlePresets($event)">
          <option v-for="value, key in presets" :value="value.value" :key="value.value">{{ key }}</option>
        </select>

        <!-- temperature -->
        <h1 class="font-light pt-2">Temperature</h1>
        <input v-model="p_temperature" type="number" step="0.1" min="0" max="1"  class="appearance-none block w-full py-2 px-3  w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">
        
        <!-- n_predict  -->
        <h1 class="font-light pt-2">n_predict</h1>
        <input v-model="p_n_predict" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

        
        <!-- top_k  -->
        <h1 class="font-light pt-2">top_k</h1>
        <input v-model="p_top_k" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

        <!-- top_p  -->
        <h1 class="font-light pt-2">top_p</h1>
        <input v-model="p_top_p" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

        <!-- batch_size  -->
        <h1 class="font-light pt-2">batch_size</h1>
        <input v-model="p_batch_size" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

        <h1 class="font-light pt-2">Stop sequences</h1>
        <input v-model="p_stop_words" type="text" class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">
          <h1 class="font-light pt-2">Injert at end</h1>
        <input v-model="p_injertion_end" type="text" class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">

        <div class="flex items-center">
          <input type="checkbox" v-model="p_interactive" id="checkbox" class="form-checkbox  text-indigo-500 h-4 w-4">
          <label for="checkbox" class="align-middle ml-2">Interactive mode</label>
        </div>

      </div>
    </div>

    <div class="flex">
      <div class="flex p-2 pt-4 pl-4">
        <!-- Botón Submit en la parte inferior -->
        <button class="bg-teal-500 hover:bg-teal-700 duration-300 text-white font-light py-1 px-4 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500" 
        :class="{ 'opacity-50': completing }"
        @click="completing ? stopCompletion() : getStreamCompletion()">
        {{ completing ? "Cancel" : "Submit" }}
        </button>
        
        </div>
        <p class="absolute mt-4 right-10">More information on: <a href="https://github.com/ggerganov/llama.cpp/tree/master/examples/server" target="_blank">llama.cpp/server</a></p>
        </div>

  </div>
</template>

<script>
import { nextTick, ref } from 'vue'

export default {
  name:"Playground",
  setup(){
    const promptBoxContent = ref("")
    const promptBoxArea = ref()
    const completing = ref(false);

    const presets = ref({
        "<Click here>":"",
        "Default":"Hello World, how are",
        "Chat Style":"This is a chat between a human and assistant\n### Human:Hello.\n### Assistant:Hello Human\n### Human:",
        "Summarization":"Text:\n\n\ntldr:"
    })

    // parameters
    const p_batch_size = ref(128)
    const p_temperature = ref(0.1)
    const p_top_k = ref(40)
    const p_top_p = ref(0.9)
    const p_n_keep = ref(-1)
    const p_n_predict = ref(20)
    const p_as_loop = ref(true)
    const p_stop_words = ref("### Human:")
    const p_interactive = ref(true)
    const p_injertion_end = ref("### Human:")

    const switchGeneratingMode = () => {
        promptBoxArea.value.disabled = !promptBoxArea.value.disabled
        completing.value = !completing.value
    }

    const stopCompletion = ()=>{
      if(completing.value){
        switchGeneratingMode()
        console.info("[!] Completion stopped")
      }else{
        console.info("[?] No completion in progress.")
      }
    }

    const scrollTextAreaToBottom = async () => {
      await nextTick()
      promptBoxArea.value.scrollTop = promptBoxArea.value.scrollHeight
    }

    const clearAll = ()=> {
      promptBoxContent.value = ""
    }
    const splitSequence = (input)=>{
      const words = input.length>0?input.split(','):[]
      return words;
    }

    const handlePresets = (event)=>{
      const presetKey = event.target.value
      console.log("[!] Selected preset prompt", presetKey)

      promptBoxContent.value = presets.value[presetKey]

    }
    async function getStreamCompletion () {
      const data = {
        prompt:promptBoxContent.value,
        batch_size: p_batch_size.value,
        temperature: p_temperature.value,
        top_k: p_top_k.value,
        top_p: p_top_p.value,
        n_keep: p_n_keep.value,
        n_predict: p_n_predict.value,
        as_loop: p_as_loop.value,
        stop: splitSequence(p_stop_words.value),
        interactive: p_interactive.value
      };

      switchGeneratingMode()
      try {
        console.info("[!] Sending Prompt...", data)
        const response = await fetch('/api/completion', { method:'POST', body: JSON.stringify(data) })
      } catch(error){
        console.error("[x] Error requesting completion.")
        return false
      }
      console.info("[!] Completing in progress...")

      while(completing.value){
        try {
          const response = await fetch('/api/next-token', {method:'GET'})
          if(response?.ok){
            const result =  await response.json();
            promptBoxContent.value += result.content
            scrollTextAreaToBottom()
            // Check prompt stream stop
            if(result.stop){
              switchGeneratingMode()
              console.info("[!] Completion finished.")
              if(p_interactive.value){
                promptBoxContent.value += p_injertion_end.value
              }
              promptBoxArea.value.focus()
              break;
            }
          }else{
              console.error("[x] Error on token-streaming caused by:", response.statusText)
              break;
          }
        } catch(error){
          console.error("[x] Error:", error)
          break;
        }
      }
    }

    return {
      getStreamCompletion,
      promptBoxContent,
      promptBoxArea,
      completing,

      // Parameters
      p_batch_size,
      p_temperature,
      p_top_k,
      p_top_p,
      p_n_keep,
      p_n_predict,
      p_as_loop,
      p_stop_words,
      p_interactive,
      p_interactive,
      p_injertion_end,
      presets,
      handlePresets,
      stopCompletion,
      clearAll
    }
  }
}
</script>


<style scoped>

</style>
