import { reactive } from 'vue'

const prompts = {
  "<Click here>": "",
  "Chat Style": "This is a chat between a human and assistant\n### Human:Hello.\n### Assistant:Hello Human\n### Human:",
  "Summarization": "Text:Apollo 11 (July 16–24, 1969) was the American spaceflight that first landed humans on the Moon. Commander Neil Armstrong and lunar module pilot Buzz Aldrin landed the Apollo Lunar Module Eagle on July 20, 1969, at 20:17 UTC, and Armstrong became the first person to step onto the Moon's surface six hours and 39 minutes later, on July 21 at 02:56 UTC. Aldrin joined him 19 minutes later, and they spent about two and a quarter hours together exploring the site they had named Tranquility Base upon landing. Armstrong and Aldrin collected 47.5 pounds (21.5 kg) of lunar material to bring back to Earth as pilot Michael Collins flew the Command Module Columbia in lunar orbit, and were on the Moon's surface for 21 hours, 36 minutes before lifting off to rejoin Columbia.\n\n\nTl;dr",
  "Default": "Hello World, how are",
  "Text Translation": "Spanish:La Tierra (del latín Terra,17​ deidad romana equivalente a Gea, diosa griega de la feminidad y la fecundidad) es un planeta del sistema solar que gira alrededor de su estrella —el Sol— en la tercera órbita más interna. Es el más denso y el quinto mayor de los ocho planetas del sistema solar. También es el mayor de los cuatro terrestres o rocosos.\n\nEnglish:",

}

const defaultInterjectWord = "### Human:"
const completionApiEndpoint = '/api/completion'

// prompt parameters
const promptParams = reactive({
  temperature: {
    value: 0.8,
    description: "Control the randomness or creativity. More temperature, more creativity, less temperature, more coherent and exact about the previous context."
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
    description: "Enable Mirostat sampling, controlling perplexity during text generation, less perplexity generates a text more preditable and coherent (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)."
  }
})

let samplePrompts = reactive({})

Object.assign(samplePrompts, prompts)

export { completionApiEndpoint, samplePrompts, promptParams, defaultInterjectWord }