<template>
  <div class="inset-0 lg:h-[91vh] h-[80vh] md:h-[90vh]  cursor-default" 
    @keyup.alt.l="emptyPromptBox" 
    @keyup.alt.r="retryCompletion"
    @keyup.prevent.ctrl.z="undoCompletion"
  >
  <div id="header-background" class="absolute right-0 bg-white w-1/2 h-32"></div>
    <div class="flex h-full">
      <div class="flex-grow w-full h-full pb-10 bg-gray-50 p-4">
        <h2 class="flex justify-start text-sm md:text-lg font-bold mb-4 subpixel-antialiased">🦙LLaMA Playground<div
            :class="{ 'hidden': !state.isCompletionInProgress }"><svg fill="rgb(20 184 166)" width="24" height="24"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <circle class="spinner_I8Q1" cx="4" cy="12" r="1.5" />
              <circle class="spinner_I8Q1 spinner_vrS7" cx="12" cy="12" r="3" />
              <circle class="spinner_I8Q1" cx="20" cy="12" r="1.5" />
            </svg></div>
        </h2>
        
        <!-- Prompt Area -->
        <div ref="promptBoxArea" contenteditable="true" @input="updateValue($event)"
          class="relative w-full h-full overflow-y-scroll resize-none p-3 border-2 rounded-md duration-500 border-teal-500 focus:ring-teal-500 focus:border-teal-600 focus:outline-0">
        </div>
        <div class="absolute right-0 bottom-0 m-4 text-gray-500"> {{ state.llamaStats.timingMsg }}</div>
      </div>
      

      <!-- Settings panel -->
      <div class="w-1/4 p-4 bg-gray-50 scroll-smooth overflow-y-scroll hidden md:block ">
        <h2 class="text-xl font-bold mb-4 absolute">⚙️Settings</h2>
        
        <div class="pt-10">
          <div class="bg-indigo-50 rounded-lg p-3">

            <!-- Preset select -->
            <h1 class="font-light pt-2">Prompt samples</h1>
            <select
              class="w-4/5 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none w- focus:ring-indigo-500"
              @change="loadExamplePrompt($event)">
              <option v-for="value, key in samplePrompts" :value="value.value" :key="value.value">{{ key }}</option>
            </select>
            <h1 class="font-light pt-2">Stop word</h1>
            <PopOver target="p_stop_sequence" title="Stop Sequences" :message="promptParams.stop_words.description">
            </PopOver>
            <input data-popover-target="p_stop_sequence" data-popover-placement="left"
              v-model="promptParams.stop_words.value" type="text"
              class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">

            <h1 class="font-light pt-2">Injert at end</h1>
            <PopOver target="p_injert_end" title="Injert at the end" :message="promptParams.injection_word.description">
            </PopOver>
            <input data-popover-target="p_injert_end" data-popover-placement="left"
              v-model="promptParams.injection_word.value" type="text"
              class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">

            <PopOver target="interactive_mode" title="Interactive mode" :message="promptParams.interactive.description">
            </PopOver>
            <div data-popover-target="interactive_mode" data-popover-placement="left" class="flex items-center pt-3 ">
              <input type="checkbox" v-model="promptParams.interactive.value" id="checkbox"
                class="form-checkbox  text-indigo-500 h-4 w-4">
              <label for="checkbox" class="align-middle ml-2">Interactive mode</label>
            </div>
          </div>
        </div>

        <div class="py-3">
          <div class="bg-indigo-50 rounded-lg p-3">
            <!-- temperature -->
            <h1 class="font-light pt-2">Temperature</h1>
            <PopOver target="n_p_temperature" title="Temperature" :message="promptParams.temperature.description">
            </PopOver>
            <input data-popover-target="n_p_temperature" data-popover-placement="left"
              v-model="promptParams.temperature.value" type="number" step="0.1" min="0" max="1"
              class="appearance-none block w-full py-2 px-3  w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- n_predict  -->
            <h1 class="font-light pt-2">n_predict</h1>
            <PopOver target="n_p_tooltip" title="Numbers of tokens" :message="promptParams.n_predict.description">
            </PopOver>
            <input data-popover-target="n_p_tooltip" data-popover-placement="left" v-model="promptParams.n_predict.value"
              type="number" step="1" min="0" max="2048"
              class="appearance-none block w-full py-2 px-3 w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">


            <!-- top_k  -->
            <h1 class="font-light pt-2">top_k</h1>
            <PopOver target="n_top_k" title="Top K" :message="promptParams.top_k.description"></PopOver>
            <input data-popover-target="n_top_k" data-popover-placement="left" v-model="promptParams.top_k.value"
              type="number" step="1" min="0" max="2048"
              class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- top_p  -->
            <h1 class="font-light pt-2">top_p</h1>
            <PopOver target="n_p_top_p" title="Top P" :message="promptParams.top_p.description">
            </PopOver>
            <input data-popover-target="n_p_top_p" data-popover-placement="left" v-model="promptParams.top_p.value"
              type="number" step="1" min="0" max="2048"
              class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- seed  -->
            <h1 class="font-light pt-2">seed</h1>
            <PopOver target="n_p_seed" title="Seed" :message="promptParams.seed.description">
            </PopOver>
            <input data-popover-target="n_p_seed" data-popover-placement="left" v-model="promptParams.seed.value"
              type="number"
              class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- n_keep  -->
            <h1 class="font-light pt-2">n_keep</h1>
            <input v-model="promptParams.n_keep.value" type="number" step="1" min="-1" max="2048"
              class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- Mirostate select -->
            <h1 class="font-light pt-2">Mirostat</h1>
            <PopOver target="n_p_mirostate" title="Mirostate" :message="promptParams.mirostat.description">
            </PopOver>
            <select data-popover-target="n_p_mirostate" data-popover-placement="left"
              class="w-4/5 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none w- focus:ring-indigo-500"
              @change="promptParams.mirostat.value = parseInt($event.target.value)">
              <option v-for="value, key in promptParams.mirostat.options" :value="value.value" :key="value.value">{{ key
              }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="flex">
    <div class="flex p-2 pt-4 pl-4">

      <!-- Undo button -->
      <button class="transition-opacity duration-700 ui-control-button-default" :class="{ 'transition-opacity duration-500 opacity-50': state.isCompletionInProgress }"
        @click="undoCompletion()">
        <div class="w-5 h-5 ">
          <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3"></path>
          </svg>
        </div>
      </button>

      <!-- Retry button -->
      <button class="transition-opacity duration-700 ui-control-button-default" :class="{ 'transition-opacity duration-500 opacity-50': state.isCompletionInProgress }"
        @click="retryCompletion()">
        <div class="w-5 h-5 ">
          <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99">
            </path>
          </svg>
        </div>
      </button>

      <!-- Submit button -->
      <button class="ui-control-button-default" :class="{ 'bg-teal-700': state.isCompletionInProgress }"
        @click="state.isCompletionInProgress ? stopCompletion() : doCompletion()">
        {{ state.isCompletionInProgress ? "Cancel" : "Submit" }}
      </button><p class="text-gray-500 pt-2 text-xs cursor-default">(Ctrl+Enter)</p>

      <p class="pl-4 align-middle text-red-600 pt-1 truncate" :class="{ 'visible': state.errorMessage }"> {{ state.errorMessage }} </p>
    </div>
    <!-- <p class="absolute mt-4 right-10 hidden md:block "><a
        href="https://github.com/ggerganov/llama.cpp/tree/master/examples/server" target="_blank">More info:
        https://github.com/ggerganov/llama.cpp</a></p> -->
  </div>
</template>

<script>
import { nextTick, ref, reactive, onMounted } from 'vue'
import { completionApiEndpoint, samplePrompts, promptParams } from "../utils/configs";
import PopOver from "../components/PopOver.vue"

export default {
  name: "Playground",
  components: {
    PopOver
  },
  setup(props) {
    const promptBoxArea = ref('')

    const state = reactive({
      isCompletionInProgress : false,
      errorMessage : '',
      completionHistory : [],
      llamaStats:{timingMsg:''}
    })

    onMounted(() => {
      document.addEventListener('keyup', triggerCompletion);
      simulateCompletion();
    })

    function simulateCompletion() {
      state.completionHistory.push(promptBoxArea.value.innerText.slice())
      writePromptBox("Hello\n")
      state.completionHistory.push(promptBoxArea.value.innerText.slice())
      writePromptBox("This\n")
    }

    function updateValue(event) {
      promptBoxArea.value = event.target;
    }

    function emptyPromptBox() {
      promptBoxArea.value.innerText = ""
    }

    function undoCompletion() {
      if (state.completionHistory.length) {
        stopCompletion()
        promptBoxArea.value.innerText = state.completionHistory.pop()
        completionModeOff()
        console.info("⏪ Undo completion")
      }
    }

    function retryCompletion() {
      console.log("🔁 Retrying")
      stopCompletion()
      undoCompletion()
      doCompletion()
    }

    function completionModeOn() {
      promptBoxArea.value.contentEditable = false
      state.isCompletionInProgress = true
    }

    function completionModeOff() {
      promptBoxArea.value.contentEditable = true
      state.isCompletionInProgress = false
      scrollTextAreaToBottom()
    }
    
    async function stopCompletion() {
      if (!state.isCompletionInProgress) {
        return false
      }
      completionModeOff()
      console.info("Completion stopped by user.")
      return true
    }

    async function scrollTextAreaToBottom() {
      await nextTick()
      promptBoxArea.value.scrollTop = promptBoxArea.value.scrollHeight
      const range = document.createRange();
      const sel = window.getSelection();
      range.selectNodeContents(promptBoxArea.value);
      range.collapse(false);
      sel.removeAllRanges();
      sel.addRange(range);
      promptBoxArea.value.focus();
    }

    // Add token/text to promptBoxArea using smooth fade in 
    function writePromptBox(text) {
      const lines = text.split(/(\n)/).filter(line => line !== '')
      lines.forEach((line) => {
        if (line == '\n') {
          promptBoxArea.value.innerText += '\n';
        } else {
          let newToken = document.createElement("span");
          newToken.textContent = line;
          newToken.classList.add("transition-token-opacity");
          newToken.style.opacity = "0";
          promptBoxArea.value.appendChild(newToken);
          window.getComputedStyle(newToken).opacity; // force re-draw
          newToken.style.opacity = "1";
        }
      })
    }

    function loadExamplePrompt(event) {
      emptyPromptBox()
      writePromptBox(samplePrompts[event.target.value])
    }

    function buildCompletionRequest() {
      const requestBody = {
        prompt: promptBoxArea.value.innerText,
        temperature: promptParams.temperature.value,
        top_k: promptParams.top_k.value,
        top_p: promptParams.top_p.value,
        n_keep: promptParams.n_keep.value,
        n_predict: promptParams.n_predict.value,
        stream: promptParams.stream.value,
        seed: promptParams.seed.value,
        mirostat: promptParams.mirostat.value
      }
      if (promptParams.interactive.value) {
        requestBody.stop = [promptParams.stop_words.value]
      }
      return requestBody
    }

    // Press ctrl+enter for start or stop the completion
    function triggerCompletion(event) {
      if (event.ctrlKey && event.key === 'Enter') {
        state.isCompletionInProgress ? stopCompletion() : doCompletion()
      }
    }

    async function doCompletion() {
      if(promptBoxArea.value)
        state.completionHistory.push(promptBoxArea.value.innerText.slice())
      
      const requestBody = buildCompletionRequest()

      stopCompletion()
      completionModeOn()
      console.info("📨 Submiting params:", requestBody)
      let result;
      try{
        result = await sendRequest(completionApiEndpoint.url, 'POST', requestBody)
      }catch(err){
        console.error("Error:", err.message)
        state.errorMessage = err.message
        return completionModeOff()
      }

      if (!result.ok) {
        state.errorMessage = "Error submiting the prompt, try again."
        return completionModeOff()
      }

      console.info("↺ Prompt submited, now fetching completion...")
      try {
        const reader = result.body.getReader();
        const processStream = ({ done, value }) => {
          if (!state.isCompletionInProgress || done) return
          
          const chunk = new TextDecoder('utf-8').decode(value);
          let chunkContent = chunk.split('\ndata: '); // get all present data
          let chuckData = chunkContent[0]
          
          let message = JSON.parse(chuckData.substring(6))
          writePromptBox(message.content)

          // check summary json sent by server
          if(chunkContent.length > 1){
            message = JSON.parse(chunkContent[1])
            console.log("Completion summary:", message )
            if(message.timings.predicted_per_second)
              state.llamaStats.timingMsg = `Token/sec: ${message.timings.predicted_per_second.toFixed(4)}`
            }

          // When completion is stopped
          if (message.stop){
            console.info("Completion finished sucessfull.")
            if (promptParams.interactive.value)
              writePromptBox(promptParams.injection_word.value)
            completionModeOff()
          }

          return reader.read().then(processStream)
        };
        return reader.read().then(processStream)

        /*  Most legible alternative but supported only for Firefox
        for await (var stream of result.body) {
          ...
        }*/

      } catch (error) {
        const message = "❌ An error ocurred while stream the completion"
        console.error(message, error)
        state.errorMessage = message
      }

      completionModeOff()
    }
    
    async function sendRequest(url, method, body) {
      const params = {
        'method': method
      }

      if (body) params.body = JSON.stringify(body)

      return await fetch(url, params);
    }

    return {
      state,
      doCompletion,
      promptBoxArea,
      samplePrompts,
      loadExamplePrompt,
      stopCompletion,
      updateValue,
      undoCompletion,
      emptyPromptBox,
      retryCompletion,
      promptParams,
      triggerCompletion
    }
  }
}
</script>
<style>
/* Loading spinner */
.spinner_I8Q1 {
  animation: spinner_qhi1 .75s linear infinite
}

.spinner_vrS7 {
  animation-delay: -.375s
}

@keyframes spinner_qhi1 {

  0%,
  100% {
    r: 1.5px
  }

  50% {
    r: 3px
  }
}

/* Token transition opacity */
.transition-token-opacity {
  opacity: 1;
  transition: opacity 0.3s ease;
}

.ui-control-button-default {
  @apply p-1 bg-teal-600 hover:bg-teal-700 duration-300 text-white mr-2 font-light;
  @apply px-2 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500;
  @apply transition-transform duration-100 transform hover:scale-110 text-base;
}

#header-background {
  background:linear-gradient(to top, rgba(255, 255, 255, 0),rgb(249 250 251)  60%);
}

</style>