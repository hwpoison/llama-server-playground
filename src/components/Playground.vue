<template>
  <div  class="lg:h-[91vh] h-[85vh] cursor-default" 
  @keyup.ctrl.enter="getStreamCompletion()"
  @keyup.alt.c="stopCompletion()"
  @keyup.alt.l="clearAll()"
  >


    <div class="flex h-full">
      <div class="flex-grow w-full h-full pb-10 bg-gray-50 p-4">
        <h2 class="flex justify-start text-xl font-bold mb-4">LLaMA Playground<div :class="{ 'hidden' : !completing }"><svg fill="rgb(20 184 166)" width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle class="spinner_I8Q1" cx="4" cy="12" r="1.5"/><circle class="spinner_I8Q1 spinner_vrS7" cx="12" cy="12" r="3"/><circle class="spinner_I8Q1"  cx="20" cy="12" r="1.5"/></svg></div></h2>

        <!-- Prompt Area -->
        <textarea ref="promptBoxArea" v-model="promptBoxContent" class="w-full h-full resize-none p-4 border-2 rounded-md border-neutral-300 outline-none" placeholder="Put your prompt..."></textarea>
      </div>

      <!-- Settings panel -->
      <div class="w-1/4 p-4 bg-gray-50  overflow-auto ">
        <h2 class="text-xl font-bold mb-4">Settings</h2>

        <div class="pt-4">
          <div class="bg-indigo-50 rounded p-3">
            <!-- Preset select -->
            <h1 class="font-light pt-2">Prompt samples</h1>
            <select class="w-4/5   block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none w- focus:ring-indigo-500" @change="handlePresets($event)">
              <option v-for="value, key in samplePrompts" :value="value.value" :key="value.value">{{ key }}</option>
            </select>
            <h1 class="font-light pt-2">Stop word</h1>
            <PopOver target="p_stop_sequence" title="Stop Sequences" message="The prompt completion will stop when this value/s are detected. Input split separated with ','"></PopOver>
            <input data-popover-target="p_stop_sequence" v-model="p_stop_words" type="text" class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">

            <h1 class="font-light pt-2">Injert at end</h1>
            <PopOver target="p_injert_end" title="Injert at the end" message="After each completion and if interaction mode is checked, this value will be added at the end of the prompt."></PopOver>
            <input data-popover-target="p_injert_end" v-model="p_injertion_end" type="text" class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">

            <PopOver target="p_interactive_mode" title="Interactive mode" message="The completion stops when a stop word is detected."></PopOver>
            <div data-popover-target="p_interactive_mode" class="flex items-center">
              <input   type="checkbox" v-model="p_interactive" id="checkbox" class="form-checkbox  text-indigo-500 h-4 w-4">
              <label for="checkbox" class="align-middle ml-2">Interactive mode</label>
            </div>
          </div>
        </div>  
        <div class="py-3">
          <div class="bg-indigo-50  rounded p-3">
            <!-- temperature -->
            <h1 class="font-light pt-2">Temperature</h1>
            <PopOver target="n_p_temperature" title="Temperature" message="Control the randomness or creativity."></PopOver>
            <input data-popover-target="n_p_temperature" v-model="p_temperature" type="number" step="0.1" min="0" max="1"  class="appearance-none block w-full py-2 px-3  w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">
            
            <!-- n_predict  -->
            <h1 class="font-light pt-2">n_predict</h1>
            <PopOver target="n_p_tooltip" title="Numbers of tokens" message="Numbers of tokens to predict when output is generated."></PopOver>
            <input data-popover-target="n_p_tooltip"  v-model="p_n_predict" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            
            <!-- top_k  -->
            <h1 class="font-light pt-2">top_k</h1>
            <PopOver target="n_p_top_k" title="Top K" message="During each token, select the most probable from K tokens. (defaul: 40)."></PopOver>
            <input data-popover-target="n_p_top_k"  v-model="p_top_k" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- top_p  -->
            <h1 class="font-light pt-2">top_p</h1>
            <PopOver target="n_p_top_p" title="Top P" message="Limits the selection of the next token based on the most probable amount over P. (default:0.9)"></PopOver>
            <input data-popover-target="n_p_top_p"   v-model="p_top_p" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">
            
            <!-- n_keep  -->
            <h1 class="font-light pt-2">n_keep</h1>
            <input v-model="p_n_keep" type="number" step="1" min="-1" max="2048"  class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- threads  -->
            <h1 class="font-light pt-2">threads</h1>
            <input v-model="p_threads" type="number" step="1" min="1" max="2048"  class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- batch_size  -->
            <h1 class="font-light pt-2">batch_size</h1>
            <PopOver target="n_p_batch_size" title="Batch size" message="Process the set-aside prompt"></PopOver>
            <input data-popover-target="n_p_batch_size" v-model="p_batch_size" type="number" step="1" min="0" max="2048"  class="appearance-none block w-full py-2 px-3 w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">
          </div>
        </div>
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

</template>

<script>
import { nextTick, ref } from 'vue'
import { samplePrompts } from "../utils/samplePrompts";
import PopOver from "../components/PopOver.vue"

export default {
  name:"Playground",
  components:{
    PopOver
  },
  setup(props){
    const promptBoxContent = ref("")
    const promptBoxArea = ref()
    const completing = ref(false);

    // parameters
    const p_batch_size = ref(128)
    const p_temperature = ref(0.1)
    const p_top_k = ref(40)
    const p_top_p = ref(0.9)
    const p_n_keep = ref(0)
    const p_n_predict = ref(20)
    const p_as_loop = ref(true)
    const p_stop_words = ref("### Human:")
    const p_interactive = ref(false)
    const p_injertion_end = ref("### Human:")
    const p_threads = ref(4)
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
    const splitSequence = (input) => {
      const words = input.length>0?input.split(','):[]
      return words;
    }

    const handlePresets = (event) => {
      const presetKey = event.target.value
      console.log("[!] Selected preset prompt", presetKey)

      promptBoxContent.value = samplePrompts[presetKey]

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
        threads:p_threads.value,
        as_loop: p_as_loop.value,
        
        interactive: p_interactive.value
      };
      if(p_interactive.value){
        data.stop = splitSequence(p_stop_words.value)
      }
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
      samplePrompts,
      // Parameters
      p_batch_size,
      p_temperature,
      p_top_k,
      p_top_p,
      p_n_keep,
      p_n_predict,
      p_threads,
      p_as_loop,
      p_stop_words,
      p_interactive,
      p_interactive,
      p_injertion_end,
      handlePresets,
      stopCompletion,
      clearAll
    }
  }
}
</script>
<style>
.spinner_I8Q1{animation:spinner_qhi1 .75s linear infinite}.spinner_vrS7{animation-delay:-.375s}@keyframes spinner_qhi1{0%,100%{r:1.5px}50%{r:3px}}
</style>