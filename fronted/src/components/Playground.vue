<template>
  <div class="inset-0 lg:h-[91vh] h-[81vh] cursor-default" @keyup.ctrl.enter="doCompletion()"
    @keyup.alt.c="stopCompletion()" @keyup.alt.l="clearAll()">
    <div class="flex h-full ">
      <div class="flex-grow w-full h-full pb-10 bg-gray-50 p-4">
        <h2 class="flex justify-start text-xl font-bold mb-4">LLaMA Playground<div
            :class="{ 'hidden': !completionInProgress }"><svg fill="rgb(20 184 166)" width="24" height="24"
              viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <circle class="spinner_I8Q1" cx="4" cy="12" r="1.5" />
              <circle class="spinner_I8Q1 spinner_vrS7" cx="12" cy="12" r="3" />
              <circle class="spinner_I8Q1" cx="20" cy="12" r="1.5" />
            </svg></div>
        </h2>

        <!-- Prompt Area -->
        <textarea ref="promptBoxArea" v-model="promptBoxContent"
          class="w-full h-full resize-none p-4 border-2 rounded-md duration-500 border-teal-500  focus:ring-teal-500 focus:border-teal-600 focus:outline-0"
          placeholder="Write something..."></textarea>
      </div>

      <!-- Settings panel -->
      <div class="w-1/4 p-4 bg-gray-50 overflow-y-scroll hidden md:block ">
        <h2 class="text-xl font-bold mb-4">Settings</h2>
        <div class="">
          <div class="bg-indigo-50 rounded-lg p-3">

            <!-- Preset select -->
            <h1 class="font-light pt-2">Prompt samples</h1>
            <select
              class="w-4/5   block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none w- focus:ring-indigo-500"
              @change="promptSamples($event)">
              <option v-for="value, key in samplePrompts" :value="value.value" :key="value.value">{{ key }}</option>
            </select>
            <h1 class="font-light pt-2">Stop word</h1>
            <PopOver target="p_stop_sequence" title="Stop Sequences" :message="promptParams.stop_words.description">
            </PopOver>
            <input data-popover-target="p_stop_sequence" v-model="promptParams.stop_words.value" type="text"
              class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">

            <h1 class="font-light pt-2">Injert at end</h1>
            <PopOver target="p_injert_end" title="Injert at the end" :message="promptParams.injection_word.description">
            </PopOver>
            <input data-popover-target="p_injert_end" v-model="promptParams.injection_word.value" type="text"
              class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm w-4/5 focus:outline-none focus:ring-indigo-500">

            <PopOver target="interactive_mode" title="Interactive mode" :message="promptParams.interactive.description">
            </PopOver>
            <div data-popover-target="interactive_mode" class="flex items-center pt-3 ">
              <input type="checkbox" v-model="promptParams.interactive.value" id="checkbox"
                class="form-checkbox  text-indigo-500 h-4 w-4">
              <label for="checkbox" class="align-middle ml-2">Interactive mode</label>
            </div>
          </div>
        </div>

        <div class="py-3">
          <div class="bg-indigo-50  rounded-lg p-3">
            <!-- temperature -->
            <h1 class="font-light pt-2">Temperature</h1>
            <PopOver target="n_p_temperature" title="Temperature" :message="promptParams.temperature.description">
            </PopOver>
            <input data-popover-target="n_p_temperature" v-model="promptParams.temperature.value" type="number" step="0.1"
              min="0" max="1"
              class="appearance-none block w-full py-2 px-3  w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- n_predict  -->
            <h1 class="font-light pt-2">n_predict</h1>
            <PopOver target="n_p_tooltip" title="Numbers of tokens" :message="promptParams.n_predict.description">
            </PopOver>
            <input data-popover-target="n_p_tooltip" v-model="promptParams.n_predict.value" type="number" step="1" min="0"
              max="2048"
              class="appearance-none block w-full py-2 px-3 w-4/5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">


            <!-- top_k  -->
            <h1 class="font-light pt-2">top_k</h1>
            <PopOver target="n_top_k" title="Top K" :message="promptParams.top_k.description"></PopOver>
            <input data-popover-target="n_top_k" v-model="promptParams.top_k.value" type="number" step="1" min="0"
              max="2048"
              class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- top_p  -->
            <h1 class="font-light pt-2">top_p</h1>
            <PopOver target="n_p_top_p" title="Top P" :message="promptParams.top_p.description">
            </PopOver>
            <input data-popover-target="n_p_top_p" v-model="promptParams.top_p.value" type="number" step="1" min="0"
              max="2048"
              class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- n_keep  -->
            <h1 class="font-light pt-2">n_keep</h1>
            <input v-model="promptParams.n_keep.value" type="number" step="1" min="-1" max="2048"
              class="appearance-none block w-full py-2 px-3 border w-4/5 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 max-w-xs">

            <!-- Mirostate select -->
            <h1 class="font-light pt-2">Mirostat</h1>
            <PopOver target="n_p_mirostate" title="Mirostate" :message="promptParams.mirostat.description">
            </PopOver>
            <select data-popover-target="n_p_mirostate"
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
      <button
        class="bg-teal-500 hover:bg-teal-700 duration-300 text-white mr-2 font-light px-2 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'opacity-50': completionInProgress }" @click="undoCompletion()">
        <div class="w-5 h-5 ">
          <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3"></path>
          </svg>
        </div>
      </button>

      <!-- Retry button -->
      <button
        class="bg-teal-500 hover:bg-teal-700 duration-300 text-white mr-2 font-light px-2 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'opacity-50': completionInProgress }" @click="retryCompletion()">
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
      <button
        class="bg-teal-500 hover:bg-teal-700 duration-300 text-white font-light py-1 px-4 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        :class="{ 'opacity-50': completionInProgress }" @click="completionInProgress ? stopCompletion() : doCompletion()">
        {{ completionInProgress ? "Cancel" : "Submit" }}
      </button>

      <p class="pl-4 align-middle text-red-600" :class="{ 'visible': errorMessage }"> {{ errorMessage }} </p>
    </div>
    <p class="absolute mt-4 right-10 hidden md:block "><a
        href="https://github.com/ggerganov/llama.cpp/tree/master/examples/server"
        target="_blank">https://github.com/ggerganov/llama.cpp</a></p>
  </div>
