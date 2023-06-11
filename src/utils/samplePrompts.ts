import { reactive  } from 'vue'

const prompts = {
    "<Click here>":"",
    "Default":"Hello World, how are",
    "Text Translation":"Spanish:La Tierra (del latín Terra,17​ deidad romana equivalente a Gea, diosa griega de la feminidad y la fecundidad) es un planeta del sistema solar que gira alrededor de su estrella —el Sol— en la tercera órbita más interna. Es el más denso y el quinto mayor de los ocho planetas del sistema solar. También es el mayor de los cuatro terrestres o rocosos.\n\nEnglish:",
    "Chat Style":"This is a chat between a human and assistant\n### Human:Hello.\n### Assistant:Hello Human\n### Human:",
    "Summarization":"Text:\n\n\ntldr:"
}


let samplePrompts = reactive({})

Object.assign(samplePrompts,prompts)

export { samplePrompts }