</template>

<script>
import { nextTick, ref, reactive, onMounted } from 'vue'
import { samplePrompts } from "../utils/samplePrompts";
import PopOver from "../components/PopOver.vue"

export default {
  name: "Playground",
  components: {
    PopOver
  },
  setup(props) {

    const defaultInterjectWord = "### Human:"
    const promptBoxContent = ref("")
    const promptBoxArea = ref()
    const completionInProgress = ref(false);
    const errorMessage = ref("")
    const fetchingToken = ref(false)
    const completionHistory = ref([])
    const sessionId = ref(undefined)

    // prompt parameters
    const promptParams = reactive({
      temperature: {
        value: 0.8,
        description: "Control the randomness or creativity."
      },
      top_k: {
        value: 40,
        description: "During each token, select the most probable from K tokens. (defaul: 40)."
      },
      top_p: {
        value: 0.9,
        description: "Limits the selection of the next token based on the most probable amount over P. (default:0.9)"
      },
      n_keep: {
        value: 0,
        description: ""
      },
      n_predict: {
        value: 100,
        description: "Numbers of tokens to predict when output is generated."
      },
      stop_words: {
        value: defaultInterjectWord,
        description: "The prompt completion will stop when this value/s are detected. Input split separated with ','"
      },
      injection_word: {
        value: defaultInterjectWord,
        description: "After each completion and if interaction mode is checked, this value will be added at the end of the prompt."
      },
      stream: {
        value: true,
        description: "Stream completion"
      },
      interactive: {
        value: false,
        description: "The completion stops when a stop word is detected."
      },
      seed: {
        value: -1,
        description: "Set the random number generator (RNG) seed (default: -1, < 0 = random seed)"
      },
      mirostat: {
        value: 0,
        options: [0, 1, 2],
        description: "Enable Mirostat sampling, controlling perplexity during text generation (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)."
      }
    })

    function undoCompletion() {
      if (completionHistory.value.length) {
        stopCompletion()
        promptBoxContent.value = completionHistory.value.pop()
        console.info("⏪ Undo completion")
      }
    }

    function retryCompletion() {
      console.log("🔁 Retry")
      stopCompletion()
      undoCompletion()
      doCompletion()
    }

    function completionModeOn() {
      promptBoxArea.value.disabled = true
      completionInProgress.value = true
    }

    function completionModeOff() {
      promptBoxArea.value.disabled = false
      completionInProgress.value = false
    }

    async function stopCompletion() {
      if (!completionInProgress.value) {
        console.info("[?] No completion in progress.")
        return false
      }
      completionModeOff()
    }

    async function scrollTextAreaToBottom() {
      await nextTick()
      promptBoxArea.value.scrollTop = promptBoxArea.value.scrollHeight
    }

    function clearAll() {
      completionHistory.value = []
      promptBoxContent.value = ""
    }

    function splitSequence(input) {
      const words = input.length > 0 ? input.split(',') : []
      return words
    }

    function promptSamples(event) {
      clearAll()
      promptBoxContent.value = samplePrompts[event.target.value]
    }

    function buildCompletionRequest() {
      const completionRequestBody = {
        prompt: promptBoxContent.value,
        temperature: promptParams.temperature.value,
        top_k: promptParams.top_k.value,
        top_p: promptParams.top_p.value,
        stop: promptParams.stop_words.value,
        n_keep: promptParams.n_keep.value,
        n_predict: promptParams.n_predict.value,
        stream: promptParams.stream.value,
        stop: [promptParams.stop_words.value],
        seed: promptParams.seed.value,
        mirostat: promptParams.mirostat.value
      }
      return completionRequestBody;
    }

    async function doCompletion() {
      completionHistory.value.push(promptBoxContent.value)
      errorMessage.value = ''
      const requestBody = buildCompletionRequest()
      try {
        stopCompletion()
        completionModeOn()
        console.info("📨 Submiting params:", requestBody)
        const result = await sendRequest(`/api/${sessionId.value}/completion`, 'POST', requestBody).then(response => {
          console.info("↺ Prompt submited, now fetching completion...")
          const reader = response.body.getReader();
          const processStream = ({ done, value }) => {
            if (done) {
              if (promptParams.interactive.value) {
                promptBoxContent.value += promptParams.injection_word.value
              }
              console.info("🏁 Completion finished.")
              return
            }
            if (!completionInProgress.value) return
            const data = new TextDecoder('utf-8').decode(value);
            const token = JSON.parse(data.substring(6))
            promptBoxContent.value += token.content
            scrollTextAreaToBottom()
            return reader.read().then(processStream)
          };
          return reader.read().then(processStream)
        })
          .catch(error => {
            console.error("❌ Error while stream the completion:", error)
            completionModeOff()
          });
      } catch (error) {
        console.error("❌ Error requesting completion:", error)
        errorMessage.value = "Connection error"
      }
      completionModeOff()
      promptBoxArea.value.focus()
      return false
    }

    async function sendRequest(url, method, body) {
      const params = {
        'method': method
      }

      if (body) params.body = JSON.stringify(body)

      return await fetch(url, params);
    }

    const generateSessionId = () => {
      sessionId.value = Math.random().toString(36).substring(2) + Date.now().toString(36);
    };

    onMounted(() => {
      // This is a temporal session id
      generateSessionId()
      console.info("Session ID:", sessionId.value)
      setInterval(ImHere, 5000)
    });

    function ImHere() {
      try {
        const response = fetch(`/api/imhere/${sessionId.value}`, { method: 'GET' })
      } catch (err) {
      }
    }

    return {
      doCompletion,
      promptBoxContent,
      promptBoxArea,
      completionInProgress,
      samplePrompts,
      promptSamples,
      stopCompletion,
      undoCompletion,
      clearAll,
      errorMessage,
      retryCompletion,
      promptParams
    }
  }
}
</script>
<style>
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
</style>